# FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu-22.04
FROM ros:humble-ros-base

RUN apt update && apt upgrade -y
RUN apt install -y ros-humble-turtlesim

RUN apt install -y bash-completion python3-argcomplete python3-colcon-argcomplete

# env 
RUN apt install -y ssh git

# GUI - on host: sudo xhost +
ENV DISPLAY=$DISPLAY
ENV XAUTHORITY=/tmp/.docker.xauth