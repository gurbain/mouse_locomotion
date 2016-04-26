##
# Mouse Locomotion Simulation
#
# Human Brain Project SP10
# 
# This project provides the user with a framework based on Blender allowing:
#  - Edition of a 3D model
#  - Edition of a physical controller model (torque-based or muscle-based)
#  - Edition of a brain controller model (oscillator-based or neural network-based)
#  - Simulation of the model
#  - Optimization of the parameters in distributed cloud simulations
# 
# File created by: Gabriel Urbain <gabriel.urbain@ugent.be>. April 2016
# Modified by: Dimitri Rodarie
##


class Result:
    """This class is called at the end of a Blender simulation. It collects the simulation results from Blender, and from the
    different classes of this project. It also provides method to save, display and load the results (usefull inside an
    optimization algorithm). It takes a Config class as a initialization argument to determine which parameters shall be saved"""

    def __init__(self, scene_, config_):

    	return

  	def save(self):

  		return

  	def load(self, file_):

  		return

  	def __str__(self):
  		
        return "foo"