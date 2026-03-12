colcon build --symlink-install
source install/setup.bash

ros2 launch run.py


ros2 run image_feeder talker
ros2 run jair_turtlesim follower
