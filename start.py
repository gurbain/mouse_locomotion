#!/usr/bin/python3

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

import subprocess

BLENDER_PLAYER_PATH = "/home/gabs48/src/blender-2.77/blenderplayer"
BLENDER_MODEL = "robot.blend"

def start_blender_sim(player_path_=BLENDER_PLAYER_PATH, arg_=None):

	# Fetch blender game engine standalone path
	args = [player_path_]

	# Add arguments to command line
	args.extend([
		"-w", "1080", "600", "2000", "200",
		"-g", "show_framerate", "=", "1",
		"-g", "show_profile", "=", "1",
		"-g", "show_properties", "=", "1",
		"-g", "ignore_deprecation_warnings", "=", "0",
		"-d",
		])
	if arg_ !=None:
		args.extend([
			"-", arg_,
			])
	args.extend([BLENDER_MODEL])

	# Start batch process and quit
	subprocess.call(args)

	print ("[INFO] Simulation Finished!")
	return


if __name__ == '__main__':

	# Set-up simulator options
	exit = False
	n_iter = 0

	# Offilne optimization loop
	while exit == False:

		# Run the simulation
		start_blender_sim()

		# Exit condition is triggered in main.py

		# Check cost function and modify config if needed
		if n_iter >= 0:
			exit = True
		n_iter += 1