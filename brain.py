import numpy as np

class Matsuoka:
	"This class represents the mouse brain and its current behaviour in the control process"

	def __init__(self,numOsc=4,h=1e-3,tau=1e-2,T=1e-1,a=10.5,b=20.5,c=0.08,aa=3,time_interval=1e-3):
		"Class initialization"
		
		self.h = h
		self.tau = tau
		self.T = T
		self.a = a
		self.b = b
		self.c = c
		self.A = aa*np.array([[0,-1,-1,1],[-1,0,1,-1],[-1,1,0,-1],[1,-1,-1,0]])
		self.numOsc = numOsc
		self.x = np.zeros((self.numOsc,1))+np.array([[0.1],[0.1],[0.2],[0.2]])
		self.v = np.zeros((self.numOsc,1))+np.array([[0.1],[0.1],[0.2],[0.2]])
		self.y = np.zeros((self.numOsc,1))+np.array([[0.1],[0.1],[0.2],[0.2]])
		self.g = lambda x:max(0.,x)
		self.Record = 0
		self.time = []
		self.iter_num = int(time_interval/h)
		for i in range(self.numOsc):
			exec('self.yRec{0:d}=[]'.format(i))

	def update_sig(self,Record=0):
		"Update control signals and forces"
		
		self.Record = Record
		for i in range(self.iter_num):
			self.x += self.h * (- self.x + self.c - self.A.dot(self.y) - self.b * self.v) / self.tau
			self.v += self.h * (- self.v + self.y) / self.T
			for i in range(self.numOsc):
				self.y[i] = self.g(self.x[i])
				
		for i in range(self.numOsc):
			if Record == 1:
				exec('self.yRec{0:d}.append(float(self.y[{0:d}]))'.format(i))


class Brain:
	"This class represents the mouse brain and its current behaviour in the control process"

	def __init__(self, scene_, controller_, name_="dull_brain"):
		"Class initialization"
		
		self.n_iter = 0
		self.scene = scene_
		self.controller = controller_
		self.name = name_
		self.oscillator = Matsuoka()

	def update_sig(self):
		"Update control signals and forces"
		
		self.oscillator.update_sig()
		self.n_iter += 1
		print("[DEBUG] Brain " + self.name + " iteration: " + str(self.n_iter))