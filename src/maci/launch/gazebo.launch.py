from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from os.path import join
from launch.substitutions import Command


"""
Basic gazebo world loading. 
"""
def generate_launch_description():

    # Start a simulation with the cafe world
    cafe_world_uri = join(get_package_share_directory("gamecity"), "worlds", "gamecity.sdf")
    path = join(get_package_share_directory("ros_gz_sim"), "launch", "gz_sim.launch.py")
    #cafe_world_uri="empty.sdf"
    gazebo_sim = IncludeLaunchDescription(path,
                                          launch_arguments=[("gz_args",  cafe_world_uri + " -r" )])

    
    # Gazebo Bridge: This brings data (sensors/clock) out of gazebo into ROS.
    bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=['/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                   '/realsense/image@sensor_msgs/msg/Image[gz.msgs.Image',
                   '/realsense/depth@sensor_msgs/msg/Image[gz.msgs.Image',
                   '/realsense/points@sensor_msgs/msg/PointCloud2[gz.msgs.PointCloudPacked', ],
        output='screen'        )
    
    static_pub = Node(package="tf2_ros", 
                      executable="static_transform_publisher",
                      arguments=["0","0","0","0","0","0",  "realsense_link", "maci/realsense_link/realsense_d435"])
    

    maci = IncludeLaunchDescription(join(get_package_share_directory("maci"), "launch","spawn_maci.launch.py"))
    moveit = IncludeLaunchDescription(join(get_package_share_directory("maci"), "launch","moveit.launch.py"))


    return LaunchDescription([gazebo_sim, bridge, maci, moveit, static_pub ])