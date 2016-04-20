##
# Mouse Locomotion Simulation
#
# This project provides the user with a framework based on Blender allowing:
#  - Creation and edition of a 3D model
#  - Design of a artificial neural network controller
#  - Offline optimization of the body parameters
#  - Online optimization of the brain controller
#
# Copyright Gabriel Urbain <gabriel.urbain@ugent.be>. February 2016
# Data Science Lab - Ghent University. Human Brain Project SP10
##
import datetime
import os
import sys
import time

import bge

root = os.path.dirname(os.path.dirname(bge.logic.expandPath("//")))
src = root + "/src/"
sys.path.append(src)

from body import *
from config import *

print("\n\n####################################")
print("##   Mouse Locomotion Simulation   #")
print("##   ---------------------------   #")
print("##                                 #")
print("##   Gabriel Urbain - UGent 2016   #")
print("####################################\n")

# Get BGE handles
scene = bge.logic.getCurrentScene()

if sys.argv[len(sys.argv) - 1] == "FROM_START.PY":
    # Catch command-line config when started from another script
    argv = sys.argv
    argv = eval(argv[argv.index("-") + 1])
    CONFIG_NAME = argv["config_name"]
    DEBUG_MODE = argv["verbose"]
    SAVE_NAME = argv["filename"]
else:
    # Default config when started directly from Blender
    CONFIG_NAME = "MouseDefConfig()"
    DEBUG_MODE = "INFO"
    dirname = root + "/save"
    filename = "sim_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".qsm"
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    SAVE_NAME = dirname + "/" + filename

# Create python controller
global owner
owner = {"n_iter": 0, "t_init": time.time()}

configuration = eval(CONFIG_NAME)
configuration.debug = DEBUG_MODE
configuration.save_path = SAVE_NAME

owner["config"] = configuration
owner["cheesy"] = Body(scene, configuration)

# Set simulation parameters
bge.logic.setTimeScale(configuration.sim_speed)
