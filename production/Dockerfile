FROM my_turtlesim_base:latest

SHELL ["/bin/bash", "-c"]

WORKDIR /workspace
ADD . .

WORKDIR /workspace/src
RUN source /opt/ros/humble/setup.bash && colcon build

ENTRYPOINT ["/bin/bash", "/workspace/src/run.sh"]
