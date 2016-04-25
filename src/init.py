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


import datetime
import logging.config
import os
import sys
import time

import bge

root = os.path.dirname(os.path.dirname(bge.logic.expandPath("//")))
src = root + "/src/"
sys.path.append(src)

from body import *
from config import *


# Get BGE handles
scene = bge.logic.getCurrentScene()

if sys.argv[len(sys.argv) - 1] == "FROM_START.PY":
    # Catch command-line config when started from another script
    argv = sys.argv
    argv = eval(argv[argv.index("-") + 1])
    CONFIG_NAME = argv["config_name"]
    LOG_FILE = argv["logfile"]
    SAVE_NAME = argv["filename"]
else:
    # Default config when started directly from Blender
    CONFIG_NAME = "DogVertDefConfig()"
    LOG_FILE = os.getenv("HOME") + "/.log/qSim.log"
    dirname = root + "/save"
    filename = "sim_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".qsm"
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    SAVE_NAME = dirname + "/" + filename

# Create python controller
global owner
owner = {"n_iter": 0, "t_init": time.time()}

# Create Logger and configuration
if not os.path.exists(os.path.dirname(LOG_FILE)):
    os.makedirs(os.path.dirname(LOG_FILE))
if not os.path.exists(LOG_FILE):
    f = open(LOG_FILE, 'w')
    f.close()

configuration = eval(CONFIG_NAME)
logging.config.fileConfig(root + "/etc/logging.conf",
                          defaults={'logfilename': LOG_FILE, 'simLevel': "DEBUG"})
logger = logging.getLogger(configuration.logger_name)
configuration.logger = logger
configuration.save_path = SAVE_NAME

owner["config"] = configuration
owner["cheesy"] = Body(scene, configuration)

# Advertise simulation has begun
logger.info("####################################")
logger.info("##   Mouse Locomotion Simulation   #")
logger.info("##   ---------------------------   #")
logger.info("##                                 #")
logger.info("##   Gabriel Urbain - UGent 2016   #")
logger.info("####################################\n")

# Set simulation parameters
bge.logic.setTimeScale(configuration.sim_speed)
