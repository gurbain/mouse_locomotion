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

# Get BGE handles
controller = bge.logic.getCurrentController()
owner = controller.owner
exit_actuator = bge.logic.getCurrentController().actuators['quit_game']
keyboard = bge.logic.keyboard


# DEBUG Control the muscle length from keyboard
if bge.logic.KX_INPUT_ACTIVE == keyboard.events[bge.events.UPARROWKEY]:
	owner["cheesy"].l_fo_leg.biceps.l0 -= 0.02
	owner["cheesy"].r_fo_leg.biceps.l0 -= 0.02
if bge.logic.KX_INPUT_ACTIVE == keyboard.events[bge.events.DOWNARROWKEY]:
	owner["cheesy"].l_fo_leg.biceps.l0 += 0.02
	owner["cheesy"].r_fo_leg.biceps.l0 += 0.02
if bge.logic.KX_INPUT_ACTIVE == keyboard.events[bge.events.LEFTARROWKEY]:
	owner["cheesy"].l_ba_leg.biceps.l0 -= 0.02
	owner["cheesy"].r_ba_leg.biceps.l0 -= 0.02
if bge.logic.KX_INPUT_ACTIVE == keyboard.events[bge.events.RIGHTARROWKEY]:
	owner["cheesy"].l_ba_leg.biceps.l0 += 0.02
	owner["cheesy"].r_ba_leg.biceps.l0 += 0.02

# Time-step update instructions
owner["n_iter"] += 1
owner["cheesy"].update_mvt()
print("[DEBUG] Main iteration: " + str(owner["n_iter"]))

# When condition encountered, stop the simulation
if owner['n_iter'] > 1000:

	# save bge.logic.globalDict
	controller.activate(exit_actuator)