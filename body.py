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

	def __init__(self, scene_, controller_):
		"Class initialization"
		
		self.n_iter = 0
		self.scene = scene_
		self.controller = controller_

	def update(self):
		"Update control signals and forces"
		
		self.n_iter += 1
		#print("[DEBUG] Leg iteration: " + str(self.n_iter))


class Backleg(Leg):
	"This class represents a generic backleg and its current behaviour in the control process"

	def __init__(self, scene_, controller_, orien_):
		"Class initialization"
		
		super().__init__(scene_, controller_)
		self.orien = orien_

		# Bones objects
		self.tarsus =  self.scene.objects["obj_shin_lower." + self.orien]
		self.tibia =  self.scene.objects["obj_shin." + self.orien]
		self.femur =  self.scene.objects["obj_thigh." + self.orien]

		# Muscle LOCAL anchors position
		self.biceps_femur_anch = vec((0, 0, 0))
		self.biceps_tibia_anch = vec((0, 0, 0))
		self.gastro_tibia_anch = vec((0, 0, 0))
		self.gastro_tarsus_anch = vec((0, 0, 0))

		# Muscles
		self.biceps = Muscle(self.scene, self.controller, self.femur, self.tibia, \
			self.biceps_femur_anch, self.biceps_tibia_anch, "B_biceps." + self.orien, 1000, 100, 30)
		self.gastrocnemius =  Muscle(self.scene, self.controller, self.tibia, self.tarsus, \
			self.gastro_tibia_anch, self.gastro_tarsus_anch, "B_gastrocnemius." + self.orien,  10, 2, 0)

	def update(self, ctrl_sig_=0):
		"Update control signals and forces"

		self.biceps.update(ctrl_sig_)
		self.gastrocnemius.update(ctrl_sig_)
		
		self.n_iter += 1
		print("[DEBUG] Backleg " + self.orien + " iteration " + str(self.n_iter) + ": Control signal = " \
			+  str(ctrl_sig_))


class Foreleg(Leg):
	"This class represents a generic foreleg and its current behaviour in the control process"

	def __init__(self, scene_, controller_, orien_):
		"Class initialization"

		super().__init__(scene_, controller_)
		self.orien = orien_

		# Bones objects
		self.carpus =  self.scene.objects["obj_wrist." + self.orien]
		self.radius =  self.scene.objects["obj_forearm." + self.orien]
		self.humerus =  self.scene.objects["obj_upper_arm." + self.orien]

		# Muscle LOCAL anchors position
		self.biceps_humerus_anch = vec((0, 0, 0))
		self.biceps_radius_anch = vec((0, 0, 0))
		self.triceps_radius_anch = vec((0, 0, 0))
		self.triceps_carpus_anch = vec((0, 0, 0))

		# Muscles
		self.biceps = Muscle(self.scene, self.controller, self.humerus, self.radius, \
			self.biceps_humerus_anch, self.biceps_radius_anch, "F_biceps." + self.orien, 1000, 100, -20)
		self.triceps =  Muscle(self.scene, self.controller, self.radius, self.carpus, \
			self.triceps_radius_anch, self.triceps_carpus_anch, "F_triceps." + self.orien, 10, 2, 0)
		self.biceps.l0 = self.biceps.l0 * 2

	def update(self, ctrl_sig_=0):
		"Update control signals and forces"

		self.biceps.update(ctrl_sig_)
		self.triceps.update(ctrl_sig_)

		self.n_iter += 1
		print("[DEBUG] Foreleg " + self.orien + " iteration " + str(self.n_iter) + ": Control signal = " \
			+  str(ctrl_sig_))


class Body:
	"This class represents the mouse body and its current behaviour in the control process"

	def __init__(self, scene_, controller_, name_="mouse"):
		"Class initialization"
		
		self.n_iter = 0
		self.scene = scene_
		self.controller = controller_
		self.name = name_
		self.l_fo_leg = Foreleg(scene_, controller_, "L")
		self.r_fo_leg = Foreleg(scene_, controller_, "R")
		self.l_ba_leg = Backleg(scene_, controller_, "L")
		self.r_ba_leg = Backleg(scene_, controller_, "R")
		self.brain = Brain(scene_, controller_)

	def update_mvt(self):
		"Update control signals and forces"
		
		self.brain.update() # iterate for new control signal
		self.l_ba_leg.update(float(self.brain.state[0])) # give the control signal
		self.r_ba_leg.update(float(self.brain.state[1])) # give the control signal
		self.l_fo_leg.update(float(self.brain.state[2])) # give the control signal
		self.r_fo_leg.update(float(self.brain.state[3])) # give the control signal
		
		self.n_iter += 1
		print("[DEBUG] Body " + self.name + " iteration " + str(self.n_iter))