# FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu-22.04
FROM osrf/ros:humble-desktop-full

RUN apt update && apt upgrade -y
RUN apt install -y ros-humble-turtlesim ros-humble-rqt

RUN apt install -y bash-completion python3-argcomplete python3-colcon-argcomplete

# env 
RUN apt install -y ssh git

# GUI - on host: sudo xhost +local:docker
ENV DISPLAY=$DISPLAY
ENV XAUTHORITY=/tmp/.docker.xauth

RUN apt install -y x11-apps