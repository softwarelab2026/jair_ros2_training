import math


def calc_distance(ball_x: float, ball_y: float, turtle_x: float, turtle_y: float) -> float:
    x_dist = ball_x - turtle_x
    y_dist = ball_y - turtle_y
    dist = math.sqrt(y_dist**2 + x_dist**2)
    return dist


def turn_with_closest_angle(angle_diff: float) -> float:
    coterminal_angle_plus = angle_diff + 2 * math.pi
    coterminal_angle_minus = angle_diff - 2 * math.pi

    coterminal_angle_plus = coterminal_angle_plus % (2 * math.pi)
    coterminal_angle_minus = coterminal_angle_minus % (-2 * math.pi)

    if abs(coterminal_angle_plus) < abs(coterminal_angle_minus):
        return coterminal_angle_plus
    return coterminal_angle_minus


def calc_turn_angle(ball_x: float, ball_y: float, turtle_x: float, turtle_y: float, turtle_theta_rad: float) -> float:
    x_dist = ball_x - turtle_x
    y_dist = ball_y - turtle_y
    ball_angle = math.atan2(y_dist, x_dist)
    return turn_with_closest_angle(ball_angle - turtle_theta_rad)


def ball_behind_turtle(ball_angle: float) -> bool:
    return abs(ball_angle) > math.pi / 2


def turtle_follow_ball(
    ball_x: float,
    ball_y: float,
    turtle_x: float,
    turtle_y: float,
    turtle_theta_rad: float,
) -> tuple[float, float]:
    turn_angle = calc_turn_angle(ball_x, ball_y, turtle_x, turtle_y, turtle_theta_rad)
    dist = calc_distance(ball_x, ball_y, turtle_x, turtle_y)

    if ball_behind_turtle(turn_angle):
        dist = 0

    return turn_angle, dist
