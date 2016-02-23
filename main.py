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
import datetime
import os
import pickle

# Get BGE handles
controller = bge.logic.getCurrentController()
owner = controller.owner
exit_actuator = bge.logic.getCurrentController().actuators['quit_game']
keyboard = bge.logic.keyboard

def save():
	dirname = "saved_sim"
	filename = "sim_" + datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S") + ".config"

	if not os.path.exists(dirname):
		os.makedirs(dirname)
	f = open(dirname + "/" + filename, 'wb')
	pickle.dump(owner["config"], f)
	f.close()


# Time-step update instructions
owner["cheesy"].update()


# DEBUG control and display
owner["n_iter"] += 1
if owner["config"].debug:
	print("[DEBUG] Main iteration " + str(owner["n_iter"]) + ": stop state = " + str(eval(owner["config"].exit_condition)))


# Simulation interruption
if eval(owner["config"].exit_condition) or bge.logic.KX_INPUT_ACTIVE == keyboard.events[bge.events.SPACEKEY]:

	# save config
	if owner["config"].save:
		save()

	# exit
	controller.activate(exit_actuator)
