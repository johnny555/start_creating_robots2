""" This launch file starts: 
- Navigation stack
- VSTL
- slam_toolbox localization
"""

from launch import LaunchDescription
from launch_ros.actions import Node , SetRemap
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, GroupAction
from os.path import join

def generate_launch_description():

    base_path = get_package_share_directory("krytn")

    # We will include everything from the mapping launch file, making sure that sensors are now enabled and setting up RVIZ for navigation.
    gazebo_and_mapping = IncludeLaunchDescription(join(base_path, "launch","mapping.launch.py"),
                                      launch_arguments=[ ("rviz_config","nav.rviz")])

    # Nav2 bringup for navigation
    navigation = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(join(get_package_share_directory('nav2_bringup'), 'launch','navigation_launch.py')),
        launch_arguments={
            'map_subscribe_transient_local': 'true',
            'use_sim_time': 'true',
            'params_file': get_package_share_directory('krytn') + '/config/navigation.yaml',
            'autostart': 'True'
        }.items(),
    )

    nav_remapped = GroupAction(actions=[#remap, 
        navigation])


    return LaunchDescription([
        gazebo_and_mapping, nav_remapped
    ])