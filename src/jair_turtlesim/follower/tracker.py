import math

import numpy as np
from follower.img_detection import extract_ball_pos
from turtlesim.msg import Pose


def image_rotation_to_turtle_window(ball_x: float, ball_y: float) -> tuple[float, float]:
    ball_y = 11 - ball_y
    return ball_x, ball_y


def calc_distance(ball_x: float, ball_y: float, turtle_x: float, turtle_y: float) -> float:
    x_dist = ball_x - turtle_x
    y_dist = ball_y - turtle_y
    dist = math.sqrt(y_dist**2 + x_dist**2)
    return dist


def _turn_with_closest_angle(angle_diff: float) -> float:
    coterminal_angle_plus = angle_diff + 2 * math.pi
    coterminal_angle_minus = angle_diff - 2 * math.pi

    coterminal_angle_plus = coterminal_angle_plus % (2 * math.pi)
    coterminal_angle_minus = coterminal_angle_minus % (-2 * math.pi)

    if abs(coterminal_angle_plus) < abs(coterminal_angle_minus):
        return coterminal_angle_plus
    return coterminal_angle_minus


def _calc_turn_angle(ball_x: float, ball_y: float, turtle_x: float, turtle_y: float, turtle_theta_rad: float) -> float:
    x_dist = ball_x - turtle_x
    y_dist = ball_y - turtle_y
    ball_angle = math.atan2(y_dist, x_dist)
    return _turn_with_closest_angle(ball_angle - turtle_theta_rad)


def ball_behind_turtle(ball_angle: float) -> bool:
    return abs(ball_angle) > math.pi / 2


def calc_turtle_error_norm(
    ball_x: float,
    ball_y: float,
    turtle_x: float,
    turtle_y: float,
    turtle_theta_rad: float,
) -> tuple[float, float]:
    turn_angle = _calc_turn_angle(ball_x, ball_y, turtle_x, turtle_y, turtle_theta_rad)
    dist = calc_distance(ball_x, ball_y, turtle_x, turtle_y)

    if ball_behind_turtle(turn_angle):
        dist = 0

    return turn_angle, dist


def calc_turtle_error(frame: np.ndarray, frame_width: int, frame_height: int, turtle_pos: Pose) -> tuple[float, float]:
    turtle_window_width, turtle_window_height = 11, 11

    ball_x, ball_y = extract_ball_pos(frame)
    norm_ball_x = np.interp(ball_x, [0, frame_width], [0, turtle_window_width])
    norm_ball_y = np.interp(ball_y, [0, frame_height], [0, turtle_window_height])
    norm_ball_x, norm_ball_y = image_rotation_to_turtle_window(norm_ball_x, norm_ball_y)

    turtle_angular_err, turtle_linear_err = calc_turtle_error_norm(
        norm_ball_x,
        norm_ball_y,
        turtle_pos.x,
        turtle_pos.y,
        turtle_pos.theta,
    )
    return turtle_angular_err, turtle_linear_err
