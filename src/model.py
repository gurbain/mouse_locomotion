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

import os.path
import sys

import bpy


def create_population(n_pop_=10):
    "Duplicate the model to create population. Speed up the process when simulation is fast \
    and computers number is limited"

    # Hide ground, lamps and camera
    bpy.data.objects["obj_ground"].hide = True
    bpy.data.objects["Camera"].hide = True
    bpy.data.objects["Lamp"].hide = True
    bpy.data.objects["Lamp.001"].hide = True
    bpy.data.objects["Lamp.002"].hide = True

    # Selct all remaining objects in buffer
    bpy.ops.object.select_all(action='SELECT')

    for i in range(n_pop_ - 1):
        # Duplicate and translate new object
        bpy.ops.object.duplicate()
        bpy.ops.transform.translate(value=(0, 15, 0), constraint_axis=(False, True, False),
                                    constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED',
                                    proportional_edit_falloff='SMOOTH',
                                    proportional_size=1, release_confirm=True)

    # Save new model with a different name
    splited_filename = os.path.splitext(bpy.data.filepath)
    saved_filename = splited_filename[0] + "_pop" + splited_filename[1]
    bpy.ops.wm.save_as_mainfile(filepath=saved_filename)
    print("[INFO] Population Model of size " + str(n_pop_) + " created and savec with name: " + saved_filename)


def start_player():
    "Start blender game engine from Blender"

    bpy.context.scene.render.engine = 'BLENDER_GAME'
    bpy.ops.view3d.game_start()


# Start the required script
eval(sys.argv[len(sys.argv) - 1])
