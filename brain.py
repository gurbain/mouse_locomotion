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

import numpy as np

class Matsuoka:
	"This class represents the mouse brain and its current behaviour in the control process"

	def __init__(self,numOsc=4, h=1e-3, tau=1e-2, T=5e-2, a=10.5, b=20.5, c=0.08, aa=3, time_interval=1e-3):
		"Class initialization" 
		
		self.h = h
		self.tau = tau
		self.T = T
		self.a = a
		self.b = b
		self.c = c
		self.A = aa*np.array([[0,-1,-1,1],[-1,0,1,-1],[-1,1,0,-1],[1,-1,-1,0]])
		self.numOsc = numOsc
		self.x = np.zeros((self.numOsc,1)) + np.array([[0.1],[0.1],[0.2],[0.2]])
		self.v = np.zeros((self.numOsc,1)) + np.array([[0.1],[0.1],[0.2],[0.2]])
		self.y = np.zeros((self.numOsc,1)) + np.array([[0.1],[0.1],[0.2],[0.2]])
		self.g = lambda x:max(0.,x)
		self.Record = 0
		self.time = []
		self.iter_num = int(time_interval / h)

	def update(self):
		"Update control signals and forces"
		
		for i in range(self.iter_num):
			self.x += self.h * (- self.x + self.c - self.A.dot(self.y) - self.b * self.v) / self.tau
			self.v += self.h * (- self.v + self.y) / self.T
			for i in range(self.numOsc):
				self.y[i] = self.g(self.x[i])


class Brain:
	"This class represents the mouse brain and its current behaviour in the control process"

	def __init__(self, scene_, controller_, n_osc_=4, name_="dull_brain"):
		"Class initialization"
		
		self.n_iter = 0
		self.scene = scene_
		self.controller = controller_
		self.name = name_
		self.n_osc = n_osc_
		self.osc = Matsuoka(self.n_osc)
		self.state = np.zeros((self.n_osc, 1))

	def update(self):
		"Update control signals and forces"
		
		# Write control signals into y
		self.osc.update()
		self.state = self.osc.y

		self.n_iter += 1
		print("[DEBUG] Brain " + self.name + " iteration " + str(self.n_iter) + ": State vector: " + \
			str(self.state))