FROM osrf/ros:humble-desktop-full
RUN apt update && apt upgrade -y

# env
RUN apt install -y ssh git
# GUI - on host: sudo xhost +local:docker
ENV DISPLAY=$DISPLAY
ENV XAUTHORITY=/tmp/.docker.xauth

RUN apt install -y bash-completion python3-pip python3-argcomplete python3-colcon-argcomplete

RUN apt install -y ros-humble-turtlesim ros-humble-rqt python3-colcon-core python3-colcon-common-extensions
