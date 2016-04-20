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

# Add src folder to path
import logging
import logging.config
import os
import sys
import bge
import datetime
import time

root = os.path.dirname(os.path.dirname(bge.logic.expandPath("//")))
src =  root + "/src/"
sys.path.append(src)

from body import *
from config import *

# Blender start
CONFIG_NAME = "RobotVertDefConfig()"
LOG_NAME = os.getenv("HOME") + "/.log/qSim.log"
dirname = root + "/save"
filename = "sim_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".qsm"
if not os.path.exists(dirname):
    os.makedirs(dirname)
SAVE_NAME = dirname + "/" + filename

# Command-line start
if sys.argv[len(sys.argv) - 1] == "FROM_START.PY":
    CONFIG_NAME = sys.argv[len(sys.argv) - 5]
    LOG_NAME = sys.argv[len(sys.argv) - 4]
    LOG_NAME = sys.argv[len(sys.argv) - 3]
    SAVE_OPTION = sys.argv[len(sys.argv) - 2]

# Get BGE handles
controller = bge.logic.getCurrentController()
scene = bge.logic.getCurrentScene()
keyboard = bge.logic.keyboard
owner = controller.owner

# Create python controller
owner["n_iter"] = 0
owner["t_init"] = time.time()
owner["config"] = eval(CONFIG_NAME)
owner["config"].save_path = SAVE_NAME

logging.config.fileConfig(root + "/etc/logging.conf", \
    defaults={'logfilename': LOG_NAME, 'simLevel' : "DEBUG" })
logger = logging.getLogger(owner["config"].logger_name)
owner["config"].logger = logger

logger.info("####################################")
logger.info("##   Mouse Locomotion Simulation   #")
logger.info("##   ---------------------------   #")
logger.info("##                                 #")
logger.info("##   Gabriel Urbain - UGent 2016   #")
logger.info("####################################\n")

owner["cheesy"] = Body(scene, owner["config"])

# Set simulation parameters
bge.logic.setTimeScale(owner["config"].sim_speed)
