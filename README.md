# Mouse Locomotion Simulation
This repository gathered blender models and python scripts for quadruped locomotion driven by reservoir computing.

## Install
Installation has been tested with Ubuntu 14.04 only but should work for other OS since Blender is a multi-platform tool.

- Import the model:
```
git clone https://github.com/Gabs48/mouse_locomotion
```
- Install Blender:
This code uses some new features of Blender and requires Blender 2.77 at least. The Blender 2.77 binaries can be downloaded via their repository:
```
cd mouse_locomotion
wget http://download.blender.org/release/Blender2.77/blender-2.77-testbuild2-linux-glibc211-x86_64.tar.bz2
tar -xf blender-2.77-testbuild2-linux-glibc211-x86_64.tar.bz2
mv blender-2.77-testbuild2-linux-glibc211-x86_64 blender-2.77
```
*An explanation is needed here for Windows and OSX*

## Run
The simulation can be launched via the *start.py* script:
```
./start.py [[-options]] model.blend
```
The full list of options can be accessed by adding the *-h* or *--help* parameters.

## Edit

- To edit geometry, mass and visual properties of the 3D model, open it with blender:
```
./blender-2.77/blender model.blend
```
- To edit the brain model, the muscle model and the body configuration, open the file *config.py* with your IDE:
```
vi config.py
```
