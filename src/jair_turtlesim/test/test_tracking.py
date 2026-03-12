import math

import pytest

from image_feeder.image_generator import ImageGenerator
from turtlesim.msg import Pose
from follower.tracker import calc_turtle_error, calc_turtle_error_norm


def test_turtle_middle_ball_in_front(turtle_pos: Pose):
    ball_pos = 11, 11/2
    
    angle, dist = calc_turtle_error_norm(ball_pos[0], ball_pos[1], turtle_pos.x, turtle_pos.y, turtle_pos.theta)
    
    assert angle == 0.0
    assert dist == 5.5

def test_turtle_middle_ball_in_front_left(turtle_pos: Pose):
    ball_pos = 11, 11
    
    angle, _ = calc_turtle_error_norm(ball_pos[0], ball_pos[1], turtle_pos.x, turtle_pos.y, turtle_pos.theta)
    
    assert angle == pytest.approx(math.pi / 4)

def test_turtle_middle_ball_in_front_right(turtle_pos: Pose):
    ball_pos = 11, 0
    
    angle, _ = calc_turtle_error_norm(ball_pos[0], ball_pos[1], turtle_pos.x, turtle_pos.y, turtle_pos.theta)
    
    assert angle == pytest.approx(-math.pi / 4)

def test_turtle_middle_ball_in_back_left(turtle_pos: Pose):
    ball_pos = 0, 11
    
    angle, dist = calc_turtle_error_norm(ball_pos[0], ball_pos[1], turtle_pos.x, turtle_pos.y, turtle_pos.theta)
    
    assert angle == pytest.approx(3/4 * math.pi)
    assert dist == pytest.approx(0.0)

def test_turtle_middle_ball_in_back_right(turtle_pos: Pose):
    ball_pos = 0, 0
    
    angle, dist = calc_turtle_error_norm(ball_pos[0], ball_pos[1], turtle_pos.x, turtle_pos.y, turtle_pos.theta)
    
    assert angle == pytest.approx(-3/4 * math.pi)
    assert dist == pytest.approx(0.0)

def test_turtle_left_up_looking_up_ball_behind():
    turtle_pos = Pose(x=1.0 ,y=10.0, theta=math.pi / 2.0)
    ball_pos = 1, 3
    
    angle, _ = calc_turtle_error_norm(ball_pos[0], ball_pos[1], turtle_pos.x, turtle_pos.y, turtle_pos.theta)
    
    assert angle == pytest.approx(-math.pi)

def test_turtle_right_down_looking_down_ball_at_right_behind():
    turtle_pos = Pose(x=10.0 ,y=1.0, theta=-2 * math.pi)
    ball_pos = 10 - 0.0000001, 3
    
    angle, dist = calc_turtle_error_norm(ball_pos[0], ball_pos[1], turtle_pos.x, turtle_pos.y, turtle_pos.theta)
    
    assert angle == pytest.approx(math.pi / 2 - 0.000001)
    assert dist == pytest.approx(0)

def test_turtle_right_down_looking_up_ball_left():
    turtle_pos = Pose(x=10.0 ,y=3.0, theta=math.pi / 2.0)
    ball_pos = 1, 3
    
    angle, dist = calc_turtle_error_norm(ball_pos[0], ball_pos[1], turtle_pos.x, turtle_pos.y, turtle_pos.theta)
    
    assert angle == pytest.approx(math.pi / 2)
    assert dist == pytest.approx(9)

def test_turtle_right_down_looking_up_ball_not_normalized_left(image_generator: ImageGenerator):
    turtle_pos = Pose(x=10.0 ,y=3.0, theta=math.pi / 2.0)
    ball_pos = 71, 581
    
    image_generator.ball_pos_x = ball_pos[0]
    image_generator.ball_pos_y = ball_pos[1]

    frame = image_generator.render_current_state()
    angle, dist = calc_turtle_error(frame, 800, 800, turtle_pos)
    
    assert angle == pytest.approx(math.pi / 2, rel=0.1)
    assert dist == pytest.approx(9, rel=0.1)

def test_turtle_mid_looking_left_ball_right():
    turtle_pos = Pose(x=5.0 ,y=5.0, theta=math.pi / 2.0)
    ball_pos = 6, 6
    
    _, dist = calc_turtle_error_norm(ball_pos[0], ball_pos[1], turtle_pos.x, turtle_pos.y, turtle_pos.theta)

    assert dist == pytest.approx(math.sqrt(1 + 1))

def test_turtle_mid_looking_right_ball_right():
    turtle_pos = Pose(x=5.0 ,y=5.0, theta=0.0)
    ball_pos = 6, 6
    
    _, dist = calc_turtle_error_norm(ball_pos[0], ball_pos[1], turtle_pos.x, turtle_pos.y, turtle_pos.theta)

    assert dist == pytest.approx(math.sqrt(1 + 1))

def test_turtle_left_looking_up_ball_left_behind():
    turtle_pos = Pose(x=5.0 ,y=5.0, theta=math.pi / 2.0)
    ball_pos = 4, 4
    
    _, dist = calc_turtle_error_norm(ball_pos[0], ball_pos[1], turtle_pos.x, turtle_pos.y, turtle_pos.theta)

    assert dist == 0.0

def test_turtle_right_down_looking_up_ball_left_behind(turtle_pos: Pose):
    turtle_pos = Pose(x=5.0 ,y=5.0, theta=0.0)
    ball_pos = 4, 4
    
    _, dist = calc_turtle_error_norm(ball_pos[0], ball_pos[1], turtle_pos.x, turtle_pos.y, turtle_pos.theta)

    assert dist == 0.0
