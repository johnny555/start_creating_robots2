"""
This file runs the sim with all system operating.

It's designed to provide a unified interface for the robot examples. 

"""

from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from os.path import join

def generate_launch_description():

    base_path = get_package_share_directory("krytn")
    web_connection = IncludeLaunchDescription(join(get_package_share_directory("rosbridge_server"), "launch","rosbridge_websocket_launch.xml"))

    web_server = ExecuteProcess(
        cmd="flask run".split(' '),
        name="start flask server",
        output="both",
        additional_env={'FLASK_APP':join(base_path, 'krytn/app.py'), 'FLASK_ENV':'development' }
    )
    return LaunchDescription([web_connection, web_server])