FROM osrf/ros:jazzy-desktop
WORKDIR /workspace
COPY . /workspace/.devcontainer/
RUN apt-get update \
    && apt-get install -y ros-jazzy-ros-gz  ros-jazzy-rqt-robot-steering ros-jazzy-slam-toolbox ros-jazzy-navigation2 \
    ros-jazzy-nav2-bringup wget python3-pip vim ros-jazzy-ros2-controllers ros-jazzy-realsense2-description \
    ros-jazzy-rqt-robot-steering ros-jazzy-gz-ros2-control ros-jazzy-ros2-controllers ros-jazzy-gz-ros2-control-demos \
    ros-jazzy-moveit-planners-chomp ros-jazzy-moveit-ros-perception ros-jazzy-ur-description ros-jazzy-rclpy ros-jazzy-action-msgs \
    ros-jazzy-control-msgs ros-jazzy-geometry-msgs ros-jazzy-moveit-msgs ros-jazzy-sensor-msgs ros-jazzy-std-srvs ros-jazzy-trajectory-msgs \
    ros-jazzy-launch-param-builder ros-jazzy-moveit-setup-assistant ros-jazzy-moveit-configs-utils ros-jazzy-moveit-simple-controller-manager\
    ros-jazzy-moveit-planners-ompl ros-jazzy-pilz-industrial-motion-planner ros-jazzy-moveit-planners-stomp\
    && rm -rf /var/lib/apt/lists/*
RUN bash .devcontainer/setup_container.bash
