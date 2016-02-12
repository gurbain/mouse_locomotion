import bge

# Get personal variables
owner = bge.logic.getCurrentController().owner

# Time-step update instructions
owner["n_iter"] += 1
owner["cheesy"].update_mvt()
print("Main iteration: " + str(owner["n_iter"]))