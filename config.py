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
		"Init default config parameters"

		# Simulation parameters
		self.name = ""
		self.sim_speed = 1.0
		self.debug = False
		self.save = False
		self.exit_condition = "owner['n_iter'] > 500"
		
		# Physical parameters
		self.back_legs_muscles = []
		self.front_legs_muscles = []
		self.brain = dict()
		self.body = dict()


class RobotDefConfig(Config):
	"Default configuration file for robot.blend"

	def __init__(self):
		"Init Robot Default Config parameters"

		# Simulation parameters
		self.name = "default_robot_simulation_config"
		self.sim_speed = 1.0
		self.debug = True
		self.save = True
		self.exit_condition = "owner['cheesy'].body.worldPosition.z < -1.8"

		## Back legs
		BL_biceps = {"name" : "B_biceps.L", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_shin.L",\
			"anch_1" : [0.95, -1, -0.54], "anch_2" : [-0.055, 0, 0.6], "k" : 500, \
			"c" : 50, "kc" : -15, "kl0" : 1}
		BR_biceps = {"name" : "B_biceps.R", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_shin.R",\
			"anch_1" : [0.95, 1, -0.54], "anch_2" : [-0.055, 0, 0.6], "k" : 500, \
			"c" : 50, "kc" : -15, "kl0" : 1}
		BL_triceps = {"name" : "B_triceps.L", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_shin.L",\
			"anch_1" : [0.686, -1, 0.094], "anch_2" : [-0.126, 0, 0.84], "k" : 1500, \
			"c" : 150, "kc" : -40, "kl0" : 0.8}
		BR_triceps = {"name" : "B_triceps.R", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_shin.R",\
			"anch_1" : [0.686, 1, 0.094], "anch_2" : [-0.126, 0, 0.84], "k" : 1500, \
			"c" : 150, "kc" : 40, "kl0" : 0.8}
		BL_gastro = {"name" : "B_gastro.L", "debug" : False, "obj_1" : "obj_shin.L", "obj_2" : "obj_shin_lower.L",\
			"anch_1" : [-0.126, 0, 0.84], "anch_2" : [0.125, 0, -0.08], "k" : 10, \
			"c" : 2, "kc" : 0, "kl0" : 1}
		BR_gastro = {"name" : "B_gastro.R", "debug" : False, "obj_1" : "obj_shin.R", "obj_2" : "obj_shin_lower.R",\
			"anch_1" : [-0.126, 0, 0.84], "anch_2" : [0.125, 0, -0.08], "k" : 10, \
			"c" : 2, "kc" : 0, "kl0" : 1}
		self.back_legs_muscles = [BL_biceps, BR_biceps, BL_triceps, BR_triceps, BL_gastro, BR_gastro]
		
		## Front Legs
		FL_biceps = {"name" : "F_biceps.L", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_upper_arm.L",\
			"anch_1" : [-0.93, -1, 0.48], "anch_2" : [-0.01, 0, 0.33], "k" : 400, \
			"c" : 40, "kc" : -5, "kl0" : 1}
		FR_biceps = {"name" : "F_biceps.R", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_upper_arm.R",\
			"anch_1" :  [-0.93, 1, 0.48], "anch_2" : [-0.01, 0, 0.33], "k" : 400, \
			"c" : 40, "kc" : -5, "kl0" : 1}
		FL_triceps = {"name" : "F_triceps.L", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_upper_arm.L",\
			"anch_1" : [-0.61, -1, 0.5], "anch_2" : [0.13, 0, 0.978], "k" : 1000, \
			"c" : 100, "kc" : 30, "kl0" : 0.4}
		FR_triceps = {"name" : "F_triceps.R", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_upper_arm.R",\
			"anch_1" :[-0.61, 1, 0.5], "anch_2" : [0.13, 0, 0.978], "k" : 1000, \
			"c" : 100, "kc" : 30, "kl0" : 0.4}
		FL_gastro = {"name" : "F_gastro.L", "debug" : False, "obj_1" : "obj_upper_arm.L", "obj_2" : "obj_wrist.L",\
			"anch_1" : [0.175, 0, 0.752], "anch_2" : [0.085, 0, 0], "k" : 10, \
			"c" : 2, "kc" : 0, "kl0" : 1}
		FR_gastro = {"name" : "F_gastro.R", "debug" : False, "obj_1" : "obj_upper_arm.R", "obj_2" : "obj_wrist.R",\
			"anch_1" : [0.175, 0, 0.752], "anch_2" : [0.085, 0, 0], "k" : 10, \
			"c" : 2, "kc" : 0, "kl0" : 1}
		self.front_legs_muscles = [FL_biceps, FR_biceps, FL_triceps, FR_triceps, FL_gastro, FR_gastro]

		## Brain
		self.brain = {"name" : "default_robot_matsuoka_brain", "n_osc" : 4, "h" : 1e-3, "tau" : 1e-2,\
			"T" : 5e-2, "a" : 10.5, "b" : 20.5, "c" : 0.08, "aa" : 3, "time_interval" : 1e-3}

		## Body
		neck1 = {"name" : "muscle_neck1", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_head",\
			"anch_1" :  [-0.95, 0, 0.47], "anch_2" : [-0.06, 0, -0.71], "k" : 2000, \
			"c" : 100, "kc" : 0, "kl0" : 0.8}
		neck2 = {"name" : "muscle_neck2", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_head",\
			"anch_1" :  [-0.59, 0, 1.4], "anch_2" : [0.117, 0, -0.26], "k" : 2000, \
			"c" : 100, "kc" : 0, "kl0" : 0.8}
		body_muscles = [neck1, neck2]
		self.body = { "name" : "Doggy", "muscles" : body_muscles}


	def get_params_list(self):
		"Return a list including all the parameters that can be changed to tune the controller model"

		liste = []
		for m in self.back_legs_muscles:
			liste += [m["anch_1"][0], m["anch_1"][1], m["anch_1"][2], m["anch_2"][0], m["anch_2"][1], m["anch_2"][2],\
				m["k"], m["c"], m["kc"], m["kl0"]]
		
		for m in self.front_legs_muscles:
			liste += [m["anch_1"][0], m["anch_1"][1], m["anch_1"][2], m["anch_2"][0], m["anch_2"][1], m["anch_2"][2],\
				m["k"], m["c"], m["kc"], m["kl0"]]
		
		for m in self.body["muscles"]:
			liste += [m["anch_1"][0], m["anch_1"][1], m["anch_1"][2], m["anch_2"][0], m["anch_2"][1], m["anch_2"][2],\
				m["k"], m["c"], m["kc"], m["kl0"]]

		liste += [self.brain["n_osc"], self.brain["h"], self.brain["tau"], self.brain["T"], self.brain["a"],\
			self.brain["b"], self.brain["c"], self.brain["aa"], self.brain["time_interval"]]

		return liste

