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

class Config:
	"Describe the configuration file to pass as an argument to a given simulation"

	def __init__(self):
		self.name = "config_1"
		self.a = 1
		self.b = 2
		self.exit_condition = "owner['n_iter'] > 1000"