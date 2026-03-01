Robotics Course Assignment: Turtlesim Ball Tracking

Objective:
In this assignment, students will create a ROS2 node in Python that enables a simulated robot to follow a ball within the Turtlesim simulator. Using image processing techniques, the robot should detect and track a ball in an input camera stream. Students will implement a position controller to move the robot towards the ball’s position within the simulated environment.

Assignment Details:

1. Environment Setup:

Use the Turtlesim simulator as the environment where the robot will move.

Students are expected to be familiar with ROS2 and Python for writing nodes and handling image messages.



2. Requirements:

Develop a ROS2 node in Python.

The node should subscribe to an image topic (e.g., /camera/image_raw) which provides a camera feed. An Image message containing a simulated video feed with the ball will be given as input.

The node should process each frame of this image to detect the position of the ball.

Use image processing techniques (such as color segmentation, contour detection, etc.) to identify the ball in the image. The ball's position should be considered as the target or goal for the robot.

Implement a position controller for the robot that calculates the control commands required to move the robot towards the ball's position.



3. Expected Functionality:

When the ball moves, the robot should adjust its trajectory accordingly to keep following the ball.

The control node should publish the desired velocity and direction commands to steer the robot towards the goal (i.e., the detected position of the ball).

The robot’s motion should be smooth and responsive, aiming to center on the ball as it moves within the Turtlesim environment.



4. Technical Requirements:

Node should subscribe to the /camera/image_raw topic to receive image data.

Process images using OpenCV (or any preferred image processing library) to detect the ball’s position.

Implement a simple proportional control strategy for steering towards the detected position of the ball.

Publish control commands to /turtle1/cmd_vel or the equivalent topic for controlling the Turtlesim robot.



5. Submission Requirements:

A well-commented Python script for the ROS2 node.

A brief report explaining the approach, image processing technique, and control strategy used. Describe any challenges faced and how they were addressed.

Include any test results, observations, or examples of the robot following the ball in the Turtlesim simulation.



6. Evaluation Criteria:

Functionality: Does the node detect the ball and accurately control the robot towards it?

Code Quality: Is the code well-structured, with meaningful comments and clear logic?

Control Strategy: Is the control strategy effective in achieving smooth and responsive movement?

Documentation: Does the report explain the approach, techniques used, and challenges clearly?




Note: Students are encouraged to use existing ROS2 libraries for image handling and may reference documentation for OpenCV and ROS2. This assignment requires a good understanding of image processing and basic control systems.