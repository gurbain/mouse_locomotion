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

from brain import Brain
from muscle import Muscle
from mathutils import Vector as vec
import bge


class Leg:
	"This class represents a generic leg and its current behaviour in the control process"

	def __init__(self, scene_, config_):
		"Class initialization"
		
		self.n_iter = 0
		self.scene = scene_
		self.config = config_
		self.debug = self.config.debug

	def update(self):
		"Update control signals and forces"
		
		self.n_iter += 1
		if self.debug:
			print("[DEBUG] Leg iteration: " + str(self.n_iter))


class Backleg(Leg):
	"This class represents a generic backleg and its current behaviour in the control process"

	def __init__(self, scene_, config_, orien_):
		"Class initialization"
		
		super().__init__(scene_, config_)
		self.orien = orien_

		# Create the muscles objects following config
		if self.orien == "L":
			self.biceps = Muscle(self.scene, self.config.back_legs_muscles[0])
			self.triceps = Muscle(self.scene, self.config.back_legs_muscles[2])
			self.gastro = Muscle(self.scene, self.config.back_legs_muscles[4])
		else: # R
			self.biceps = Muscle(self.scene, self.config.back_legs_muscles[1])
			self.triceps = Muscle(self.scene, self.config.back_legs_muscles[3])
			self.gastro = Muscle(self.scene, self.config.back_legs_muscles[5])

	def update(self, ctrl_sig_):
		"Update control signals and forces"

		self.biceps.update(ctrl_sig_[0])
		self.triceps.update(ctrl_sig_[1])
		self.gastro.update(ctrl_sig_[2])
		
		self.n_iter += 1
		if self.debug:
			print("[DEBUG] Backleg " + self.orien + " iteration " + str(self.n_iter) + ": Control signal = " \
				+  str(ctrl_sig_))


class Foreleg(Leg):
	"This class represents a generic foreleg and its current behaviour in the control process"

	def __init__(self, scene_, config_, orien_):
		"Class initialization"

		super().__init__(scene_, config_)
		self.orien = orien_

		# Create the muscles objects following config
		if self.orien == "L":
			self.biceps = Muscle(self.scene, self.config.front_legs_muscles[0])
			self.triceps = Muscle(self.scene, self.config.front_legs_muscles[2])
			self.gastro = Muscle(self.scene, self.config.front_legs_muscles[4])
		else: # R
			self.biceps = Muscle(self.scene, self.config.front_legs_muscles[1])
			self.triceps = Muscle(self.scene, self.config.front_legs_muscles[3])
			self.gastro = Muscle(self.scene, self.config.front_legs_muscles[5])

	def update(self, ctrl_sig_):
		"Update control signals and forces"

		self.biceps.update(ctrl_sig_[0])
		self.triceps.update(ctrl_sig_[1])
		self.gastro.update(ctrl_sig_[2])

		self.n_iter += 1
		if self.debug:
			print("[DEBUG] Foreleg " + self.orien + " iteration " + str(self.n_iter) + ": Control signal = " \
				+  str(ctrl_sig_))


class Body:
	"This class represents the mouse body and its current behaviour in the control process"

	def __init__(self, scene_, config_):
		"Class initialization"
		
		self.n_iter = 0
		self.scene = scene_
		self.config = config_
		self.name = self.config.body["name"]
		self.debug = self.config.debug

		# Create 4 legs
		self.l_fo_leg = Foreleg(scene_, config_, "L")
		self.r_fo_leg = Foreleg(scene_, config_, "R")
		self.l_ba_leg = Backleg(scene_, config_, "L")
		self.r_ba_leg = Backleg(scene_, config_, "R")

		# Create the brain object
		self.brain = Brain(scene_, config_)

		# Create the muscles objects following config
		self.body = self.scene.objects["obj_body"]
		self.muscles = []
		for muscle_config in self.config.body["muscles"]:
			self.muscles.append(Muscle(self.scene, muscle_config))
		

	def update(self):
		"Update control signals and forces"
		
		self.brain.update()

		for muscle in self.muscles:
			muscle.update()

		self.l_ba_leg.update([float(self.brain.state[2]), float(self.brain.state[0]), 0])
		self.r_ba_leg.update([float(self.brain.state[2]), float(self.brain.state[0]), 0])
		self.l_fo_leg.update([float(self.brain.state[0]), float(self.brain.state[1]), 0])
		self.r_fo_leg.update([float(self.brain.state[0]), float(self.brain.state[1]), 0])
		
		self.n_iter += 1
		if self.debug:
			print("[DEBUG] Body " + self.name + " iteration " + str(self.n_iter))