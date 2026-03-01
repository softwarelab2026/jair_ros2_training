# FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu-22.04
FROM ros:humble-ros-base

RUN apt update && apt upgrade -y
RUN apt install -y ssh

ENV DISPLAY=$DISPLAY
ENV XAUTHORITY=/tmp/.docker.xauth
# host: sudo xhost +