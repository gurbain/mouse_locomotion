from brain import Brain

class Muscle:
	"This class implements Hill Model for muscle force "

	def __init__(self, scene_, controller_, ce_=0, pee_=0, see_=0, lce_=0, lsee_=0, lm_=0, fm_=0):
		"Class initialization"
		
		self.n_iter = 0
		self.scene = scene_
		self.controller = controller_
		self.ce = ce_
		self.pee = pee_
		self.see = see_
		self.lce = lce_
		self.lsee = lsee_
		self.lm = lm_
		self.fm = fm_
		
	def update_mvt(self, ctrl_sig):
		"Update control signals and forces"
		
		# Here, we update the muscle forces given geometry and control signal
		self.n_iter += 1
		print("Bone iteration: " + str(self.n_iter))


class Bone:
	"This class represents a generic bone and the forces that shall be applied on it"

	def __init__(self, scene_, controller_, name_="obj_unknown"):
		"Class initialization"
		
		self.n_iter = 0
		self.scene = scene_
		self.controller = controller_
		self.name = name_
		
	def update_mvt(self, force, torque):
		"Update control signals and forces"
		
		# Here, we update obj_name with forces and torque applied in CG
		self.n_iter += 1
		print("Bone iteration: " + str(self.n_iter))


class Leg:
	"This class represents a generic leg and its current behaviour in the control process"

	def __init__(self, scene_, controller_):
		"Class initialization"
		
		self.n_iter = 0
		self.scene = scene_
		self.controller = controller_

	def update_mvt(self):
		"Update control signals and forces"
		
		self.n_iter += 1
		print("Leg iteration: " + str(self.n_iter))


class Backleg(Leg):
	"This class represents a generic backleg and its current behaviour in the control process"

	def __init__(self, scene_, controller_):
		"Class initialization"
		
		self.tarsus =  Bone(scene_, controller_)
		self.tibia =  Bone(scene_, controller_)
		self.femur =  Bone(scene_, controller_)
		self.biceps =  Muscle(scene_, controller_)
		self.gastrocnemius =  Muscle(scene_, controller_)
		self.biceps_r_anch = [0, 0, 0]
		self.biceps_l_anch = [0, 0, 0]
		self.gastro_r_anch = [0, 0, 0]
		self.gastro_l_anch = [0, 0, 0]
		
		super().__init__(scene_, controller_)

	def update_mvt(self, ctrl_sig):
		"Update control signals and forces"
		
		# Here, we shall compute new values for the each muscle given control signal and muscle geometry
		# Here, we shall apply new forces to each bone CGs
		
		self.n_iter += 1
		print("Backleg iteration: " + str(self.n_iter))


class Foreleg(Leg):
	"This class represents a generic foreleg and its current behaviour in the control process"

	def __init__(self, scene_, controller_):
		"Class initialization"
		
		self.humerus =  Bone(scene_, controller_)
		self.radius =  Bone(scene_, controller_)
		self.carpus =  Bone(scene_, controller_)
		self.biceps =  Muscle(scene_, controller_)
		self.triceps =  Muscle(scene_, controller_)
		self.biceps_r_anch = [0, 0, 0]
		self.biceps_l_anch = [0, 0, 0]
		self.triceps_r_anch = [0, 0, 0]
		self.triceps_l_anch = [0, 0, 0]
		
		super().__init__(scene_, controller_)

	def update_mvt(self, ctrl_sig):
		"Update control signals and forces"
		
		# Here, we shall compute new values for the each muscle given control signal and muscle geometry
		# Here, we shall apply new forces to each bone CGs
		
		self.n_iter += 1
		print("Foreleg iteration: " + str(self.n_iter))


class Mouse:
	"This class represents the mouse body and its current behaviour in the control process"

	def __init__(self, scene_, controller_):
		"Class initialization"
		
		self.n_iter = 0
		self.scene = scene_
		self.controller = controller_
		self.l_fo_leg = Foreleg(scene_, controller_)
		self.r_fo_leg = Foreleg(scene_, controller_)
		self.l_ba_leg = Backleg(scene_, controller_)
		self.r_ba_leg = Backleg(scene_, controller_)
		self.brain = Brain(scene_, controller_)

	def update_mvt(self):
		"Update control signals and forces"
		
		self.brain.update_sig() # iterate for new control signal
		self.l_fo_leg.update_mvt(0) # give the control signal
		self.r_fo_leg.update_mvt(0) # give the control signal
		self.l_ba_leg.update_mvt(0) # give the control signal
		self.r_ba_leg.update_mvt(0) # give the control signal
		
		self.n_iter += 1
		print("Mouse iteration: " + str(self.n_iter))


