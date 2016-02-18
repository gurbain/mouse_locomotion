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

	def update_mvt(self):
		"Update control signals and forces"
		
		self.n_iter += 1
		print("[DEBUG] Leg iteration: " + str(self.n_iter))


class Backleg(Leg):
	"This class represents a generic backleg and its current behaviour in the control process"

	def __init__(self, scene_, controller_, orien_):
		"Class initialization"
		
		super().__init__(scene_, controller_)
		self.orien = orien_

		# Bones objects
		self.tarsus =  self.scene.objects["obj_shin_lower." + self.orien]
		self.tibia =  self.scene.objects["obj_shin." + self.orien]
		self.femur =  self.scene.objects["obj_shin_lower." + self.orien]

		# Muscle LOCAL anchors position
		self.biceps_femur_anch = vec((0, 0, 0))
		self.biceps_tibia_anch = vec((0, 0, 0))
		self.gastro_tibia_anch = vec((0, 0, 0))
		self.gastro_tarsus_anch = vec((0, 0, 0))

		# Muscles
		self.biceps = Muscle(self.scene, self.controller, self.femur, self.tibia, \
			self.biceps_femur_anch, self.biceps_tibia_anch, "biceps")
		self.gastrocnemius =  Muscle(self.scene, self.controller, self.tibia, self.tarsus, \
			self.gastro_tibia_anch, self.gastro_tarsus_anch, "gastrocnemius")

	def update_mvt(self, ctrl_sig_):
		"Update control signals and forces"
		
		if ctrl_sig_ != None:
			self.biceps.l0 = ctrl_sig_
			self.triceps.l0 = ctrl_sig_

		self.biceps.update()
		self.gastrocnemius.update()
		
		self.n_iter += 1
		print("[DEBUG] Backleg iteration: " + str(self.n_iter))


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
			self.biceps_humerus_anch, self.biceps_radius_anch, "biceps")
		self.triceps =  Muscle(self.scene, self.controller, self.radius, self.carpus, \
			self.triceps_radius_anch, self.triceps_carpus_anch, "triceps")

	def update_mvt(self, ctrl_sig_=None):
		"Update control signals and forces"
		
		if ctrl_sig_ != None:
			self.biceps.l0 = ctrl_sig_
			self.triceps.l0 = ctrl_sig_

		self.biceps.update()
		self.triceps.update()

		self.n_iter += 1
		print("[DEBUG] Foreleg iteration: " + str(self.n_iter))


class Mouse:
	"This class represents the mouse body and its current behaviour in the control process"

	def __init__(self, scene_, controller_):
		"Class initialization"
		
		self.n_iter = 0
		self.scene = scene_
		self.controller = controller_
		self.l_fo_leg = Foreleg(scene_, controller_, "L")
		self.r_fo_leg = Foreleg(scene_, controller_, "R")
		self.l_ba_leg = Backleg(scene_, controller_, "L")
		self.r_ba_leg = Backleg(scene_, controller_, "R")
		self.brain = Brain(scene_, controller_)

	def update_mvt(self):
		"Update control signals and forces"
		
		self.brain.update_sig() # iterate for new control signal
		self.l_fo_leg.update_mvt(0) # give the control signal
		self.r_fo_leg.update_mvt(0) # give the control signal
		self.l_ba_leg.update_mvt(0) # give the control signal
		self.r_ba_leg.update_mvt(0) # give the control signal
		
		self.n_iter += 1
		print("[DEBUG] Mouse iteration: " + str(self.n_iter))