from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from os.path import join
from launch_param_builder import load_xacro
from pathlib import Path
from launch.substitutions import Command

"""
This launch assumes that gazebo is already running with the krytn simulation. 
"""
def generate_launch_description():
    # Create a robot in the world.
    # Steps: 
    # 1. Process a file using the xacro tool to get an xml file containing the robot description.
    # 2. Publish this robot description using a ros topic so all nodes can know about the joints of the robot. 
    # 3. Spawn a simulated robot in the gazebo simulation using the published robot description topic. 

    # Step 1. Process robot file. 
    robot_file = join(get_package_share_directory("maci"), "robot_description","maci.urdf.xacro")
    robot_xml = load_xacro(Path(robot_file))

    #Step 2. Publish robot file to ros topic /robot_description & static joint positions to /tf
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='both',
        parameters=[{'robot_description':robot_xml, 
                     'use_sim_time':True}],
    )

    # Step 3. Spawn a robot in gazebo by listening to the published topic.
    robot = Node(
        package='ros_gz_sim',
        executable="create",
        arguments="-topic robot_description -x -6.70 -y -9.34 -z 1.23".split(' '),
        name="spawn_robot",
        output="both"
    )

    # Step 5: Enable the ros2 controllers
    start_controllers  = Node(
                package="controller_manager",
                executable="spawner",
                arguments=['maci_joint_state_broadcaster', 'maci_controller', 'gripper_controller'],
                output="screen",
            )

    return LaunchDescription([robot_state_publisher, start_controllers, robot ])