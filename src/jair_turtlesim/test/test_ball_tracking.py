
import math

import pytest

from image_feeder.image_generator import ImageGenerator
from follower.ball_tracker import BallTracker
from turtlesim.msg import Pose
from cv_bridge import CvBridge

def test_ball_detection_image_center(image_generator:ImageGenerator, ball_tracker:BallTracker):
    center = int(image_generator.image_width / 2), int(image_generator.image_height / 2)

    image_generator._ball_pos_x = center[0]
    image_generator._ball_pos_y = center[1]

    img = image_generator._render_current_state()
    ball_pos = ball_tracker._extract_ball_pos(img)

    assert ball_pos == center

def test_ball_detection_image_left_up(image_generator:ImageGenerator, ball_tracker:BallTracker):
    exptectd_ball_pos = 200, 200

    image_generator._ball_pos_x = exptectd_ball_pos[0]
    image_generator._ball_pos_y = exptectd_ball_pos[1]

    img = image_generator._render_current_state()
    ball_pos = ball_tracker._extract_ball_pos(img)

    assert ball_pos == exptectd_ball_pos

def test_ball_detection_image_left_down(image_generator:ImageGenerator, ball_tracker:BallTracker):
    exptectd_ball_pos = 200, 600

    image_generator._ball_pos_x = exptectd_ball_pos[0]
    image_generator._ball_pos_y = exptectd_ball_pos[1]

    img = image_generator._render_current_state()
    ball_pos = ball_tracker._extract_ball_pos(img)

    assert ball_pos == exptectd_ball_pos

def test_ball_detection_image_right_up(image_generator:ImageGenerator, ball_tracker:BallTracker):
    exptectd_ball_pos = 700, 600

    image_generator._ball_pos_x = exptectd_ball_pos[0]
    image_generator._ball_pos_y = exptectd_ball_pos[1]

    img = image_generator._render_current_state()
    ball_pos = ball_tracker._extract_ball_pos(img)

    assert ball_pos == exptectd_ball_pos

def test_ball_detection_image_right_down(image_generator:ImageGenerator, ball_tracker:BallTracker):
    exptectd_ball_pos = 700, 600

    image_generator._ball_pos_x = exptectd_ball_pos[0]
    image_generator._ball_pos_y = exptectd_ball_pos[1]

    img = image_generator._render_current_state()
    ball_pos = ball_tracker._extract_ball_pos(img)

    assert ball_pos == exptectd_ball_pos

def test_turtle_middle_ball_left(image_generator:ImageGenerator, ball_tracker:BallTracker, turtle_pos: Pose):
    ball_pos = 400, 700
    exptected_turtle_error = 0.375, -math.pi/2

    image_generator._ball_pos_x = ball_pos[0]
    image_generator._ball_pos_y = ball_pos[1]

    img = image_generator._render_current_state()
    ros_image_msg = CvBridge().cv2_to_imgmsg(img, encoding="bgr8")
    turtle_error = ball_tracker._calc_linear_angular_err(ros_image_msg, turtle_pos)

    assert turtle_error == exptected_turtle_error

def test_turtle_middle_ball_right(image_generator:ImageGenerator, ball_tracker:BallTracker, turtle_pos: Pose):
    ball_pos = 400, 100
    exptected_turtle_error = 0.375, math.pi/2

    image_generator._ball_pos_x = ball_pos[0]
    image_generator._ball_pos_y = ball_pos[1]

    img = image_generator._render_current_state()
    ros_image_msg = CvBridge().cv2_to_imgmsg(img, encoding="bgr8")
    turtle_error = ball_tracker._calc_linear_angular_err(ros_image_msg, turtle_pos)

    assert turtle_error == exptected_turtle_error

def test_turtle_middle_ball_behind_right(image_generator:ImageGenerator, ball_tracker:BallTracker, turtle_pos: Pose):
    ball_pos = 100, 350
    exptected_turtle_error = 0.3801726581436387, 3.141592653589793

    image_generator._ball_pos_x = ball_pos[0]
    image_generator._ball_pos_y = ball_pos[1]

    img = image_generator._render_current_state()
    ros_image_msg = CvBridge().cv2_to_imgmsg(img, encoding="bgr8")
    turtle_error = ball_tracker._calc_linear_angular_err(ros_image_msg, turtle_pos)

    assert turtle_error[0] == pytest.approx(exptected_turtle_error[0])
    assert turtle_error[1] == pytest.approx(exptected_turtle_error[1])
