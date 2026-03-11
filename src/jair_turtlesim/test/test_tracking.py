import math

import pytest

from turtlesim.msg import Pose
from jair_turtlesim.follower.tracker import turtle_follow_ball


def test_turtle_middle_ball_in_front(turtle_pos: Pose):
    ball_pos = 11, 11/2
    
    angle, dist = turtle_follow_ball(ball_pos[0], ball_pos[1], turtle_pos.x, turtle_pos.y, turtle_pos.theta)
    
    assert angle == 0.0
    assert dist == 5.5

def test_turtle_middle_ball_in_front_left(turtle_pos: Pose):
    ball_pos = 11, 11
    
    angle, dist = turtle_follow_ball(ball_pos[0], ball_pos[1], turtle_pos.x, turtle_pos.y, turtle_pos.theta)
    
    assert angle == pytest.approx(0.7853981633974483)
    assert dist == pytest.approx(7.7781745930520225)

def test_turtle_middle_ball_in_front_right(turtle_pos: Pose):
    ball_pos = 11, 0
    
    angle, dist = turtle_follow_ball(ball_pos[0], ball_pos[1], turtle_pos.x, turtle_pos.y, turtle_pos.theta)
    
    assert angle == pytest.approx(-0.7853981633974483)
    assert dist == pytest.approx(7.7781745930520225)

def test_turtle_middle_ball_in_back_left(turtle_pos: Pose):
    ball_pos = 0, 11
    
    angle, dist = turtle_follow_ball(ball_pos[0], ball_pos[1], turtle_pos.x, turtle_pos.y, turtle_pos.theta)
    
    assert angle == pytest.approx(2.356194490192344)
    assert dist == pytest.approx(0.0)

def test_turtle_middle_ball_in_back_right(turtle_pos: Pose):
    ball_pos = 0, 0
    
    angle, dist = turtle_follow_ball(ball_pos[0], ball_pos[1], turtle_pos.x, turtle_pos.y, turtle_pos.theta)
    
    assert angle == pytest.approx(-2.356194490192344)
    assert dist == pytest.approx(0.0)

def test_turtle_left_up_looking_down_ball_at_right(turtle_pos: Pose):
    turtle_pos._x = 1
    turtle_pos._y = 10
    turtle_pos._theta = -math.pi / 2 + 0.05
    ball_pos = 0.05, 3
    
    angle, dist = turtle_follow_ball(ball_pos[0], ball_pos[1], turtle_pos.x, turtle_pos.y, turtle_pos.theta)
    
    assert angle == pytest.approx(-0.18489016227079969)
    assert dist == pytest.approx(7.064170156501046)

def test_turtle_right_down_looking_down_ball_at_right_behind(turtle_pos: Pose):
    turtle_pos._x = 10
    turtle_pos._y = 1
    turtle_pos._theta = -math.pi / 2 + 0.05
    ball_pos = 0.05, 3
    
    angle, dist = turtle_follow_ball(ball_pos[0], ball_pos[1], turtle_pos.x, turtle_pos.y, turtle_pos.theta)
    
    assert angle == pytest.approx(-1.819158069919009)
    assert dist == pytest.approx(0)

def test_turtle_right_down_looking_up_ball_left(turtle_pos: Pose):
    turtle_pos._x = 10
    turtle_pos._y = 3
    turtle_pos._theta = math.pi / 2
    ball_pos = 1, 3.5
    
    angle, dist = turtle_follow_ball(ball_pos[0], ball_pos[1], turtle_pos.x, turtle_pos.y, turtle_pos.theta)
    
    assert angle == pytest.approx(1.5152978215491792)
    assert dist == pytest.approx(9.013878188659973)
