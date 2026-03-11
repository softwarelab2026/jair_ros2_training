import math

import cv2
import numpy as np
from cv_bridge import CvBridge
from follower.pid import PID
from rclpy.impl.rcutils_logger import RcutilsLogger
from sensor_msgs.msg import Image
from turtlesim.msg import Pose


# pylint: disable=too-few-public-methods
class BallTracker:
    def __init__(self, logger: RcutilsLogger):
        self.pid_linear = PID(5, 0.001, 0.01)
        self.pid_angular = PID(12, 0.02, 0.05)
        self._logger = logger

    def _normalize_turtle_pos(self, turtle_pos: Pose) -> tuple[float, float, float]:
        turtle_window_height = 11
        turtle_window_width = 11
        norm_x = np.interp(turtle_pos.x, [0, turtle_window_width], [0, 1])
        norm_y = np.interp(turtle_pos.y, [0, turtle_window_height], [0, 1])
        return norm_x, norm_y, turtle_pos.theta

    def _normalize_ball_pos(
        self,
        frame_height: int,
        frame_width: int,
        ball_pos_x: int,
        ball_pos_y: int,
    ) -> tuple[float, float]:
        norm_x = np.interp(ball_pos_x, [0, frame_width], [0, 1])
        norm_y = np.interp(ball_pos_y, [0, frame_height], [0, 1])
        return norm_x, norm_y

    def _extract_ball_pos(self, frame: np.ndarray) -> tuple[int, int]:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)

        ret, mask = cv2.threshold(blurred, 75, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            area_pos = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(area_pos)

            if radius > 5:
                # self.get_logger().info(f'Circle found at: x={int(x)}, y={int(y)}')
                return (int(x), int(y))
        return (0, 0)

    def _fix_image_rotation_to_turtle(self, ball_pos_norm: tuple[float, float]) -> tuple[float, float]:
        ball_x, ball_y = ball_pos_norm
        ball_y = 1 - ball_y
        return ball_x, ball_y

    def _ros_img_to_cv2(self, _frame: Image) -> np.ndarray:
        return CvBridge().imgmsg_to_cv2(_frame, desired_encoding='passthrough')

    def _get_ball_pos_norm(self, _frame: Image) -> tuple[float, float]:
        frame_cv2 = self._ros_img_to_cv2(_frame)
        frame_height, frame_width = 800, 800

        ball_x, ball_y = self._extract_ball_pos(frame_cv2)
        norm_ball_x, norm_ball_y = self._normalize_ball_pos(frame_height, frame_width, ball_x, ball_y)
        return norm_ball_x, norm_ball_y

    def _turtle_error(
        self,
        norm_ball_pos: tuple[float, float],
        norm_turtle_pos: tuple[float, float, float],
    ) -> tuple[float, float]:
        turtle_theta_rad = norm_turtle_pos[2]
        x_dist = norm_ball_pos[0] - norm_turtle_pos[0]
        y_dist = norm_ball_pos[1] - norm_turtle_pos[1]
        dist = math.sqrt(y_dist**2 + x_dist**2)

        angle_rad = 0.0
        angle_rad = math.atan(y_dist / x_dist)
        angle_rad = angle_rad - turtle_theta_rad
        # if turtle_theta_rad > math.pi / 2:
        #     angle_rad += math.pi/2
        # if turtle_theta_rad < -math.pi/2:
        #     angle_rad -= math.pi/2

        if self._logger:
            self._logger.info(f'ball angle {round(angle_rad, 2)}')

        return dist, angle_rad

    def _ball_behind_turtle(self, ball_angle: float) -> bool:
        return abs(ball_angle) > math.pi / 2

    def track_ball(self, _frame: Image, turtle_pos: Pose) -> tuple[float, float]:
        ball_pos_norm = self._get_ball_pos_norm(_frame)
        norm_ball_x, norm_ball_y = self._fix_image_rotation_to_turtle(ball_pos_norm)
        norm_turtle_x, norm_turtle_y, turtle_theta = self._normalize_turtle_pos(turtle_pos)

        (turtle_linear_err, turtle_angular_err) = self._turtle_error(
            (norm_ball_x, norm_ball_y),
            (norm_turtle_x, norm_turtle_y, turtle_theta),
        )

        gas = self.pid_linear.calc(turtle_linear_err)
        steer = self.pid_angular.calc(turtle_angular_err)

        if self._logger:
            self._logger.info(f'Ball pos: {round(norm_ball_x, 2)},\t{round(norm_ball_y, 2)}')
            self._logger.info(
                f'turtle pos: {round(norm_turtle_x, 2)}\t,{round(norm_turtle_y, 2)}\ttheta: {round(turtle_theta, 2)}',
            )
            self._logger.info(
                f'Error linear,anglular: {round(turtle_linear_err, 2)},\t{round(turtle_angular_err, 2)} rad',
            )
            self._logger.info(f'gas, steer: {round(gas, 2)},\t{round(steer, 2)} rad')
            self._logger.info(f'ball behind turtle: {self._ball_behind_turtle(turtle_angular_err)}')

        if self._ball_behind_turtle(turtle_angular_err):
            gas = 0

        gas = 0
        # steer = 0

        gas = max(gas, 0)
        return gas, steer
