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

import bge
from body import *
from config import *
import sys
import time

# Default config when started directly from Blender
CONFIG_NAME = "MouseDefConfig()"
DEBUG_MODE = "False"
dirname = "../save"
filename = "sim_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".qsm"
if not os.path.exists(dirname):
	os.makedirs(dirname)
SAVE_NAME = dirname + "/" + filename

print("\n\n####################################")
print("##   Mouse Locomotion Simulation   #")
print("##   ---------------------------   #")
print("##                                 #")
print("##   Gabriel Urbain - UGent 2016   #")
print("####################################\n")

# Get BGE handles
controller = bge.logic.getCurrentController()
scene = bge.logic.getCurrentScene()
keyboard = bge.logic.keyboard
owner = controller.owner

# Catch command-line config when started from start.py script
if sys.argv[len(sys.argv) - 1] == "FROM_START.PY":
	CONFIG_NAME = sys.argv[len(sys.argv) - 4]
	DEBUG_MODE = sys.argv[len(sys.argv) - 3]
	SAVE_OPTION = sys.argv[len(sys.argv) - 2]

# Create python controller
owner["n_iter"] = 0
owner["t_init"] = time.time()
owner["config"] = eval(CONFIG_NAME)
owner["config"].debug = eval(DEBUG_MODE)
owner["config"].save = eval(SAVE_OPTION)
owner["cheesy"] = Body(scene, owner["config"])

# Set simulation parameters
bge.logic.setTimeScale(owner["config"].sim_speed)