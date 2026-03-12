import numpy as np
from cv_bridge import CvBridge
from follower.img_detection import extract_ball_pos
from follower.pid import PID
from follower.tracker import calc_turtle_error, normalize_ball_to_turtle_pos
from rclpy.impl.rcutils_logger import RcutilsLogger
from sensor_msgs.msg import Image
from turtlesim.msg import Pose


def _ros_img_to_cv2(_frame: Image) -> np.ndarray:
    return CvBridge().imgmsg_to_cv2(_frame, desired_encoding='passthrough')


# pylint: disable=too-few-public-methods
class BallTracker:
    def __init__(self, logger: RcutilsLogger):
        self._pid_linear = PID(8, 0.05, 0.01, 15)
        self._pid_angular = PID(20, 0.08, 0, 15)

        self._logger = logger

    def track_ball(self, frame: Image, turtle_pos: Pose, dt: float) -> tuple[float, float]:
        ball_x, ball_y = extract_ball_pos(_ros_img_to_cv2(frame))
        norm_ball_x, norm_ball_y = normalize_ball_to_turtle_pos(ball_x, ball_y, frame.width, frame.height)

        turtle_angular_err, turtle_linear_err = calc_turtle_error(
            norm_ball_x,
            norm_ball_y,
            turtle_pos.x,
            turtle_pos.y,
            turtle_pos.theta,
        )

        gas = self._pid_linear.calc(turtle_linear_err, dt)
        steer = self._pid_angular.calc(turtle_angular_err, dt)

        if self._logger:
            self._logger.info(f'gas, steer: {round(gas, 2)},\t{round(steer, 2)} rad')

        gas = max(gas, 0)
        return gas, steer
