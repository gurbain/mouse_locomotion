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

import math

import bge
from mathutils import Vector as vec


class HillMuscle:
    "This class implements Hill Model for muscle force "

    def __init__(self, scene_, params_):
        "Class initialization. Parameters can be found in D.F.B. Haeufle, M. Günther, A. Bayer, S. Schmitt (2014) \
        Hill-type muscle model with serial damping and eccentric force-velocity relation. Journal of Biomechanics"

        self.n_iter = 0
        self.scene = scene_
        self.params = params_

        ## Contractile Element (CE)
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

        ## Parallel Elastic Element (PEE)
        self.PEE_L_PEE0 = 0.9  # rest length of PEE normalized to optimal lenght of CE (Guenther et al., 2007)
        self.PEE_l_PEE0 = self.PEE_L_PEE0 * self.CE_l_CEopt  # rest length of PEE (Guenther et al., 2007)
        self.PEE_v_PEE = 2.5  # exponent of F_PEE (Moerl et al., 2012)
        self.PEE_F_PEE = 2.0  # force of PEE if l_CE is stretched to deltaWlimb_des (Moerl et al., 2012)
        self.PEE_K_PEE = self.PEE_F_PEE * (
            self.CE_F_max / (self.CE_l_CEopt * (self.CE_DeltaW_limb_des + 1 - self.PEE_L_PEE0)) ** self.PEE_v_PEE)
        # factor of non-linearity in F_PEE (Guenther et al., 2007)

        ## Serial Damping Element (SDE)
        self.SDE_D_SE = 0.3  # xxx dimensionless factor to scale d_SEmax (Moerl et al., 2012)
        self.SDE_R_SE = 0.01  # minimum value of d_SE normalised to d_SEmax (Moerl et al., 2012)
        self.SDE_d_SEmax = self.SDE_D_SE * (self.CE_F_max * self.CE_A_rel0) / (self.CE_l_CEopt * self.CE_B_rel0)
        # maximum value in d_SE in [Ns/m] (Moerl et al., 2012)

        ## Serial Elastic Element (SEE)
        self.SEE_l_SEE0 = 0.172  # rest length of SEE in [m] (Kistemaker et al., 2006)
        self.SEE_DeltaU_SEEnll = 0.0425  # relativ stretch at non-linear linear transition (Moerl et al., 2012)
        self.SEE_DeltaU_SEEl = 0.017  # relativ additional stretch in the linear part providing a force increase of deltaF_SEE0 (Moerl, 2012)
        self.SEE_DeltaF_SEE0 = 568  # both force at the transition and force increase in the linear part in [N] (~ 40# of the maximal isometric muscle force)

        self.SEE_l_SEEnll = (1 + self.SEE_DeltaU_SEEnll) * self.SEE_l_SEE0
        self.SEE_v_SEE = self.SEE_DeltaU_SEEnll / self.SEE_DeltaU_SEEl
        self.SEE_KSEEnl = self.SEE_DeltaF_SEE0 / (self.SEE_DeltaU_SEEnll * self.SEE_l_SEE0) ** self.SEE_v_SEE
        self.SEE_KSEEl = self.SEE_DeltaF_SEE0 / (self.SEE_DeltaU_SEEl * self.SEE_l_SEE0)

    def update(self, ctrl_sig):
        "Update control signals and forces"

        # Here, we update the muscle forces given geometry and control signal
        self.n_iter += 1

    # print("Muscle iteration: " + str(self.n_iter))


    def update(self, l_CE, l_MTC, dot_l_MTC, q):
        "Computations are based on D.F.B. Haeufle, M. Günther, A. Bayer, S. Schmitt (2014) \
        Hill-type muscle model with serial damping and eccentric force-velocity relation. Journal of Biomechanics"

        # Isometric force (Force length relation)
        if l_CE >= self.CE_l_CEopt:  # descending branch
            F_isom = math.exp(-(abs(((l_CE / self.CE_l_CEopt) - 1) / self.CE_DeltaW_limb_des)) ** self.CE_v_CElimb_des)
        else:  # ascending branch
            F_isom = math.exp(-(abs(((l_CE / self.CE_l_CEopt) - 1) / self.CE_DeltaW_limb_asc)) ** self.CE_v_CElimb_asc)

        # Force of the parallel elastic element PEE
        if l_CE >= self.PEE_l_PEE0:
            F_PEE = self.PEE_K_PEE * (l_CE - self.PEE_l_PEE0) ** (self.PEE_v_PEE)
        else:  # shorter than slack length
            F_PEE = 0

        # Force of the serial elastic element SEE
        l_SEE = abs(l_MTC - l_CE)  # SEE length
        if (l_SEE > self.SEE_l_SEE0) and (l_SEE < self.SEE_l_SEEnll):  # non-linear part
            F_SEE = self.SEE_KSEEnl * ((l_SEE - self.SEE_l_SEE0) ** (self.SEE_v_SEE))
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


class DampedSpringMuscle:
    "This class implements a simple muscle composed by a spring and a damping in parallel"

    def __init__(self, scene_, params_):
        "Class initialization. Requires scene, controller as well as two object and the local point of application \
        of the spring forces"

        self.n_iter = 0
        self.scene = scene_
        self.params = params_
        self.name = self.params["name"]
        self.debug = self.params["debug"]
        self.active = True

        # Check if onject exist
        if not self.params["obj_1"] in self.scene.objects:
            print("\033[91m[CRITIC]\033[0m Muscle " + self.name + " deactivated: first extremity object doesn't exit." \
                  + " Check your configuration file!")
            self.active = False
        else:
            self.obj1 = self.scene.objects[self.params["obj_1"]]
        if not self.params["obj_2"] in self.scene.objects:
            print("\033[91m[CRITIC]\033[0m Muscle " + self.name + " deactivated: first extremity object doesn't exit." \
                  + " Check your configuration file!")
            self.active = False
        else:
            self.obj2 = self.scene.objects[self.params["obj_2"]]

        # Points of application in local coordinates
        if self.params["anch_1"] == None:
            print("\033[93m[DANGER]\033[0m You have not defined the first application point of muscle " + self.name + \
                  "! Center is taken by default. This may results in erroneous simulation")
            self.params["anch_1"] = [0.0, 0.0, 0.0]
        if self.params["anch_2"] == None:
            print("\033[93m[DANGER]\033[0m You have not defined the second application point of muscle " + self.name + \
                  "! Center is taken by default. This may results in erroneous simulation")
            self.params["anch_2"] = [0.0, 0.0, 0.0]
        self.app_point_1 = vec((self.params["anch_1"]))
        self.app_point_2 = vec((self.params["anch_2"]))

        # Model constants and variables
        self.k = self.params["k"];  # scalar in N/m
        self.c = self.params["c"];  # scalar in N/m
        self.k_cont = self.params["kc"]  # no dimension
        if self.active:
            self.app_point_1_world = self.obj1.worldTransform * self.app_point_1  # global coordinates of app point 1 in m
            self.app_point_2_world = self.obj2.worldTransform * self.app_point_2  # global coordinates of app point 2 in m
            self.l = self.app_point_2_world - self.app_point_1_world  # global coordinate vector between app points in m
            v = self.obj2.getVelocity(self.app_point_2) - self.obj1.getVelocity(self.app_point_1)
            self.v_norm = v.dot(self.l.normalized()) * self.l.normalized()  # normal velocity vector in m/s
            self.l0 = self.params["kl0"] * self.l.length;  # scalar in m
            self.l_cont = self.l0;  # scalar in m

    def draw_muscle(self, color_=[256, 0, 0]):
        bge.render.drawLine(self.app_point_1_world, self.app_point_2_world, color_)

    def compute_step_energy(self):

        return 0

    def update(self, ctrl_sig=None):
        "Update and apply forces on the objects connected to the spring. The spring can be controlled in length by \
        fixing manually l0"

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
            impulse = force / bge.logic.getLogicTicRate()

            # apply impusle on an object point only in traction
            f_type = "Push"
            if float((force * self.l.normalized())) < 0.0:
                f_type = "Pull"
                self.obj1.applyImpulse(self.app_point_1_world, - impulse)
                self.obj2.applyImpulse(self.app_point_2_world, impulse)

            # DEBUG data
            self.draw_muscle()
            self.n_iter += 1

            if self.debug:
                print("[DEBUG] Muscle " + self.name + " iteration " + str(self.n_iter) + ": Force = " + str(
                    force) + " norm = " \
                      + str(force * self.l.normalized()) + "N")
                print("\t\t\tType = " + f_type)
                print("\t\t\tFs = " + str(force_s))
                print("\t\t\tFd = " + str(force_d))
                print("\t\t\tl = " + str(self.l) + " ; l0 = " + str(self.l0))
                print(
                    "\t\t\tG app point 1=" + str(self.app_point_1_world) + " ;G app point 2=" + str(
                        self.app_point_2_world))
                print("\t\t\tL app point 1=" + str(self.app_point_1) + " ;L app point 2=" + str(self.app_point_2))
        else:
            if self.debug:
                print("\033[93m[DANGER]\033[0m Muscle " + self.name + " has been deactivated.")


class Muscle(DampedSpringMuscle):
    def __init__(self, scene_, params_):
        "Class initialization"

        super(Muscle, self).__init__(scene_, params_)
