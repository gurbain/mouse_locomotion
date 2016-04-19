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

import logging
import numpy as np


class Matsuoka:
    """This class represents the mouse brain and its current behaviour in the control process"""

    def __init__(self, scene_, config_):
        """Class initialization"""

        self.scene = scene_
        self.config = config_
        self.h = self.config.brain["h"]
        self.tau = self.config.brain["tau"]
        self.T = self.config.brain["T"]
        self.a = self.config.brain["a"]
        self.b = self.config.brain["b"]
        self.c = self.config.brain["c"]
        self.aa = self.config.brain["aa"]
        self.A = self.aa * np.array([[0, -1, -1, 1], [-1, 0, 1, -1], [-1, 1, 0, -1], [1, -1, -1, 0]])
        self.n_osc = self.config.brain["n_osc"]
        self.x = np.zeros((self.n_osc, 1)) + np.array([[0.1], [0.1], [0.2], [0.2]])
        self.v = np.zeros((self.n_osc, 1)) + np.array([[0.1], [0.1], [0.2], [0.2]])
        self.y = np.zeros((self.n_osc, 1)) + np.array([[0.1], [0.1], [0.2], [0.2]])
        self.g = lambda x: max(0., x)
        self.Record = 0
        self.time = []
        self.time_interval = self.config.brain["time_interval"]
        self.iter_num = int(self.time_interval / self.h)

    def update(self):
        """Update control signals and forces"""

        for i in range(self.iter_num):
            self.x += self.h * (- self.x + self.c - self.A.dot(self.y) - self.b * self.v) / self.tau
            self.v += self.h * (- self.v + self.y) / self.T
            for i in range(self.n_osc):
                self.y[i] = self.g(self.x[i])


class Brain:
    """This class represents the mouse brain and its current behaviour in the control process"""

    def __init__(self, scene_, config_):
        """Class initialization"""

        self.n_iter = 0
        self.scene = scene_
        self.config = config_
        self.logger = config_.logger
        self.name = self.config.brain["name"]
        self.n_osc = self.config.brain["n_osc"]
        self.osc = Matsuoka(self.scene, self.config)
        self.state = np.zeros((self.n_osc, 1))

    def update(self):
        """Update control signals and forces"""

        # Write control signals into y
        self.osc.update()
        self.state = self.osc.y

        self.n_iter += 1
        self.logger.debug("Brain " + self.name + " iteration " + str(self.n_iter) + ": State vector: " +
            str(np.transpose(self.state)))
