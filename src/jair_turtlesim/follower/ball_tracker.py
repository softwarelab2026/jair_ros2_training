import numpy as np
from cv_bridge import CvBridge
from follower.pid import PID
from follower.tracker import calc_turtle_error
from rclpy.impl.rcutils_logger import RcutilsLogger
from sensor_msgs.msg import Image
from turtlesim.msg import Pose


def _ros_img_to_cv2(_frame: Image) -> np.ndarray:
    return CvBridge().imgmsg_to_cv2(_frame, desired_encoding='passthrough')


# pylint: disable=too-few-public-methods
class BallTracker:
    def __init__(self, logger: RcutilsLogger):
        self.pid_linear = PID(2, 0.05, 0.01, 10)
        self.pid_angular = PID(12, 0.05, 0.01, 10)

        self._logger = logger

    def track_ball(self, _frame: Image, turtle_pos: Pose, dt: float) -> tuple[float, float]:
        turtle_angular_err, turtle_linear_err = calc_turtle_error(
            _ros_img_to_cv2(_frame),
            _frame.width,
            _frame.height,
            turtle_pos,
        )

        gas = self.pid_linear.calc(turtle_linear_err, dt)
        steer = self.pid_angular.calc(turtle_angular_err, dt)

        if self._logger:
            self._logger.info(f'gas, steer: {round(gas, 2)},\t{round(steer, 2)} rad')

        gas = max(gas, 0)
        return gas, steer
