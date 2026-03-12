import pytest

from image_feeder.image_generator import ImageGenerator
from follower.img_detection import extract_ball_pos

def test_ball_detection_image_right_down(image_generator:ImageGenerator):
    exptectd_ball_pos = 700, 600

    image_generator.ball_pos_x = exptectd_ball_pos[0]
    image_generator.ball_pos_y = exptectd_ball_pos[1]

    img = image_generator.render_current_state()
    ball_pos = extract_ball_pos(img)

    assert ball_pos == exptectd_ball_pos

def test_ball_jumping_on_wall_right(image_generator:ImageGenerator):
    image_generator.ball_pos_x = 680
    image_generator.ball_pos_y = 600

    image_generator.render_frame()
    ball_pos = image_generator.ball_pos_x, image_generator.ball_pos_y

    
    assert ball_pos == (pytest.approx(674, rel=2), 605)

def test_ball_jumping_on_wall_left(image_generator:ImageGenerator):
    image_generator.ball_pos_x = 20
    image_generator.ball_pos_y = 200

    image_generator.render_frame()
    ball_pos = image_generator.ball_pos_x, image_generator.ball_pos_y

    assert ball_pos == (pytest.approx(26, rel=2), 205)

def test_ball_jumping_on_wall_up(image_generator:ImageGenerator):
    image_generator.ball_pos_x = 500
    image_generator.ball_pos_y = 780

    image_generator.render_frame()
    ball_pos = image_generator.ball_pos_x, image_generator.ball_pos_y

    assert ball_pos == (495, pytest.approx(774, rel=2))

def test_ball_jumping_on_wall_down(image_generator:ImageGenerator):
    image_generator.ball_pos_x = 500
    image_generator.ball_pos_y = 20

    image_generator.render_frame()
    ball_pos = image_generator.ball_pos_x, image_generator.ball_pos_y

    assert ball_pos == (495, pytest.approx(26, rel=2))
