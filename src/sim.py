#!/usr/bin/python2

##
# Mouse Locomotion Simulation
#
# Human Brain Project SP10
# 
# This project provides the user with a framework based on Blender allowing:
#  - Edition of a 3D model
#  - Edition of a physical controller model (torque-based or muscle-based)
#  - Edition of a brain controller model (oscillator-based or neural network-based)
#  - Simulation of the model
#  - Optimization of the parameters in distributed cloud simulations
# 
# File created by: Gabriel Urbain <gabriel.urbain@ugent.be>. March 2016
# Modified by: Dimitri Rodarie
##


import datetime
import fcntl
import logging
import os
import pickle
import pyevolve
from pyevolve import *
import logging
import socket
import struct
import subprocess
import sys
import time

import net
from rpyc.utils.registry import REGISTRY_PORT
from rpyc.utils.server import ThreadedServer


class Simulation:
    """
    Main class for high level simulation. It receives a set of simulation options as defined
    in the DEF_OPT dict. Methods start_service() and start_registry can be launched independently
    to run service and registry	servers. Other methods require a call to start_manager which
    distribute simulation accross the network.
    """

    def __init__(self, opt_=None):
        """Initialize with CLI options"""
        self.opt = opt_
        self.ipaddr = self.__get_ip_address('eth0')
        self.pid = os.getpid()

    def __get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            ip_name = socket.inet_ntoa(fcntl.ioctl(
                s.fileno(),
                0x8915,  # SIOCGIFADDR
                struct.pack('256s', ifname[:15])
            )[20:24])
        except Exception as e:
            logging.warning("No ethernet connection!")
            ip_name = "localhost"

        return ip_name

    def start_service(self):
        """Start a service server"""

        logging.info("Start service server on address: " + str(self.ipaddr) + ":18861")
        self.t = ThreadedServer(net.SimService, port=18861, auto_register=True)
        self.t.start()

    def start_registry(self):
        """Start a registery server"""

        logging.info("Start registry server on address: " + str(self.ipaddr) + ":" + str(REGISTRY_PORT))
        self.r = net.SimRegistry()
        self.r.start()

    def start_manager(self):
        """Start a simulation manager"""

        self.t_sim_init = time.time()
        logging.info("Start sim manager server with PID " + str(self.pid))
        self.sm = net.SimManager()
        self.sm.start()
        time.sleep(1)

    def stop_manager(self):
        """Stop the simulation manager"""

        self.sm.stop()
        time.sleep(1)
        self.sim_time = time.time() - self.t_sim_init

    def run_sim(self):
        """Run a simple one shot simulation"""

        # Start manager
        self.start_manager()

        # Simulate
        sim_list = [self.opt]
        res_list = self.sm.simulate(sim_list)

        # Stop and disply results
        self.stop_manager()
        time.sleep(1)
        rs_ls = ""
        for i in res_list:
            rs_ls += str(i) + " "
        logging.info("Results: " + str(rs_ls))
        logging.info("Simulation Finished!")

    def __create_ga(self):
        """Creation and initialization function for the genome and the genetic algorithm. It fixes the
        parameters to use in the algorithm"""

        # Algo parameters
        self.genome_size = 10
        self.population_size = 20
        self.num_max_generation = 50
        self.mutation_rate = 0.2
        self.cross_over_rate = 0.9
        self.genome_min = 0
        self.genome_max = 1.0
        self.interactive_mode = False
        self.initializator = Initializators.G1DListInitializatorReal
        self.mutator = Mutators.G1DListMutatorRealGaussian
        self.selector = Selectors.GTournamentSelector
        self.stop_num_av = 10
        self.stop_thresh = 0.01
        self.bf_list = []

        # Create a genome instance and parametrize it
        genome = G1DList.G1DList(self.genome_size)
        genome.evaluator.set(self.__eval_fct)
        genome.initializator.set(self.initializator)
        genome.mutator.set(self.mutator)
        genome.setParams(rangemin=self.genome_min, rangemax=self.genome_max)

        # Create a Genetic Algorithm (ga) instance and parametrize it
        ga = GSimpleGA.GSimpleGA(genome)
        ga.selector.set(self.selector)
        ga.setGenerations(self.num_max_generation)
        ga.setMutationRate(self.mutation_rate)
        ga.setPopulationSize(self.population_size)
        ga.setCrossoverRate(self.cross_over_rate)
        ga.setInteractiveMode(self.interactive_mode)
        ga.terminationCriteria.set(self.__conv_fct)

        # Return the algorithm instance
        return ga

    def __eval_fct(self, genome):
        """Evaluation function of the genetic algorithm. For each set of genome, it compute a 
        score and returns it"""

        score = 0.0

        # Create a config for the genome
        self.opt["genome"] = genome.getInternalList()
        logging.info(" ---------------- DEBUT SIM -----------")

        # Simulate
        sim_list = [self.opt]
        res_list = self.sm.simulate(sim_list)

        # In the result list, we look for the score
        score = 1
        logging.info(" ---------------- FIN SIM -----------")

        # Return the score result
        return score

    def __conv_fct(self, ga):
        """Convergence function of the genetic algorithm. It is called at each iteration step and 
        return True of Flase depending on a convergence criteria"""

        # Get best individus
        pop = ga.getPopulation()
        bi = pop.bestFitness()
        self.bf_list.append(bi.getFitnessScore())

        # Return the convergence
        if len(self.bf_list) > self.stop_num_av:
            av = sum(self.bf_list[-self.stop_num_av:]) / self.stop_num_av
            #print("av: " + str(av)  + " curr: " + str(self.bf_lis[-1]) + ' abs: ' + str(abs(self.bf_lis[-1] - av)))
            if  abs(self.bf_list[-1] - av) < self.stop_thresh:
                logging.info("Criterion reached. Best element : " +  str(bi.getInternalList()))
                return True

        return False

    def brain_opti_sim(self):
        """Run an iterative simulation to optimize the muscles parameters"""

        # Start manager
        self.start_manager()

        # Create genetic algorithm
        ga = self.__create_ga()

        # Run genetic algorithm until convergence or max iteration reached
        ga.evolve(freq_stats=10)

        # Stop and disply results
        logging.info("Simulation Finished!")
        self.stop_manager()
        time.sleep(1)
        logging.info(ga.bestIndividual())

    def muscle_opti_sim(self):
        """Run an iterative simulation to optimize the muscles parameters"""

        logging.error("This simulation is not implemented yet! Exiting...")


class BlenderSim:
    """
    Main class for low level simulation. It receives a set of simulation options as defined
    in the DEF_OPT dict. It can only start a simulation via a batch subprocess on localhost.
    """

    def __init__(self, opt_):
        """Initialize with  options"""

        self.opt = opt_
        self.dirname = self.opt["root_dir"] + "/save"
        if not os.path.exists(self.dirname):
            os.makedirs(self.dirname)

    def start_blenderplayer(self):
        """Call blenderplayer via command line subprocess"""

        # Fetch blender game engine standalone path
        args = [self.opt["blender_path"] + "blenderplayer"]

        # Add arguments to command line
        args.extend([
            "-w", "1080", "600", "2000", "200",
            "-g", "show_framerate", "=", "1",
            "-g", "show_profile", "=", "1",
            "-g", "show_properties", "=", "1",
            "-g", "ignore_deprecation_warnings", "=", "0",
            "-d",
        ])

        filename = "sim_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".qsm"
        self.opt["save_path"] = self.dirname + "/" + filename

        if self.opt["fullscreen"]:
            args.extend(["-f"])
        args.extend([self.opt["blender_model"]])
        args.extend(["-"])
        params = {'config_name': self.opt["config_name"] + "()",
                  'logfile': str(self.opt["logfile"]),
                  'filename': str(self.opt["save_path"])}
        args.extend([str(params)])
        args.extend(["FROM_START.PY"])

        # Start batch process and quit
        logging.debug("Subprocess call: " + str(args))
        subprocess.call(args)

    def start_blender_with_player(self):
        """Call blender via command line subprocess and start the game engine simulation"""

        # Fetch blender game engine standalone path
        args = [self.opt["blender_path"] + "blender"]

        # Add arguments to command line
        args.extend([self.opt["blender_model"]])
        args.extend(["--python", "ge.py"])
        args.extend(["--start_player()"])

        # Start batch process and quit
        logging.debug("Subprocess call: " + str(args))
        subprocess.call(args)

    def create_pop(self):
        """Call blender via command line subprocess and create a population out of a model"""

        # Fetch blender game engine standalone path
        args = [self.opt["blender_path"] + "blender"]

        # Add arguments to command line
        args.extend(["-b"])
        args.extend([self.opt["blender_model"]])
        args.extend(["--python", "model.py"])
        args.extend(["--create_pop()"])

        # Start batch process and quit
        logging.debug("Subprocess call: " + str(args))
        subprocess.call(args)

    def get_results(self):
        """This function reads the file saved in Blender at the end of the simulation to retrieve results"""

        # Retrieve filename
        if not "save_path" in self.opt:
            results = "WARNING BlenderSim.get_results() : Nothing to show"
        elif os.path.isfile(self.opt["save_path"]):
            f = open(self.opt["save_path"], 'rb')
            results = pickle.load(f)
            f.close()
        else:
            results = "ERROR BlenderSim.get_results() : Can't open the file " + self.opt[
                "save_path"] + ".\nThe file doesn't exist."
        return results
