import bge
from body import *

print("## Virtual Mouse Simulation")
print("## ------------------------")
print("##")
print("## Gabriel Urbain - UGent 2016")

# Get blender handles
controller = bge.logic.getCurrentController()
scene = bge.logic.getCurrentScene()
keyboard = bge.logic.keyboard
owner = controller.owner
 
# Initialize variables here
owner["n_iter"] = 0
owner["cheesy"] = Mouse(scene, controller)
