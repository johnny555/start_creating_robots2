#!/bin/bash
bash .vscode/scripts/build.sh

source install/setup.bash
ros2 launch first_robot gazebo.launch.py
