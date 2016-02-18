import bge
from body import *

print("#################################")
print("##   Virtual Mouse Simulation   #")
print("##   ------------------------   #")
print("##                              #")
print("## Gabriel Urbain - UGent 2016  #")
print("#################################\n")

# Get blender handles
controller = bge.logic.getCurrentController()
scene = bge.logic.getCurrentScene()
keyboard = bge.logic.keyboard
owner = controller.owner
 
# Initialize variables here
owner["n_iter"] = 0
owner["cheesy"] = Body(scene, controller, "cheesy")