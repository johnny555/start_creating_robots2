from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch_param_builder import load_xacro
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from os.path import join 
from launch.substitutions import Command
from pathlib import Path
import os

def generate_launch_description():

    # Start a simulation with the cafe world
    cafe_world_uri = join(get_package_share_directory("gamecity"), "worlds", "gamecity.sdf")
    path = join(get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py")
    
    gazebo_sim = IncludeLaunchDescription(path,
                                          launch_arguments=[("gz_args", '-r '+ cafe_world_uri)])

    # Create a robot in the world.
    # Steps: 
    # 1. Process a file using the xacro tool to get an xml file containing the robot description.
    # 2. Publish this robot description using a ros topic so all nodes can know about the joints of the robot. 
    # 3. Spawn a simulated robot in the gazebo simulation using the published robot description topic. 

    # Step 1. Process robot file. 
    robot_file = join(get_package_share_directory("krytn"), "robot_description","krytn.urdf.xacro")
    robot_xml = load_xacro(Path(robot_file))

    #Step 2. Publish robot file to ros topic /robot_description & static joint positions to /tf
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='both',
        parameters=[{'robot_description':robot_xml, 
                     'use_sim_time':True}],
    )

    # Step 3. Spawn a robot in gazebo by listening to the published topic.
    robot = Node(
        package='ros_gz_sim',
        executable="create",
        arguments=[
            "-topic", "/robot_description", 
            "-z", "0.5",
        ],
        name="spawn_robot",
        output="both"
    )

    # Gazebo Bridge: This brings data (sensors/clock) out of gazebo into ROS.
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                   '/lidar@sensor_msgs/msg/LaserScan@gz.msgs.LaserScan',
                   '/lidar/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked',
                   '/realsense/image@sensor_msgs/msg/Image[gz.msgs.Image',
                   '/realsense/depth@sensor_msgs/msg/Image[gz.msgs.Image',
                   '/realsense/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked',
                   ],
        output='screen'
        )

    
    # A gui tool for easy tele-operation.
    robot_steering = Node(
        package="rqt_robot_steering",
        executable="rqt_robot_steering",
    )

    # Step 5: Enable the ros2 controllers
    start_controllers  = Node(
                package="controller_manager",
                executable="spawner",
                arguments=['joint_state_broadcaster', 'diff_drive_base_controller'],
                output="screen",
            )

    twist_stamper = Node(
        package="twist_stamper",
        executable="twist_stamper.py",
        remappings=[("/cmd_vel_in", "/cmd_vel"),
                       ("/cmd_vel_out",  "/diff_drive_base_controller/cmd_vel")],
        parameters=[{"use_sim_time","True"}],
        output="screen"
    )  

    # Fix Frames while we wait for merged changes to make their way into released packages: 
    # https://github.com/gazebosim/gz-sensors/pull/446/commits/277d3946be832c14391b6feb6971e243f1968486 
    # This fix allows us to specify the frame for the sensor rather than create a fixed transform here. 
    static_pub = Node(package="tf2_ros", 
                      executable="static_transform_publisher",
                      arguments=["0","0","0","0","0","0", "lidar_2d_link", "krytn/base_footprint/lidar_2d_v1", ])
    
    static_pub2 = Node(package="tf2_ros", 
                      executable="static_transform_publisher",
                      arguments=["0","0","0","0","0","0",  "realsense_link", "krytn/base_footprint/realsense_d435"])



  
    return LaunchDescription([gazebo_sim, bridge, robot, twist_stamper,
                              robot_steering, robot_state_publisher,
                              start_controllers, static_pub, static_pub2])