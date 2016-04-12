#!/usr/bin/python2

##
# Mouse Locomotion Simulation
# 
# This project provides the user with a framework based on Blender allowing:
#  - Creation and edition of a 3D model
#  - Design of a artificial neural network controller
#  - Offline optimization of the body parameters
#  - Online optimization of the brain controller
# 
# Copyright Gabriel Urbain <gabriel.urbain@ugent.be>. March 2016
# Data Science Lab - Ghent University. Human Brain Project SP10
##

import collections
import logging
import os
import sys
import threading
import time
from threading import Thread, Lock

import rpyc
from rpyc.lib import setup_logger
from rpyc.utils.factory import DiscoveryError
from rpyc.utils.registry import REGISTRY_PORT, DEFAULT_PRUNING_TIMEOUT
from rpyc.utils.registry import UDPRegistryServer
from rpyc.utils.server import ThreadedServer

import sim


class SimManager(Thread):
    """
    SimManager class provides a high level interface to distribute a large number of
    simulation requests in a variable size computation cloud using tools like asynchonous
    request and registry server to monitor the network state via UDP requests.
    Usage:
            # Create and start SimManager thread
            sm = SimManager()
            sm.start()

            # Send simulation list and wait for results
            sim_list = [opt1 opt2]
            res_list = sm.simulate(sim_list)

            # Wait to terminate all work and stop SimManager thread
            sm.terminate()
    """

    def __init__(self):
        """Create sim manager parameters and start registry server"""

        # Simulation list stacks
        # NB: FIFO: append answer on the left and remove the right one
        self.rqt = collections.deque([])  # Request FIFO
        self.rsp = collections.deque([])  # Response FIFO
        self.cloud_state = dict()  # dictionnary of server state on the cloud. Entries are server hashes
        self.server_list = []  # list of active servers
        self.conn_list = []  # list of active RPYC connections

        # Simulation manager parameter
        self.rqt_n = 0
        self.sim_prun_t = 0.1
        self.mng_prun_t = 0.1
        self.mng_stop = False
        self.bg_async_threads = []
        self.reg_found = True
        self.terminated = False
        self.interrupted = False
        self.interrupt_to = 3
        self.server_dispo = False

        # Threading
        self.mutex_cloud_state = Lock()
        self.mutex_server_list = Lock()
        self.mutex_conn_list = Lock()
        self.mutex_rsp = Lock()
        self.mutex_rqt = Lock()
        threading.Thread.__init__(self)

        logging.debug("Sim Manager initialization achieved. Number of active threads = " +
                      str(threading.active_count()))

    def __refresh_cloud_state(self):
        """Refresh the cloud state list using the registry server"""

        # Check network with rpyc registry thread
        self.mutex_server_list.acquire()
        try:
            self.server_list = rpyc.discover("BLENDERSIM")
            logging.debug("Server list " + str(self.server_list))
        except DiscoveryError:
            if self.reg_found:
                logging.info("Simulation servers not found on the network!")
                self.reg_found = False
            pass
        self.mutex_server_list.release()

        if self.server_list and not self.reg_found:
            logging.info("Simulation servers found on the network: " + str(self.server_list))
            self.reg_found = True

        # Lock cloud_state and server_list ressource
        self.mutex_cloud_state.acquire()
        self.mutex_server_list.acquire()

        # Transform server list into a dict
        serv_list_dict = []
        for item in map(lambda x: ["address", x[0], "port", x[1], "n_threads", 0], self.server_list):
            serv_list_dict.append(dict(zip((item[0::2]), (item[1::2]))))
        serv_dict = dict(zip(map(hash, self.server_list), serv_list_dict))

        # Create sets for server_dict and cloud_state
        keys_serv_dict = set(serv_dict.keys())
        keys_cloud_state = set(self.cloud_state.keys())

        # Compare and update cloud_state set if needed
        for elem in keys_serv_dict.difference(keys_cloud_state):
            self.cloud_state[elem] = serv_dict[elem]
        for elem in keys_cloud_state.difference(keys_serv_dict):
            self.cloud_state.pop(elem)

        # Release ressources
        self.mutex_cloud_state.release()
        self.mutex_server_list.release()

        logging.debug("Server list " + str(self.server_list) + " cloud " + str(self.cloud_state))

    def __select_candidate(self):
        """Select the most suited candidate in the simulation cloud. """

        # We check registry_server for new server (adding it as empty one)
        self.__refresh_cloud_state()
        logging.debug("List of registered simulation computers: " + str(self.server_list))

        # We select an available server on the cloud_state list minimizing thread numbers
        self.mutex_cloud_state.acquire()
        for key in self.cloud_state:
            if self.cloud_state[key]["n_threads"] == 0:
                self.mutex_cloud_state.release()
                return key

        for key in self.cloud_state:
            if self.cloud_state[key]["n_threads"] == 1:
                self.mutex_cloud_state.release()
                return key

        self.mutex_cloud_state.release()
        return 0

    def response_sim(self, rsp):
        """Callback function called when a simulation has finished"""

        # We add the rsp from the simulation to the rsp list
        self.mutex_rsp.acquire()
        self.rsp.appendleft(rsp.value)
        self.mutex_rsp.release()

        self.mutex_conn_list.acquire()
        conn_found = False
        for item in self.conn_list:
            if rsp._conn.__hash__() == item["conn"].__hash__():

                conn_found = True
                server_hash = item["server"]

                # Decrease thread number in cloud_state dict
                if server_hash in self.cloud_state:
                    logging.info("Response received from server " + str(self.cloud_state[server_hash]["address"]) +
                                 ":" + str(self.cloud_state[server_hash]["port"]) + " with " +
                                 str(self.cloud_state[server_hash]["n_threads"]) + " threads: " + str(rsp.value))
                    self.mutex_cloud_state.acquire()
                    self.cloud_state[server_hash]["n_threads"] -= 1
                    self.mutex_cloud_state.release()

                else:
                    logging.error("Server " + str(self.cloud_state[server_hash]["address"]) +
                                  ":" + str(self.cloud_state[server_hash]["address"]) +
                                  " not in the list anymore. Please check connection to ensure simulation results.")
                    # Close connection and listening thread
                    # As soon as we stop the thread, the function is directly exited because the callback
                    # function is handle by the thread itself

                logging.info("Deletion of connection: " + str(item["conn"].__hash__()) + "!")
                item["conn"].close()
                t = item["thread"]
                self.conn_list.remove(item)
                self.mutex_conn_list.release()
                t.stop()
                break

        # If no candidate in the list
        if not conn_found:
            logging.error("Connection " + str(rsp._conn.__hash__()) +
                          " not in the list anymore. Please check connection to ensure simulation results.")

        return

    def simulate(self, sim_list):
        """Perform synchronous simulation with the given list and return response list"""

        l_sim_list = len(sim_list)

        # If rqt list is empty
        if not self.rqt:

            # Add to request list
            self.mutex_rqt.acquire()
            self.rqt.extendleft(sim_list)
            sim_n = len(self.rqt)
            self.mutex_rqt.release()

            # Check for simulation and interrupt when processed or interrupted
            to = 0
            while (len(self.rsp) != sim_n or self.rqt) and (not self.terminated) and \
                    (to < self.interrupt_to):
                if self.interrupted:
                    to = time.time() - to_init
                try:
                    time.sleep(self.sim_prun_t)
                except KeyboardInterrupt:
                    logging.warning("Simulation interrupted by user! Please clean up " +
                                    "remote computers.")
                    self.stop()
                    to_init = time.time()
                    self.interrupted = True

            # Create rsp buff and remove all rsp elements
            self.mutex_rsp.acquire()
            rsps = self.rsp
            self.rsp = []
            self.mutex_rsp.release()

            logging.warning("Simulation finished!")
            return rsps

        # If it isn't print error message and return
        else:
            logging.error("Simulation manager hasn't not finished yet with the" +
                          "simulation. Try again later")

            return 0

    def get_cloud_state(self):
        """Return a dict with available machines in the network and their current usage"""

        return self.cloud_state

    def stop(self):
        """Stop managing loop"""

        self.mng_stop = True

    def run(self):
        """Run the managing loop. Check rqt stack for simulation request. Select the candidate \
        server for simulation. Start simulation."""

        logging.info("Start Sim Manager main loop")

        # Continue while not asked for termination or when there are candidates in the list
        # and a server to process them
        while (not self.mng_stop) or (self.rqt and self.server_dispo):

            if self.rqt:

                # Select a candidate server
                server_hash = self.__select_candidate()

                if server_hash != 0:

                    # We found a server
                    self.server_dispo = True
                    logging.info("Starting sim service on server: " +
                                 str(self.cloud_state[server_hash]["address"]) + ":" +
                                 str(self.cloud_state[server_hash]["port"]))

                    # Connect to candidate server
                    try:
                        conn = rpyc.connect(self.cloud_state[server_hash]["address"],
                                            self.cloud_state[server_hash]["port"])

                    except Exception as e:
                        logging.error("Exception when connecting:" + str(e))
                        pass

                    # Update the cloud_state list
                    self.mutex_cloud_state.acquire()
                    self.cloud_state[server_hash]["n_threads"] += 1
                    self.mutex_cloud_state.release()

                    # Create serving thread to handle answer
                    try:
                        bgt = rpyc.BgServingThread(conn)
                    except Exception as e:
                        logging.error("Exception in serving thread:" + str(e))
                        pass

                    self.mutex_conn_list.acquire()
                    self.conn_list.append({"server": server_hash, "conn": conn,
                                           "thread": bgt})
                    self.mutex_conn_list.release()

                    # Create asynchronous handle
                    async_simulation = rpyc.async(conn.root.exposed_simulation)

                    try:
                        # Call asynchronous service
                        res = async_simulation(self.rqt[-1])

                        # Assign asynchronous callback
                        res.add_callback(self.response_sim)

                    except Exception as e:
                        logging.error("Exception from server:" + str(e))
                        pass

                    # Clear request from list: TODO: check if async_simulation don't need it anymore!
                    self.mutex_rqt.acquire()
                    self.rqt.pop()
                    self.mutex_rqt.release()

                else:
                    self.server_dispo = False
                    time.sleep(self.mng_prun_t)

            else:
                time.sleep(self.mng_prun_t)

        logging.info("Simulation Manager has terminated properly!")
        self.terminated = True


class SimRegistry(UDPRegistryServer):
    """
    SimManager class provides a registry server to monitor the network state via UDP requests.
    Usage:
            # Create and start SimRegister thread
            r = SimRegister()
            r.start()
    """

    def __init__(self):
        super(SimRegistry, self).__init__(host='0.0.0.0', port=REGISTRY_PORT,
                                          pruning_timeout=DEFAULT_PRUNING_TIMEOUT)

    def start(self):
        setup_logger(False, None)
        super(SimRegistry, self).start()


class SimService(rpyc.Service):
    """
    SimManager class provides a services server to listen to external requests and start a Blender
    simulation remotely and asynchroously. Results are sent back to SimManager
    Usage:
            # Create and start SimService thread
            s = ThreadedServer(SimService, port=18861, auto_register=True)
            s.start()
    """

    ALIASES = ["BLENDERSIM", "BLENDER", "BLENDERPLAYER"]

    def on_connect(self):
        self.a = 4
        pass

    def on_disconnect(self):
        pass

    def exposed_simulation(self, opt_):  # this is an exposed method

        # Perform simulation
        logging.info("Processing simulation request")
        s = sim.BlenderSim(opt_)
        s.start_blenderplayer()
        logging.info("Simulation request processed")

        return s.get_results()


# Testing functions ###

def start_manager():
    N_SIM = 400

    # Create and start SimManager thread
    t_i = time.time()
    print("#### Starting Sim Manager Test Program with PID " + str(os.getpid()) + " ####")
    sm = SimManager()
    sm.daemon = True
    sm.start()

    # Send simulation list and wait for results
    sim_list = []
    opt = {"blender_path": "blender-2.77/", "blender_model": "robot.blend",
           "config_name": "MouseDefConfig", "sim_type": "run", "registry": False, "service": False,
           "logfile": "stdout", "fullscreen": False, "verbose": "INFO", "save": False}
    for i in range(N_SIM):
        sim_list.append(opt)
    res_list = sm.simulate(sim_list)

    sys.stdout.write("Resultats: ")
    for i in res_list:
        sys.stdout.write(str(i) + " ")
    print("")

    # Wait to terminate all work and stop SimManager thread
    sm.stop()
    time.sleep(1)
    print("#### Exiting Sim Manager Test Program - Sim time: " + str(float("{0:.2f}".format(time.time() - t_i))) +
          " sec for " + str(N_SIM) + " simulations ####")


def start_service():
    t = ThreadedServer(SimService, port=18861, auto_register=True)
    try:
        t.start()
    except KeyboardInterrupt:
        t.stop()
        print "Ctrl-c pressed ..."
        sys.exit(1)


def start_registry():
    r = SimRegistry()
    r.daemon = True
    r.start()


if __name__ == '__main__':

    if len(sys.argv) == 2:
        if sys.argv[1] == "-s":
            start_service()
        elif sys.argv[1] == "-r":
            start_registry()
        elif sys.argv[1] == "-m":
            start_manager()
    else:
        start_manager()
