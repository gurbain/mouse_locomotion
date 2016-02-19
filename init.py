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

print("####################################")
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
 
# Initialize variables here
owner["n_iter"] = 0
owner["cheesy"] = Body(scene, controller, "cheesy")