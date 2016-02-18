# Mouse Locomotion Simulation
This repository proposes a Blender model and some simulation scripts for mouse locomotion driven by reservoir computing.

### Running on Ubuntu 14.04
Installation has been tested with Ubuntu 14.04 only but should work for other OS since Blender is a multi-platform tool.
- Install Blender:
```
sudo apt-get install blender
```
This code has also been tested with Blender 2.76 manually compiled and Python 3. More information about manual building here: http://wiki.blender.org/index.php/Dev:Doc/Building_Blender
- Import the model:
```
git clone https://github.com/Gabs48/mouse_locomotion
```
- Run the simulation:
```
cd mouse_locomotion
blender -b cheesy.blend --python start.py
```
As the view is not set, nothing appears in the GUI that opens but the simulation runs in the background and should ouput stuff in the shell. The simulation can also be runned inside the blender software, by placing the cursor on the 3D view and pressing the keyboard key 'p'.

### Editing
- To edit the model, just open it in Blender:
```
cd mouse_locomotion
blender cheesy.blend
```
- To edit the controls, open the Python scripts in your IDE. An overview of the simulation process can be found in *architecture.jpg*. The init.py and main.py scripts are started from the blender object *obj_head* (see Outliner tab). This can be modified in the Logic Editor tab.
