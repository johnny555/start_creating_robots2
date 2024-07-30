"""
This file runs the sim with all system operating.

It's designed to provide a unified interface for the robot examples. 

"""

from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from os.path import join

def generate_launch_description():

    base_path = get_package_share_directory("maci")
    gazebo = IncludeLaunchDescription(join(base_path, "launch","gazebo.launch.py"))

    return LaunchDescription([gazebo])