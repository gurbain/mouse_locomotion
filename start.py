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
import config

# Default options
BLENDER_PATH = "blender-2.77/"
BLENDER_MODEL = "robot.blend"
CONFIG_NAME = "RobotDefConfig"
SIM_TYPE = "run"
FULLSCREEN_MODE = False
DEBUG_MODE = False
SAVE_OPTION = False

def start_blenderplayer():
	"Call blenderplayer binary via command line subprocess"

	# Fetch blender game engine standalone path
	args = [BLENDER_PATH + "blenderplayer"]

	# Add arguments to command line
	args.extend([
		"-w", "1080", "600", "2000", "200",
		"-g", "show_framerate", "=", "1",
		"-g", "show_profile", "=", "1",
		"-g", "show_properties", "=", "1",
		"-g", "ignore_deprecation_warnings", "=", "0",
		"-d",
		])
	if FULLSCREEN_MODE:
		args.extend(["-f"])
	args.extend([BLENDER_MODEL])
	args.extend(["-", CONFIG_NAME + "()"])
	args.extend([str(DEBUG_MODE), str(SAVE_OPTION)])
	args.extend(["FROM_START.PY"])

	# Start batch process and quit
	subprocess.call(args)


def start_blender():
	"Call blender binary via command line subprocess"

	# Fetch blender game engine standalone path
	args = [BLENDER_PATH + "blender"]

	# Add arguments to command line
	args.extend(["-b"])
	args.extend([BLENDER_MODEL])
	args.extend(["--python", "model.py"])

	# Start batch process and quit
	subprocess.call(args)


def run_sim():
	"Run a simple one shot simulation"

	start_blender()
	start_blenderplayer()
	print ("[INFO] Simulation Finished!")


def brain_opti_sim():
	"Run an iterative simulation to optimize the muscles parameters"
	# Set-up simulator options
	exit = False
	n_iter = 0

	# Offilne optimization loop
	while exit == False:

		# Run the simulation
		start_blenderplayer()

		# Exit condition is triggered in main.py

		# Check cost function and modify config if needed
		if n_iter >= 0:
			exit = True
		n_iter += 1


def muscle_opti_sim():
	"Run an iterative simulation to optimize the muscles parameters"

	print("[INFO] This simulation is not implemented yet! Exiting...")


def disp_menu():
	print("This script provide a framework for quadruped locomotion driven by reservoir computing\n")
	print("Usage: ./start.py [-hfsd] [-t TYPE] [-p BLENDER_PATH] [-c CONFIG] [MODEL]")
	print("Examples:         ./start.py robot.blend")
	print("                  ./start.py -d -f -t brain_optim cheesy.blend\n")
	print("-h                Display this help menu and exit")
	print("-c CONFIG         Specify the configuration file to use. Avaiblable types are:")
	print("                  ", end="")
	for c in dir(config):
		if c != "Config":
			if c == "RobotDefConfig":
				print(c + " (default); ", end="")
			else:
				if c.find("__") == -1:
					print(c + "; ", end="")
	print("\n-t TYPE           Specify the type of simulation to be done. Avaiblable types are:")
	print("                  run (default); brain_opti; muscle_opti")
	print("-p BLENDER_PATH   Specify the path for the blender binaries.")
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
			if i + 1 < len(sys.argv):
				if sys.argv[i + 1][0] != '-':
					BLENDER_PATH = sys.argv[i + 1]
			else:
				print("[INFO] No valid blenderplayer binary after option '-b'. Using " + BLENDER_PATH \
					+ " by default.")

		if arg == "-c":
			if i + 1 < len(sys.argv):
				if sys.argv[i + 1] in dir(config):
					CONFIG_NAME = sys.argv[i + 1]
				else:
					print("[INFO] No valid config name after '-c'. Using " + CONFIG_NAME \
						+ " by default.")
			else:
				print("[INFO] No valid config name after '-c'. Using " + CONFIG_NAME \
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