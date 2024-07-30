from launch.actions import GroupAction
from launch_ros.actions import PushRosNamespace
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from ament_index_python.packages import get_package_share_directory
from os.path import join
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, ExecuteProcess

from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_move_group_launch



def generate_launch_description():

    move_group = IncludeLaunchDescription(join(get_package_share_directory("maci_moveit"), "launch", "move_group.launch.py"))
    rviz = IncludeLaunchDescription(join(get_package_share_directory("maci_moveit"), "launch", "moveit_rviz.launch.py"))
    
    mg_sim_time = ExecuteProcess(cmd=["ros2", "param", "set", "/move_group", "use_sim_time","True"])
    rviz_sim_time = ExecuteProcess(cmd=["ros2", "param", "set", "/rviz", "use_sim_time","True"])

      
    return LaunchDescription([move_group, rviz, mg_sim_time, rviz_sim_time])