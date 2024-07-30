from pathlib import Path

import launch
from launch.substitutions import Command
from launch.substitutions import LaunchConfiguration

import launch_ros
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_share = Path(launch_ros.substitutions.FindPackageShare(package='first_robot_freecad').find('first_robot_freecad'))
    default_model_path = pkg_share / 'urdf/FirstRobot.urdf'

    robot_state_publisher_node = launch_ros.actions.Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {
                # ParameterValue is required to avoid being interpreted as YAML.
                'robot_description': ParameterValue(Command(['xacro ', LaunchConfiguration('model')]), value_type=str),
            },
            ]
    )

    return launch.LaunchDescription([
        launch.actions.DeclareLaunchArgument(name='model',
                                             default_value=str(default_model_path),
                                             description="Absolute path to the robot's URDF file"),
        robot_state_publisher_node,
    ])
