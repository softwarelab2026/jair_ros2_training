import pytest

from image_feeder.image_generator import ImageGenerator
from follower.ball_tracker import BallTracker

def test_ball_detection_image_center(image_generator:ImageGenerator, ball_tracker:BallTracker):
    center = int(image_generator.image_width / 2), int(image_generator.image_height / 2)
    
    image_generator._ball_pos_x = center[0]
    image_generator._ball_pos_y = center[1]

    img = image_generator._render_current_state()
    ball_pos = ball_tracker._extract_ball_pos(img)
    
    assert ball_pos == center

def test_dummy():
    assert True
