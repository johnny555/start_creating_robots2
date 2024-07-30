#!/bin/bash
bash .vscode/scripts/build.sh

source install/setup.bash
ros2 launch krytn navigation.launch.py
