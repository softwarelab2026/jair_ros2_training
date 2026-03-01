#!/bin/bash

echo "source $(pwd)/ros_settings.sh" >> ~/.bashrc
echo "source /usr/share/colcon_cd/function/colcon_cd.sh" >> ~/.bashrc
echo "export _colcon_cd_root=/opt/ros/humble/" >> ~/.bashrc

pip install -r requirements.txt
pre-commit install
pre-commit run
