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
from muscle import DampedSpringReducedTorqueMuscle


class Leg:
    """This class represents a generic leg and its current behaviour in the control process"""

    def __init__(self, scene_, config_):
        """Class initialization"""

        self.n_iter = 0
        self.scene = scene_
        self.config = config_
        self.debug = self.config.debug

    def update(self, ctrl_sig_):
        """Update control signals and forces"""

        self.n_iter += 1
        if self.debug:
            print("[DEBUG] Leg iteration: " + str(self.n_iter))


class Backleg(Leg):
    """This class represents a generic backleg and its current behaviour in the control process"""

    def __init__(self, scene_, config_, orien_):
        """Class initialization"""

        Leg.__init__(self, scene_, config_)
        self.orien = orien_

        # Create the muscles objects following config
        self.muscles = []
        self.brain_sig = []
        if self.orien == "L":
            for muscle_config in self.config.back_leg_L_muscles:
                self.muscles.append(DampedSpringReducedTorqueMuscle(self.scene, muscle_config))
                self.brain_sig.append(muscle_config["brain_sig"])
        else:  # R
            for muscle_config in self.config.back_leg_R_muscles:
                self.muscles.append(DampedSpringReducedTorqueMuscle(self.scene, muscle_config))
                self.brain_sig.append(muscle_config["brain_sig"])

    def update(self, ctrl_sig_):
        """Update control signals and forces"""

        for i in range(len(self.muscles)):
            if self.brain_sig[i] is None:
                ctrl_sig = 0
            else:
                ctrl_sig = ctrl_sig_[self.brain_sig[i]]
            self.muscles[i].update(ctrl_sig=ctrl_sig)

        self.n_iter += 1
        if self.debug:
            print("[DEBUG] Backleg " + self.orien + " iteration " + str(self.n_iter) + ": Control signal = " +
                  str(self.brain_sig))


class Foreleg(Leg):
    """This class represents a generic foreleg and its current behaviour in the control process"""

    def __init__(self, scene_, config_, orien_):
        """Class initialization"""

        Leg.__init__(self, scene_, config_)
        self.orien = orien_

        # Create the muscles objects following config
        self.muscles = []
        self.brain_sig = []
        if self.orien == "L":
            for muscle_config in self.config.front_leg_L_muscles:
                self.muscles.append(DampedSpringReducedTorqueMuscle(self.scene, muscle_config))
                self.brain_sig.append(muscle_config["brain_sig"])
        else:  # R
            for muscle_config in self.config.front_leg_R_muscles:
                self.muscles.append(DampedSpringReducedTorqueMuscle(self.scene, muscle_config))
                self.brain_sig.append(muscle_config["brain_sig"])

    def update(self, ctrl_sig_):
        """Update control signals and forces"""

        for i in range(len(self.muscles)):
            if self.brain_sig[i] is None:
                ctrl_sig = 0
            else:
                ctrl_sig = ctrl_sig_[self.brain_sig[i]]
            self.muscles[i].update(ctrl_sig=ctrl_sig)

        self.n_iter += 1
        if self.debug:
            print("[DEBUG] Foreleg " + self.orien + " iteration " + str(self.n_iter) + ": Control signal = " +
                  str(self.brain_sig))


class Body:
    """This class represents the mouse body and its current behaviour in the control process"""

    def __init__(self, scene_, config_):
        """Class initialization"""

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
        self.muscles = []
        for muscle_config in self.config.body["muscles"]:
            self.muscles.append(DampedSpringReducedTorqueMuscle(self.scene, muscle_config))

    def update(self):
        """Update control signals and forces"""

        self.brain.update()

        for muscle in self.muscles:
            muscle.update()

        ctrl_sig = [float(self.brain.state[0]), float(self.brain.state[1]), float(self.brain.state[2]),
                    float(self.brain.state[3])]
        # 2 0 /
        # 2 0 /
        # 0 1 /
        # 0 1 /
        self.l_ba_leg.update(ctrl_sig)
        self.r_ba_leg.update(ctrl_sig)
        self.l_fo_leg.update(ctrl_sig)
        self.r_fo_leg.update(ctrl_sig)

        self.n_iter += 1
        if self.debug:
            print("[DEBUG] Body " + self.name + " iteration " + str(self.n_iter))
