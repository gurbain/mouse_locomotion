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
		self.back_leg_L_muscles = []
		self.front_leg_R_muscles = []
		self.back_leg_L_muscles = []
		self.front_leg_R_muscles = []
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
		self.exit_condition = "bge.logic.getCurrentScene().objects['obj_body'].worldPosition.z < -1.8"

		## Back legs
		BL_biceps = {"name" : "B_biceps.L", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_shin.L",\
			"anch_1" : [0.95, -1, -0.54], "anch_2" : [-0.055, 0, 0.6], "k" : 500, \
			"c" : 50, "kc" : -15, "kl0" : 1, "brain_sig" : 2}
		BR_biceps = {"name" : "B_biceps.R", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_shin.R",\
			"anch_1" : [0.95, 1, -0.54], "anch_2" : [-0.055, 0, 0.6], "k" : 500, \
			"c" : 50, "kc" : -15, "kl0" : 1, "brain_sig" : 2}
		BL_triceps = {"name" : "B_triceps.L", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_shin.L",\
			"anch_1" : [0.686, -1, 0.094], "anch_2" : [-0.126, 0, 0.84], "k" : 1500, \
			"c" : 150, "kc" : -40, "kl0" : 0.8, "brain_sig" : 0}
		BR_triceps = {"name" : "B_triceps.R", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_shin.R",\
			"anch_1" : [0.686, 1, 0.094], "anch_2" : [-0.126, 0, 0.84], "k" : 1500, \
			"c" : 150, "kc" : -40, "kl0" : 0.8, "brain_sig" : 0}
		BL_gastro = {"name" : "B_gastro.L", "debug" : False, "obj_1" : "obj_shin.L", "obj_2" : "obj_shin_lower.L",\
			"anch_1" : [-0.126, 0, 0.84], "anch_2" : [0.125, 0, -0.08], "k" : 10, \
			"c" : 2, "kc" : 0, "kl0" : 1, "brain_sig" : None}
		BR_gastro = {"name" : "B_gastro.R", "debug" : False, "obj_1" : "obj_shin.R", "obj_2" : "obj_shin_lower.R",\
			"anch_1" : [-0.126, 0, 0.84], "anch_2" : [0.125, 0, -0.08], "k" : 10, \
			"c" : 2, "kc" : 0, "kl0" : 1, "brain_sig" : None}
		self.back_leg_L_muscles = [BL_biceps, BL_triceps,  BL_gastro]
		self.back_leg_R_muscles = [BR_biceps, BR_triceps,  BL_gastro]
		
		## Front Legs
		FL_biceps = {"name" : "F_biceps.L", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_upper_arm.L",\
			"anch_1" : [-0.93, -1, 0.48], "anch_2" : [-0.01, 0, 0.33], "k" : 400, \
			"c" : 40, "kc" : -5, "kl0" : 1, "brain_sig" : 1}
		FR_biceps = {"name" : "F_biceps.R", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_upper_arm.R",\
			"anch_1" :  [-0.93, 1, 0.48], "anch_2" : [-0.01, 0, 0.33], "k" : 400, \
			"c" : 40, "kc" : -5, "kl0" : 1, "brain_sig" : 1}
		FL_triceps = {"name" : "F_triceps.L", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_upper_arm.L",\
			"anch_1" : [-0.61, -1, 0.5], "anch_2" : [0.13, 0, 0.978], "k" : 1000, \
			"c" : 100, "kc" : 30, "kl0" : 0.4, "brain_sig" : 0}
		FR_triceps = {"name" : "F_triceps.R", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_upper_arm.R",\
			"anch_1" :[-0.61, 1, 0.5], "anch_2" : [0.13, 0, 0.978], "k" : 1000, \
			"c" : 100, "kc" : 30, "kl0" : 0.4, "brain_sig" : 0}
		FL_gastro = {"name" : "F_gastro.L", "debug" : False, "obj_1" : "obj_upper_arm.L", "obj_2" : "obj_wrist.L",\
			"anch_1" : [0.175, 0, 0.752], "anch_2" : [0.085, 0, 0], "k" : 10, \
			"c" : 2, "kc" : 0, "kl0" : 1, "brain_sig" : None}
		FR_gastro = {"name" : "F_gastro.R", "debug" : False, "obj_1" : "obj_upper_arm.R", "obj_2" : "obj_wrist.R",\
			"anch_1" : [0.175, 0, 0.752], "anch_2" : [0.085, 0, 0], "k" : 10, \
			"c" : 2, "kc" : 0, "kl0" : 1, "brain_sig" : None}
		self.front_leg_L_muscles = [FL_biceps, FL_triceps, FL_gastro]
		self.front_leg_R_muscles = [FR_biceps, FR_triceps, FR_gastro]

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


class RobotVertDefConfig(Config):
	"Default configuration file for robot_vert.blend"

	def __init__(self):
		"Init Robot Default Config parameters"

		# Simulation parameters
		super().__init__()
		self.name = "default_robot_vert_simulation_config"
		self.sim_speed = 1.0
		self.debug = True
		self.save = True
		self.exit_condition =  "owner['n_iter'] > 2500"#"bge.logic.getCurrentScene().objects['obj_body.B'].worldPosition.z < -1.8"

		## Back legs
		BL_biceps = {"name" : "B_biceps.L", "debug" : False, "obj_1" : "obj_body.B", "obj_2" : "obj_shin.L",\
			"anch_1" : [0.91, -1, -0.3], "anch_2" : [0.066, 0, 0.3], "k" : 500, \
			"c" : 50, "kc" : -40, "kl0" : 1, "brain_sig" : 2}
		BR_biceps = {"name" : "B_biceps.R", "debug" : False, "obj_1" : "obj_body.B", "obj_2" : "obj_shin.R",\
			"anch_1" : [0.91, 1, -0.3], "anch_2" : [0.066, 0, 0.3], "k" : 500, \
			"c" : 50, "kc" : -40, "kl0" : 1, "brain_sig" : 2}
		BL_triceps = {"name" : "B_triceps.L", "debug" : False, "obj_1" : "obj_body.B", "obj_2" : "obj_shin.L",\
			"anch_1" : [0.72, -1, 0.23], "anch_2" : [-0.102, 0, 0.55], "k" : 1000, \
			"c" : 50, "kc" : -40, "kl0" : 0.6, "brain_sig" : None}
		BR_triceps = {"name" : "B_triceps.R", "debug" : False, "obj_1" : "obj_body.B", "obj_2" : "obj_shin.R",\
			"anch_1" : [0.72, 1, 0.23], "anch_2" : [-0.102, 0, 0.55], "k" : 1000, \
			"c" : 50, "kc" : -40, "kl0" : 0.6, "brain_sig" : None}
		BL_gastro = {"name" : "B_gastro.L", "debug" : False, "obj_1" : "obj_thigh.L", "obj_2" : "obj_shin_lower.L",\
			"anch_1" : [-0.053, 0, -0.77], "anch_2" : [0.09, 0, 0.14], "k" : 200, \
			"c" : 20, "kc" : -10, "kl0" : 1, "brain_sig" : 2}
		BR_gastro = {"name" : "B_gastro.R", "debug" : False, "obj_1" : "obj_thigh.R", "obj_2" : "obj_shin_lower.R",\
			"anch_1" : [-0.053, 0, -0.77], "anch_2" : [0.09, 0, 0.14], "k" : 200, \
			"c" : 20, "kc" : -10, "kl0" : 1, "brain_sig" : 2}
		self.back_leg_L_muscles = [BL_biceps, BL_triceps, BL_gastro]
		self.back_leg_R_muscles = [BR_biceps, BR_triceps, BR_gastro]

		## Front Legs
		FL_biceps = {"name" : "F_biceps.L", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_upper_arm.L",\
			"anch_1" : [-0.93, -1, 0.48], "anch_2" : [-0.01, 0, 0.33], "k" : 400, \
			"c" : 40, "kc" : -7, "kl0" : 1, "brain_sig" : 1}
		FR_biceps = {"name" : "F_biceps.R", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_upper_arm.R",\
			"anch_1" :  [-0.93, 1, 0.48], "anch_2" : [-0.01, 0, 0.33], "k" : 400, \
			"c" : 40, "kc" : -7, "kl0" : 1, "brain_sig" : 1}
		FL_triceps = {"name" : "F_triceps.L", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_upper_arm.L",\
			"anch_1" : [-0.61, -1, 0.5], "anch_2" : [0.13, 0, 0.978], "k" : 1000, \
			"c" : 100, "kc" : 30, "kl0" : 0.4, "brain_sig" : None}
		FR_triceps = {"name" : "F_triceps.R", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_upper_arm.R",\
			"anch_1" :[-0.61, 1, 0.5], "anch_2" : [0.13, 0, 0.978], "k" : 1000, \
			"c" : 100, "kc" : 30, "kl0" : 0.4, "brain_sig" : None}
		FL_gastro = {"name" : "F_gastro.L", "debug" : False, "obj_1" : "obj_upper_arm.L", "obj_2" : "obj_wrist.L",\
			"anch_1" : [0.175, 0, 0.752], "anch_2" : [0.085, 0, 0], "k" : 10, \
			"c" : 2, "kc" : 0, "kl0" : 1, "brain_sig" : None}
		FR_gastro = {"name" : "F_gastro.R", "debug" : False, "obj_1" : "obj_upper_arm.R", "obj_2" : "obj_wrist.R",\
			"anch_1" : [0.175, 0, 0.752], "anch_2" : [0.085, 0, 0], "k" : 10, \
			"c" : 2, "kc" : 0, "kl0" : 1, "brain_sig" : None}
		self.front_leg_L_muscles = [FL_biceps, FL_triceps, FL_gastro]
		self.front_leg_R_muscles = [FR_biceps, FR_triceps, FR_gastro]

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

		vert1_u = {"name" : "muscle_vert1_up", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_vert.1",\
			"anch_1" :  [-0.186, 0, 0.93], "anch_2" : [-0.01, 0, 0.1], "k" : 4000, \
			"c" : 100, "kc" : 0, "kl0" : 0.8}
		vert1_d = {"name" : "muscle_vert1_down", "debug" : False, "obj_1" : "obj_body", "obj_2" : "obj_vert.1",\
			"anch_1" :  [-0.167, 0, 0.65], "anch_2" : [-0.01, 0, -0.1], "k" : 2000, \
			"c" : 100, "kc" : 0, "kl0" : 0.8}

		vert2_u = {"name" : "muscle_vert2_up", "debug" : False, "obj_1" : "obj_vert.1", "obj_2" : "obj_vert.2",\
			"anch_1" :  [0.01, 0, 0.1], "anch_2" : [-0.01, 0, 0.1], "k" : 2000, \
			"c" : 100, "kc" : 0, "kl0" : 0.8}
		vert2_d = {"name" : "muscle_vert2_down", "debug" : False, "obj_1" :"obj_vert.1", "obj_2" : "obj_vert.2",\
			"anch_1" :  [0.01, 0, -0.1], "anch_2" : [-0.01, 0, -0.1], "k" : 2000, \
			"c" : 100, "kc" : 0, "kl0" : 0.8}

		vert3_u = {"name" : "muscle_vert3_up", "debug" : False, "obj_1" : "obj_vert.2", "obj_2" : "obj_vert.3",\
			"anch_1" :  [0.01, 0, 0.1], "anch_2" : [-0.01, 0, 0.1], "k" : 2000, \
			"c" : 100, "kc" : 0, "kl0" : 0.8}
		vert3_d = {"name" : "muscle_vert3_down", "debug" : False, "obj_1" :"obj_vert.2", "obj_2" : "obj_vert.3",\
			"anch_1" :  [0.01, 0, -0.1], "anch_2" : [-0.01, 0, -0.1], "k" : 2000, \
			"c" : 100, "kc" : 0, "kl0" : 0.8}

		vert4_u = {"name" : "muscle_vert4_up", "debug" : False, "obj_1" : "obj_vert.3", "obj_2" : "obj_vert.4",\
			"anch_1" :  [0.01, 0, 0.1], "anch_2" : [-0.01, 0, 0.1], "k" : 2000, \
			"c" : 100, "kc" : 0, "kl0" : 0.8}
		vert4_d = {"name" : "muscle_vert4_down", "debug" : False, "obj_1" :"obj_vert.3", "obj_2" : "obj_vert.4",\
			"anch_1" :  [0.01, 0, -0.1], "anch_2" : [-0.01, 0, -0.1], "k" : 2000, \
			"c" : 100, "kc" : 0, "kl0" : 0.8}

		vert5_u = {"name" : "muscle_vert5_up", "debug" : False, "obj_1" : "obj_vert.4", "obj_2" : "obj_vert.5",\
			"anch_1" :  [0.01, 0, 0.1], "anch_2" : [-0.01, 0, 0.1], "k" : 2000, \
			"c" : 100, "kc" : 0, "kl0" : 0.8}
		vert5_d = {"name" : "muscle_vert5_down", "debug" : False, "obj_1" :"obj_vert.4", "obj_2" : "obj_vert.5",\
			"anch_1" :  [0.01, 0, -0.1], "anch_2" : [-0.01, 0, -0.1], "k" : 2000, \
			"c" : 100, "kc" : 0, "kl0" : 0.8}

		vert6_u = {"name" : "muscle_vert6_up", "debug" : False, "obj_1" : "obj_vert.5", "obj_2" : "obj_body.B",\
			"anch_1" :  [0.01, 0, 0.1], "anch_2" : [0.425, 0, 0.93], "k" : 2000, \
			"c" : 100, "kc" : 0, "kl0" : 0.8}
		vert6_d = {"name" : "muscle_vert6_down", "debug" : False, "obj_1" :"obj_vert.5", "obj_2" : "obj_body.B",\
			"anch_1" :  [0.01, 0, -0.1], "anch_2" : [0.425, 0, 0.65], "k" : 2000, \
			"c" : 100, "kc" : 0, "kl0" : 0.8}
		abdos = {"name" : "muscle_abdos", "debug" : False, "obj_1" :"obj_body", "obj_2" : "obj_body.B",\
			"anch_1" :  [-0.1977, 0, -0.61], "anch_2" : [0.45, 0, -0.61], "k" : 2000, \
			"c" : 200, "kc" : 0, "kl0" : 0.85}
		body_muscles = [neck1, neck2, vert1_u, vert1_d, vert2_u, vert2_d, vert3_u, vert3_d, vert4_u, vert4_d, \
			vert5_u, vert5_d, vert6_u, vert6_d, abdos]
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