#!/bin/bash

source /opt/ros/jazzy/setup.bash
source install/setup.bash

echo "Starting FreeCAD, please wait ..."
/home/ubuntu/FreeCAD.AppImage --appimage-extract-and-run --module-path ${PYTHONPATH//:/' --module-path '} cad_designs/first_robot.FCStd
