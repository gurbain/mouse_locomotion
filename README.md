# mouse_locomotion
Blender model and simulation scripts for mouse locomotion driven by reservoir computing

### Running on Ubuntu 14.04
This installation has been tested with Ubuntu 14.04 only but should work for other OS since Blender is a multi-platform tool.
- Install Blender:
```
sudo apt-get install blender
```
This code has also been tested with Blender 2.70 manually compiled and Python 3. More information about manual building here: http://wiki.blender.org/index.php/Dev:Doc/Building_Blender

- Import the model:
```
git clone https://github.com/Gabs48/mouse_locomotion
```

- Open the model:
```
cd mouse_locomotion
blender cheesy.blend
```

### Editing
An overview of the simulation process can be found in **architecture.jpg**. The init.py and main.py scripts are started from the blender object **obj_head**
