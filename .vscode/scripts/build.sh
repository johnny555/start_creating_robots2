#!/bin/bash
source /opt/ros/jazzy/local_setup.bash
source install/setup.bash

colcon build --symlink-install --merge-install
