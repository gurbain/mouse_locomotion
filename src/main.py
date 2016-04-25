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
# File created by: Gabriel Urbain <gabriel.urbain@ugent.be>. February 2016
# Modified by: Dimitri Rodarie
##


import logging
import time
import pickle
import bge

# Get BGE handles
controller = bge.logic.getCurrentController()
exit_actuator = bge.logic.getCurrentController().actuators['quit_game']
keyboard = bge.logic.keyboard


def save():
    global pickle
    """Save te simulation results"""

    f = open(owner["config"].save_path, 'wb')
    pickle.dump([owner["config"], time.time()], f)
    f.close()


# Time-step update instructions
owner["cheesy"].update()

# DEBUG control and display
owner["n_iter"] += 1
owner["config"].logger.debug("Main iteration " + str(owner["n_iter"]) + ": stop state = " +
          str(eval(owner["config"].exit_condition)))
owner["config"].logger.debug("[Interruption: exit = " + str(eval(owner["config"].exit_condition)) +
          " sim time = " + str(time.time() - owner["t_init"]) + " timeout = " + str(owner["config"].timeout))

# Simulation interruption
if eval(owner["config"].exit_condition) \
        or bge.logic.KX_INPUT_ACTIVE == keyboard.events[bge.events.SPACEKEY] \
        or time.time() - owner["t_init"] > owner["config"].timeout:
    # save config
    save()

    # exit
    controller.activate(exit_actuator)