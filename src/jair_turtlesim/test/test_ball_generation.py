
import math

import pytest

from image_feeder.image_generator import ImageGenerator
from follower.ball_tracker import BallTracker

def test_ball_detection_image_center(image_generator:ImageGenerator, ball_tracker:BallTracker):
    center = int(image_generator.image_width / 2), int(image_generator.image_height / 2)

    image_generator.ball_pos_x = center[0]
    image_generator.ball_pos_y = center[1]

    img = image_generator.render_current_state()
    ball_pos = ball_tracker.extract_ball_pos(img)

    assert ball_pos == center

def test_ball_detection_image_left_up(image_generator:ImageGenerator, ball_tracker:BallTracker):
    exptectd_ball_pos = 200, 200

    image_generator.ball_pos_x = exptectd_ball_pos[0]
    image_generator.ball_pos_y = exptectd_ball_pos[1]

    img = image_generator.render_current_state()
    ball_pos = ball_tracker.extract_ball_pos(img)

    assert ball_pos == exptectd_ball_pos

def test_ball_detection_image_left_down(image_generator:ImageGenerator, ball_tracker:BallTracker):
    exptectd_ball_pos = 200, 600

    image_generator.ball_pos_x = exptectd_ball_pos[0]
    image_generator.ball_pos_y = exptectd_ball_pos[1]

    img = image_generator.render_current_state()
    ball_pos = ball_tracker.extract_ball_pos(img)

    assert ball_pos == exptectd_ball_pos

def test_ball_detection_image_right_up(image_generator:ImageGenerator, ball_tracker:BallTracker):
    exptectd_ball_pos = 700, 600

    image_generator.ball_pos_x = exptectd_ball_pos[0]
    image_generator.ball_pos_y = exptectd_ball_pos[1]

    img = image_generator.render_current_state()
    ball_pos = ball_tracker.extract_ball_pos(img)

    assert ball_pos == exptectd_ball_pos

def test_ball_detection_image_right_down(image_generator:ImageGenerator, ball_tracker:BallTracker):
    exptectd_ball_pos = 700, 600

    image_generator.ball_pos_x = exptectd_ball_pos[0]
    image_generator.ball_pos_y = exptectd_ball_pos[1]

    img = image_generator.render_current_state()
    ball_pos = ball_tracker.extract_ball_pos(img)

    assert ball_pos == exptectd_ball_pos
