#!/bin/bash

source /opt/ros/jazzy/local_setup.bash

# Create user ros, and allow it to install stuff. 
adduser --disabled-password --gecos "docker user" ros
echo 'ros ALL=(ALL) NOPASSWD:ALL' > /etc/sudoers.d/ros && chmod 0440 /etc/sudoers.d/ros
chown -R ros /workspace

# Get FreeCAD 
sudo --user=ros wget -O /home/ros/FreeCAD.AppImage https://github.com/FreeCAD/FreeCAD-Bundle/releases/download/weekly-builds/FreeCAD_weekly-builds-38334-conda-Linux-x86_64-py311.AppImage
sudo chmod +x /home/ros/FreeCAD.AppImage 

# Setup FreeCAD Cross For FreeCAD
sudo --user=ros mkdir -p /home/ros/.local/share/FreeCAD/Mod/
sudo --user=ros git clone https://github.com/johnny555/freecad.cross.git /home/ros/.local/share/FreeCAD/Mod/freecad.cross

# Get python deps
sudo --user=ros pip install black urdf-parser-py

# clean up apt

#     
su ros

# Make it so that sourcing happens automatically
echo "source /opt/ros/jazzy/setup.bash" >> /home/ros/.bashrc
echo "source /workspace/install/setup.bash" >> /home/ros/.bashrc

# Suppress deprecated setuptools warning
echo "PYTHONWARNINGS=\"ignore:setup.py install is deprecated::setuptools.command.install,ignore:easy_install command is deprecated::setuptools.command.easy_install\"; export PYTHONWARNINGS" >> /home/ros/.bashrc

# Add GAZEBO path so we can easily include models. Must use merge install. 
# Sholud be able to use package:// syntax now. 
echo "export GZ_SIM_RESOURCE_PATH=/workspace/install/share/:/opt/ros/jazzy/share/" >> /home/ros/.bashrc
echo "export SDF_PATH=/workspace/install/share/:/opt/ros/jazzy/share/" >> /home/ros/.bashrc