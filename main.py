import bge

# Get personal variables
owner = bge.logic.getCurrentController().owner
keyboard = bge.logic.keyboard


# DEBUG Control the muscle length from keyboard
if bge.logic.KX_INPUT_ACTIVE == keyboard.events[bge.events.UPARROWKEY]:
	owner["cheesy"].l_fo_leg.biceps.l0 -= 0.02
	owner["cheesy"].r_fo_leg.biceps.l0 -= 0.02
if bge.logic.KX_INPUT_ACTIVE == keyboard.events[bge.events.DOWNARROWKEY]:
	owner["cheesy"].l_fo_leg.biceps.l0 += 0.02
	owner["cheesy"].r_fo_leg.biceps.l0 += 0.02
if bge.logic.KX_INPUT_ACTIVE == keyboard.events[bge.events.LEFTARROWKEY]:
	owner["cheesy"].l_ba_leg.biceps.l0 -= 0.02
	owner["cheesy"].r_ba_leg.biceps.l0 -= 0.02
if bge.logic.KX_INPUT_ACTIVE == keyboard.events[bge.events.RIGHTARROWKEY]:
	owner["cheesy"].l_ba_leg.biceps.l0 += 0.02
	owner["cheesy"].r_ba_leg.biceps.l0 += 0.02

# Time-step update instructions
owner["n_iter"] += 1
owner["cheesy"].update_mvt()
print("[DEBUG] Main iteration: " + str(owner["n_iter"]))