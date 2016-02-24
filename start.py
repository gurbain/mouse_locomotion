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
import sys

# Default options
BLENDER_PLAYER_PATH = "blender-2.77/blenderplayer"
BLENDER_MODEL = "robot.blend"
SIM_TYPE = "run"
FULLSCREEN_MODE = False
DEBUG_MODE = False
SAVE_OPTION = False

def start_blender():
	""

	# Fetch blender game engine standalone path
	args = [BLENDER_PLAYER_PATH]

	# Add arguments to command line
	args.extend([
		"-w", "1080", "600", "2000", "200",
		"-g", "show_framerate", "=", "1",
		"-g", "show_profile", "=", "1",
		"-g", "show_properties", "=", "1",
		"-g", "ignore_deprecation_warnings", "=", "0",
		"-d",
		])
	# if arg_ !=None:
	# 	args.extend([
	# 		"-", arg_,
	# 		])
	args.extend([BLENDER_MODEL])

	# Start batch process and quit
	subprocess.call(args)

	print ("[INFO] Simulation Finished!")
	return


def run_sim():

	# Set-up simulator options
	exit = False
	n_iter = 0

	# Offilne optimization loop
	while exit == False:

		# Run the simulation
		start_blender()

		# Exit condition is triggered in main.py

		# Check cost function and modify config if needed
		if n_iter >= 0:
			exit = True
		n_iter += 1


def brain_opti_sim():
	print("[INFO] This simulation is not implemented yet! Exiting...")
	exit(0)


def muscle_opti_sim():
	print("[INFO] This simulation is not implemented yet! Exiting...")
	exit(0)


def disp_menu():
	print("This script provide a framework for quadruped locomotion driven by reservoir computing\n")
	print("Usage: ./start.py [-hfsd] [-t TYPE] [-b BLENDERPLAYER] [MODEL]")
	print("Examples:         ./start.py robot.blend")
	print("                  ./start.py -d -f -t brain_optim cheesy.blend\n")
	print("-h                Display this help menu and exit")
	print("-t TYPE           Specify the type of simulation to be done. Avaiblable types are: run")
	print("                  (default); brain_opti; muscle_opti")
	print("-b BLENDERPLAYER  Specify the path for the blenderplayer binaries.")
	print("                  Default: ./blender-2.77/blenderplayer")
	print("-s                Save config at the end of the simulation")
	print("-f                Fullscreen view")
	print("-d                Debug mode")
	exit(0)


if __name__ == '__main__':

	# Arguments parsing
	found_model = False
	i = 0
	for arg in sys.argv:

		if arg.find(".blend") != -1:
			BLENDER_MODEL = arg
			found_model = True

		if arg == "-h":
			disp_menu()

		if arg == "-f":
			FULLSCREEN_MODE = True

		if arg == "-d":
			DEBUG_MODE = True

		if arg == "-s":
			SAVE_OPTION = True

		if arg == "-t":
			if sys.argv[i + 1] == "run":
				SIM_TYPE = "run"
			elif sys.argv[i + 1] == "brain_opti":	
				SIM_TYPE = "brain_opti"
			elif sys.argv[i + 1] == "muscle_opti":	
				SIM_TYPE = "muscle_opti"
			else:
				print("[INFO] No type found after -t option. Using " + SIM_TYPE  + " by default.")

		if arg == "-b":
			if sys.argv[i + 1][0] != '-':
				BLENDER_PLAYER_PATH = sys.argv[i + 1]
			else:
				print("[INFO] No valid blenderplayer binary after option '-b'. Using " + BLENDER_PLAYER_PATH \
					+ " by default.")
		i += 1

	if not found_model:
		print("[INFO] No model found in arguments. Using " + BLENDER_MODEL + " by default.")

	if SIM_TYPE == "brain_opti":
		brain_opti_sim()
	elif SIM_TYPE == "muscle_opti":
		brain_opti_sim()
	else:
		run_sim()
