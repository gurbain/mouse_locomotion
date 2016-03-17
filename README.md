# Mouse Locomotion Simulation
This repository gathered blender models and python scripts for quadruped locomotion driven by reservoir computing.

## Download:
Installation has been tested with Ubuntu 14.04 only but should work for other OS since Blender is a multi-platform tool.

- Import the model:
```
git clone https://github.com/Gabs48/mouse_locomotion
```

## Local Simulation

### Dependency Installation
This repository uses python libraries Rpyc and Plumbum. They are available on the official python distribution and can be install via pip:
```
sudo pip install rpyc
sudo pip install plumbum
```

### Blender user version Installation

This simulator uses features only available in Blender 2.77 version. For linux users with AMD64 processor architecture, this version of blender can be installed automatically in */opt* thanks to the *install_blender* script. Absolute paths and users parameters at the beginning of the script shall be edited manually.

```
cd mouse_locomotion
./sh/install_blender.sh
```

### Execution

 - Start a registry server to aknowledge the cloud state (shell 1):
```
qSim -r
```
 - Start a service server to process requests (shell 2):
```
qSim -s
``` 
 - Start simulation (shell 3):
```
qSim -m model.blend -c MyConfig
```

## Cloud Simulation on Elis network

### Bashrc Installation

A custom .bashrc file referencing all variables can be installed on all computers of the network with the script:
 
```
cd mouse_locomotion
./sh/install_remote_bash.sh
```

### Installation

The following script download and install this repository as well as all dependencies on remote computers:
 
```
./install_packages.sh
```

### Execution

- Start a registry server to aknowledge the cloud state (shell 1):
```
qSim -r
```
 - Start services server on the cloud (shell 2). The following daemon can be used to start a XVFB server (to redirect the simulation display) as well a RPYC server behind a screen shell. It also allows to stop or restart them remotely. Absolute paths and users parameters at the beginning of the script shall be edited manually to adapt to the network:
 
```
./rpyser start|stop|restart|help
```
 - Start simulation (shell 3):
```
qSim -m model.blend -c MyConfig
```

## Edition

- To edit geometry, mass and visual properties of the 3D model, open it with blender:
```
./blender-2.77/blender model.blend
```
- To edit the brain model, the muscle model and the body configuration, open the file *config.py* with your IDE:
```
vi config.py
```