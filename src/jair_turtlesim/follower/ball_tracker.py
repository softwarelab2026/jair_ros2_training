import numpy as np
from cv_bridge import CvBridge
from follower.img_detection import extract_ball_pos
from follower.pid import PID
from follower.tracker import turtle_follow_ball
from rclpy.impl.rcutils_logger import RcutilsLogger
from sensor_msgs.msg import Image
from turtlesim.msg import Pose


def _ros_img_to_cv2(_frame: Image) -> np.ndarray:
    return CvBridge().imgmsg_to_cv2(_frame, desired_encoding='passthrough')


def image_rotation_to_turtle_window(ball_x: float, ball_y: float) -> tuple[float, float]:
    ball_y = 1 - ball_y
    return ball_x, ball_y


# pylint: disable=too-few-public-methods
class BallTracker:
    def __init__(self, logger: RcutilsLogger):
        self.pid_linear = PID(30, 0.05, 0.01, 10)
        self.pid_angular = PID(12, 0.05, 0.01, 10)

        self._logger = logger

    def track_ball(self, _frame: Image, turtle_pos: Pose, dt: float) -> tuple[float, float]:
        turtle_window_width, turtle_window_height = 11, 11

        ball_x, ball_y = extract_ball_pos(_ros_img_to_cv2(_frame))
        norm_ball_x = np.interp(ball_x, [0, _frame.width], [0, 1])
        norm_ball_y = np.interp(ball_y, [0, _frame.height], [0, 1])
        norm_ball_x, norm_ball_y = image_rotation_to_turtle_window(norm_ball_x, norm_ball_y)

        norm_turtle_x = np.interp(turtle_pos.x, [0, turtle_window_width], [0, 1])
        norm_turtle_y = np.interp(turtle_pos.y, [0, turtle_window_height], [0, 1])

        turtle_angular_err, turtle_linear_err = turtle_follow_ball(
            norm_ball_x,
            norm_ball_y,
            norm_turtle_x,
            norm_turtle_y,
            turtle_pos.theta,
        )

        gas = self.pid_linear.calc(turtle_linear_err, dt)
        steer = self.pid_angular.calc(turtle_angular_err, dt)

        if self._logger:
            self._logger.info(f'gas, steer: {round(gas, 2)},\t{round(steer, 2)} rad')

        gas = max(gas, 0)
        return gas, steer
