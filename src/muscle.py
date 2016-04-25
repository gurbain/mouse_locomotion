# coding=utf-8
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
import math
from mathutils import Vector as vec

import bge


class Muscle:
    def __init__(self, scene_, params_):
        """Class initialization"""
        self.n_iter = 0
        self.scene = scene_
        self.params = params_
        self.name = self.params["name"]
        self.active = True

        self.logger = logging.getLogger(params_["logger"])

        # Check if onject exist
        if not self.params["obj_1"] in self.scene.objects:
            self.logger.error("Muscle " + self.name + " deactivated: first extremity object doesn't exit." +
                  " Check your configuration file!")
            self.active = False
        else:
            self.obj1 = self.scene.objects[self.params["obj_1"]]
        if not self.params["obj_2"] in self.scene.objects:
            self.logger.error("Muscle " + self.name + " deactivated: second extremity object doesn't exit." +
                " Check your configuration file!")
            self.active = False
        else:
            self.obj2 = self.scene.objects[self.params["obj_2"]]

        # Points of application in local coordinates
        if self.params["anch_1"] is None:
            self.logger.error("You have not defined the first application point of muscle " + self.name +
                  "! Center is taken by default. This may results in erroneous simulation")
            self.params["anch_1"] = [0.0, 0.0, 0.0]
        if self.params["anch_2"] is None:
            self.logger.error("You have not defined the second application point of muscle " + self.name +
                  "! Center is taken by default. This may results in erroneous simulation")
            self.params["anch_2"] = [0.0, 0.0, 0.0]
        self.app_point_1 = vec((self.params["anch_1"]))
        self.app_point_2 = vec((self.params["anch_2"]))

        if self.active:
            self.app_point_1_world = self.obj1.worldTransform * self.app_point_1  # global coordinates of app point 1 in m
            self.app_point_2_world = self.obj2.worldTransform * self.app_point_2  # global coordinates of app point 2 in m

    def get_power(self):
        """Return the power developped by the muscle on the two extremity objects"""

        return 0

    def draw_muscle(self, color_=[256, 0, 0]):
        """Draw a line to represent the muscle in the blender simulation"""

        bge.render.drawLine(self.app_point_1_world, self.app_point_2_world, color_)

    def update(self, **kwargs):
        # Here, we update the muscle forces given geometry and control signal
        self.n_iter += 1


class HillMuscle(Muscle):
    """This class implements Hill Model for muscle force """

    def __init__(self, scene_, params_):
        """Class initialization. Parameters can be found in D.F.B. Haeufle, M. Günther, A. Bayer, S. Schmitt (2014) \
        Hill-type muscle model with serial damping and eccentric force-velocity relation. Journal of Biomechanics"""

        Muscle.__init__(self, scene_, params_)

        # Contractile Element (CE)
        self.CE_F_max = 1420  # F_max in [N] for Extensor (Kistemaker et al., 2006)
        self.CE_l_CEopt = 0.092  # optimal length of CE in [m] for Extensor (Kistemaker et al., 2006)
        self.CE_DeltaW_limb_des = 0.35  # width of normalized bell curve in descending branch (Moerl et al., 2012)
        self.CE_DeltaW_limb_asc = 0.35  # width of normalized bell curve in ascending branch (Moerl et al., 2012)
        self.CE_v_CElimb_des = 1.5  # exponent for descending branch (Moerl et al., 2012)
        self.CE_v_CElimb_asc = 3.0  # exponent for ascending branch (Moerl et al., 2012)
        self.CE_A_rel0 = 0.25  # parameter for contraction dynamics: maximum value of A_rel (Guenther, 1997, S. 82)
        self.CE_B_rel0 = 2.25  # parameter for contraction dynmacis: maximum value of B_rel (Guenther, 1997, S. 82)
        # eccentric force-velocity relation:
        self.CE_S_eccentric = 2  # relation between F(v) slopes at v_CE=0 (van Soest & Bobbert, 1993)
        self.CE_F_eccentric = 1.5  # factor by which the force can exceed F_isom for large eccentric velocities (van Soest & Bobbert, 1993)

        # Parallel Elastic Element (PEE)
        self.PEE_L_PEE0 = 0.9  # rest length of PEE normalized to optimal lenght of CE (Guenther et al., 2007)
        self.PEE_l_PEE0 = self.PEE_L_PEE0 * self.CE_l_CEopt  # rest length of PEE (Guenther et al., 2007)
        self.PEE_v_PEE = 2.5  # exponent of F_PEE (Moerl et al., 2012)
        self.PEE_F_PEE = 2.0  # force of PEE if l_CE is stretched to deltaWlimb_des (Moerl et al., 2012)
        self.PEE_K_PEE = self.PEE_F_PEE * (
            self.CE_F_max / (self.CE_l_CEopt * (self.CE_DeltaW_limb_des + 1 - self.PEE_L_PEE0)) ** self.PEE_v_PEE)
        # factor of non-linearity in F_PEE (Guenther et al., 2007)

        # Serial Damping Element (SDE)
        self.SDE_D_SE = 0.3  # xxx dimensionless factor to scale d_SEmax (Moerl et al., 2012)
        self.SDE_R_SE = 0.01  # minimum value of d_SE normalised to d_SEmax (Moerl et al., 2012)
        self.SDE_d_SEmax = self.SDE_D_SE * (self.CE_F_max * self.CE_A_rel0) / (self.CE_l_CEopt * self.CE_B_rel0)
        # maximum value in d_SE in [Ns/m] (Moerl et al., 2012)

        # Serial Elastic Element (SEE)
        self.SEE_l_SEE0 = 0.172  # rest length of SEE in [m] (Kistemaker et al., 2006)
        self.SEE_DeltaU_SEEnll = 0.0425  # relativ stretch at non-linear linear transition (Moerl et al., 2012)
        self.SEE_DeltaU_SEEl = 0.017  # relativ additional stretch in the linear part providing a force increase of deltaF_SEE0 (Moerl, 2012)
        self.SEE_DeltaF_SEE0 = 568  # both force at the transition and force increase in the linear part in [N] (~ 40# of the maximal isometric muscle force)

        self.SEE_l_SEEnll = (1 + self.SEE_DeltaU_SEEnll) * self.SEE_l_SEE0
        self.SEE_v_SEE = self.SEE_DeltaU_SEEnll / self.SEE_DeltaU_SEEl
        self.SEE_KSEEnl = self.SEE_DeltaF_SEE0 / (self.SEE_DeltaU_SEEnll * self.SEE_l_SEE0) ** self.SEE_v_SEE
        self.SEE_KSEEl = self.SEE_DeltaF_SEE0 / (self.SEE_DeltaU_SEEl * self.SEE_l_SEE0)

    def update(self, **kwargs):
        """Computations are based on D.F.B. Haeufle, M. Günther, A. Bayer, S. Schmitt (2014) \
        Hill-type muscle model with serial damping and eccentric force-velocity relation. Journal of Biomechanics"""
        if "l_CE" in kwargs:
            l_CE = kwargs["l_CE"]
        else:
            self.logger.error("Muscle " + self.name + " deactivated: l_CE isn't defined." +
                  " Check your configuration file!")
            self.active = False
            l_CE = 0

        if "l_MTC" in kwargs:
            l_MTC = kwargs["l_MTC"]
        else:
            self.logger.error("Muscle " + self.name + " deactivated: l_MTC isn't defined." +
                  " Check your configuration file!")
            self.active = False
            l_MTC = 0

        if "dot_l_MTC" in kwargs:
            dot_l_MTC = kwargs["dot_l_MTC"]
        else:
            self.logger.error("Muscle " + self.name + " deactivated: dot_l_MTC isn't defined." +
                  " Check your configuration file!")
            self.active = False
            dot_l_MTC = 0

        if "q" in kwargs:
            q = kwargs["q"]
        else:
            self.logger.error("Muscle " + self.name + " deactivated: q isn't defined." +
                  " Check your configuration file!")
            self.active = False
            q = 0

        if self.active:
            # Isometric force (Force length relation)
            if l_CE >= self.CE_l_CEopt:  # descending branch
                F_isom = math.exp(
                    -(abs(((l_CE / self.CE_l_CEopt) - 1) / self.CE_DeltaW_limb_des)) ** self.CE_v_CElimb_des)
            else:  # ascending branch
                F_isom = math.exp(
                    -(abs(((l_CE / self.CE_l_CEopt) - 1) / self.CE_DeltaW_limb_asc)) ** self.CE_v_CElimb_asc)

            # Force of the parallel elastic element PEE
            if l_CE >= self.PEE_l_PEE0:
                F_PEE = self.PEE_K_PEE * (l_CE - self.PEE_l_PEE0) ** self.PEE_v_PEE
            else:  # shorter than slack length
                F_PEE = 0

            # Force of the serial elastic element SEE
            l_SEE = abs(l_MTC - l_CE)  # SEE length
            if (l_SEE > self.SEE_l_SEE0) and (l_SEE < self.SEE_l_SEEnll):  # non-linear part
                F_SEE = self.SEE_KSEEnl * ((l_SEE - self.SEE_l_SEE0) ** self.SEE_v_SEE)
            elif l_SEE >= self.SEE_l_SEEnll:  # linear part
                F_SEE = self.SEE_DeltaF_SEE0 + self.SEE_KSEEl * (l_SEE - self.SEE_l_SEEnll)
            else:  # salck length
                F_SEE = 0

            # Hill Parameters concentric contraction
            if l_CE < self.CE_l_CEopt:
                A_rel = 1
            else:
                A_rel = F_isom

            A_rel = A_rel * self.CE_A_rel0 * 1 / 4 * (1 + 3 * q)
            B_rel = self.CE_B_rel0 * 1 * 1 / 7 * (3 + 4 * q)

            # calculate CE contraction velocity
            D0 = self.CE_l_CEopt * B_rel * self.SDE_d_SEmax * (
                self.SDE_R_SE + (1 - self.SDE_R_SE) * (q * F_isom + F_PEE / self.CE_F_max))
            C2 = self.SDE_d_SEmax * (self.SDE_R_SE - (A_rel - F_PEE / self.CE_F_max) * (1 - self.SDE_R_SE))
            C1 = - C2 * dot_l_MTC - D0 - F_SEE + F_PEE - self.CE_F_max * A_rel
            C0 = D0 * dot_l_MTC + self.CE_l_CEopt * B_rel * (F_SEE - F_PEE - self.CE_F_max * q * F_isom)

            # solve the quadratic equation
            if (C1 ** 2 - 4 * C2 * C0) < 0:
                dot_l_CE = 0
            # warning('the quadratic equation in the muscle model would result in a complex solution to compensate, the CE contraction velocity was set to zero')
            else:
                dot_l_CE = (- C1 - math.sqrt(C1 ** 2 - 4 * C2 * C0)) / (2 * C2)

            # in case of an eccentric contraction:
            if dot_l_CE > 0:
                # calculate new Hill-parameters (asymptotes of the hyperbola)
                B_rel = (q * F_isom * (1 - self.CE_F_eccentric) / (q * F_isom + A_rel) * B_rel / self.CE_S_eccentric)
                A_rel = - self.CE_F_eccentric * q * F_isom

                # calculate CE eccentric velocity
                D0 = self.CE_l_CEopt * B_rel * self.SDE_d_SEmax * (
                    self.SDE_R_SE + (1 - self.SDE_R_SE) * (q * F_isom + F_PEE / self.CE_F_max))
                C2 = self.SDE_d_SEmax * (self.SDE_R_SE - (A_rel - F_PEE / self.CE_F_max) * (1 - self.SDE_R_SE))
                C1 = - C2 * dot_l_MTC - D0 - F_SEE + F_PEE - self.CE_F_max * A_rel
                C0 = D0 * dot_l_MTC + self.CE_l_CEopt * B_rel * (F_SEE - F_PEE - self.CE_F_max * q * F_isom)

                # solve the quadratic equation
                if (C1 ** 2 - 4 * C2 * C0) < 0:
                    dot_l_CE = 0
                # warning('the quadratic equation in the muscle model would result in a complex solution to compensate, the CE contraction velocity was set to zero')
                else:
                    dot_l_CE = (- C1 + math.sqrt(C1 ** 2 - 4 * C2 * C0)) / (
                        2 * C2)  # note that here +sqrt gives the correct solution

            # Contractile element force
            F_CE = self.CE_F_max * (((q * F_isom + A_rel) / (1 - dot_l_CE / (self.CE_l_CEopt * B_rel))) - A_rel)

            # Force of the serial damping element
            F_SDE = self.SDE_d_SEmax * ((1 - self.SDE_R_SE) * ((F_CE + F_PEE) / self.CE_F_max) + self.SDE_R_SE) * (
                dot_l_MTC - dot_l_CE)
            F_MTC = F_SEE + F_SDE

            return F_MTC


class DampedSpringMuscle(Muscle):
    """This class implements a simple muscle composed by a spring and a damping in parallel"""

    def __init__(self, scene_, params_):
        """Class initialization. Requires scene, controller as well as two object and the local point of application \
        of the spring forces"""
        Muscle.__init__(self, scene_, params_)

        # Model constants and variables
        self.k = self.params["k"]  # scalar in N/m??
        self.c = self.params["c"]  # scalar in N.s/m??
        self.k_cont = self.params["kc"]  # no dimension
        self.ctrl_sig = None
        if self.active:
            self.l = self.app_point_2_world - self.app_point_1_world  # global coordinate vector between app points in m
            self.v_1 = self.obj1.getVelocity(self.app_point_1) # vector in m/s??
            self.v_2 = self.obj2.getVelocity(self.app_point_2) # vector in m/s??
            v = self.v_2 - self.v_1 # vector in m/s??
            self.v_norm = v.dot(self.l.normalized()) * self.l.normalized()  # normal velocity vector in m/s??
            self.l0 = self.params["kl0"] * self.l.length  # scalar in m??
            self.l_cont = self.l0  # scalar in m??
            self.force = vec((0, 0, 0)) # vector in N??

    def get_power(self):
        """Return the time-step power developped by the muscle on the two extremity objects"""

        power = 0.0
        if self.ctrl_sig != 0.0:# and float((self.force * self.l.normalized())) < 0.0:
            power_1 = - self.force * self.v_1
            power_2 = self.force * self.v_2
            power = power_2 + power_1

            self.logger.debug("v_1 = " + str(self.v_1.length) + " m/s; v_2 = " + str(self.v_2.length) + \
                " m/s; F = " + str(self.force.length) + " N")
            self.logger.debug("power obj1 = " + str(power_1) + " ; power obj2 = " + str(power_2) + \
                " ; power tot = " + str(power))

        return power

    def update(self, **kwargs):
        """Update and apply forces on the objects connected to the spring. The spring can be controlled in length by \
        fixing manually l0"""

        if "ctrl_sig" in kwargs:
            self.ctrl_sig = kwargs["ctrl_sig"]
        else:
            self.ctrl_sig = None

        # If muscle has not been deactivated
        if self.active:

            # get control length
            if self.ctrl_sig is None:
                self.l_cont = self.l0  # by default, control length is the spring reference length
            else:
                self.l_cont = self.l0 * (1 + self.k_cont * self.ctrl_sig)

            # get length and velocity
            self.app_point_1_world = self.obj1.worldTransform * self.app_point_1
            self.app_point_2_world = self.obj2.worldTransform * self.app_point_2
            self.l = self.app_point_2_world - self.app_point_1_world

            # Damping must be in spring axis direction
            self.v_1 = self.obj1.getVelocity(self.app_point_1)
            self.v_2 = self.obj2.getVelocity(self.app_point_2)
            v = self.v_2 - self.v_1
            self.v_norm = v.dot(self.l.normalized()) * self.l.normalized()
            # print("l: " + str(self.l) + " norm: " + str(self.l.normalized()) + " v = " +  str(v) + "vdot" + str(v.dot(self.l.normalized())) +" vnorm: " + str(self.v_norm))

            # compute spring force
            force_s = - (self.k * (self.l.length - self.l_cont)) * self.l.normalized()

            # compute damping force
            force_d = - self.c * self.v_norm

            # compute total force
            self.force = force_s + force_d
            impulse = self.force / bge.logic.getLogicTicRate()

            # apply impusle on an object point only in traction
            f_type = "Push"
            if float((self.force * self.l.normalized())) < 0.0:
                f_type = "Pull"
                self.obj1.applyImpulse(self.app_point_1_world, - impulse)
                self.obj2.applyImpulse(self.app_point_2_world, impulse)

            # DEBUG data
            self.draw_muscle()
            self.n_iter += 1

            #self.logger.debug("Muscle " + self.name + ":" + str(self.n_iter) + ": Ft = " + str(
            #    self.force) + " - " + str(self.force * self.l.normalized()) + "N")
            #self.logger.debug("  Type = " + f_type)
            #self.logger.debug("  Fs = " + str(force_s) + " ;  Fd = " + str(force_d))
            #self.logger.debug("  l = " + str(self.l) + " ; l0 = " + str(self.l0))
            #self.logger.debug("  L P1 = " + str(self.app_point_1) + " ; L P2 = " + str(self.app_point_2))
            #self.logger.debug("  G P1 = " + str(self.app_point_1_world) + " ; G P2 = " + str(self.app_point_2_world))

        else:
            self.logger.warning("Muscle " + self.name + " has been deactivated.")




class DampedSpringReducedTorqueMuscle(Muscle):
    """This class implements a simple muscle composed by a spring and a damper in parallel.\
    Forces and torques applied in the center of gravity are computed separately and a reduction\
    factor is added to torque to stabilise the process"""

    def __init__(self, scene_, params_):
        """Class initialization. Requires scene, controller as well as two object and the local point of application \
        of the spring forces"""

        Muscle.__init__(self, scene_, params_)
        # Model constants and variables
        if "k" in self.params:
            self.k = self.params["k"]  # scalar in N/m
        else:
            self.k_cont = 100
        if "c" in self.params:
            self.c = self.params["c"]  # scalar in N.s/m
        else:
            self.k_cont = 10
        if "kc" in self.params:
            self.k_cont = self.params["kc"]  # no dimension
        else:
            self.k_cont = 0
        if "kt" in self.params:
            self.damp_torque_fact = self.params["kt"]  # no dimension
        else:
            self.damp_torque_fact = 0.1

        if self.active:
            self.l = self.app_point_2_world - self.app_point_1_world  # global coordinate vector between app points in m
            v = self.obj2.getVelocity(self.app_point_2) - self.obj1.getVelocity(self.app_point_1)
            self.v_norm = v.dot(self.l.normalized()) * self.l.normalized()  # normal velocity vector in m/s
            self.l0 = self.params["kl0"] * self.l.length  # scalar in m
            self.l_cont = self.l0  # scalar in m

    def update(self, **kwargs):
        """Update and apply forces on the objects connected to the spring. The spring can be controlled in length by \
        fixing manually l0"""

        if "ctrl_sig" in kwargs:
            ctrl_sig = kwargs["ctrl_sig"]
        else:
            ctrl_sig = None

        # If muscle has not been deactivated
        if self.active:
            # get control length
            if ctrl_sig == None:
                self.l_cont = self.l0  # by default, control length is the spring reference length
            else:
                self.l_cont = self.l0 * (1 + self.k_cont * ctrl_sig)

            # get length and velocity
            self.app_point_1_world = self.obj1.worldTransform * self.app_point_1
            self.app_point_2_world = self.obj2.worldTransform * self.app_point_2
            self.l = self.app_point_2_world - self.app_point_1_world

            # Center of gravity and lever arm
            cg_1 = self.obj1.worldPosition
            cg_2 = self.obj2.worldPosition
            lever_1_vect = self.app_point_1_world - cg_1
            lever_2_vect = self.app_point_2_world - cg_2

            # Damping must be in spring axis direction.
            v = self.obj2.getVelocity(self.app_point_2) - self.obj1.getVelocity(self.app_point_1)
            self.v_norm = v.dot(self.l.normalized()) * self.l.normalized()
            # print("l: " + str(self.l) + " norm: " + str(self.l.normalized()) + " v = " +  str(v) + "vdot" + str(v.dot(self.l.normalized())) +" vnorm: " + str(self.v_norm))

            # compute spring force
            force_s = - (self.k * (self.l.length - self.l_cont)) * self.l.normalized()

            # compute damping force
            force_d = - self.c * self.v_norm

            # compute total force
            force = force_s + force_d

            # compute total torques
            torque_1 = self.damp_torque_fact * lever_1_vect.cross(-force)
            torque_2 = self.damp_torque_fact * lever_2_vect.cross(force)

            # apply impusle on an object point only in traction
            f_type = "Push"
            if float((force * self.l.normalized())) < 0.0:
                f_type = "Pull"
                self.obj1.applyForce(- force)
                self.obj2.applyForce(force)
                self.obj1.applyTorque(torque_1)
                self.obj2.applyTorque(torque_2)

            # DEBUG data
            self.draw_muscle()
            self.n_iter += 1

            self.logger.debug("Muscle " + self.name + ":" + str(self.n_iter) + ": Ft = " + str(
                force) + " - " + str(force * self.l.normalized()) + "N")
            self.logger.debug("  Type = " + f_type)
            self.logger.debug("  Fs = " + str(force_s) + " ;  Fd = " + str(force_d))
            self.logger.debug("  l = " + str(self.l) + " ; l0 = " + str(self.l0))
            self.logger.debug("  L P1 = " + str(self.app_point_1) + " ; L P2 = " + str(self.app_point_2))
            self.logger.debug("  G P1 = " + str(self.app_point_1_world) + " ; G P2 = " + str(self.app_point_2_world))
            self.logger.debug("  G O1 = " + str(cg_1) + " ; G O2 = " + str(cg_1))
            self.logger.debug("  G OP 1 = " + str(lever_1_vect) + " ; G CG 2 = " + str(lever_2_vect))
            self.logger.debug("  T1 = " + str(torque_1) + " ; T2 = " + str(torque_2))
        else:
            self.logger.warning("Muscle " + self.name + " has been deactivated.")
