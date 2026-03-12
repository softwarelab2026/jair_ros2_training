
import pytest
from image_feeder.image_generator import ImageGenerator
from follower.ball_tracker import BallTracker
from turtlesim.msg import Pose

@pytest.fixture
def image_generator() -> ImageGenerator:
    generator = ImageGenerator(800, 800, 20)
    generator.ball_pos_x = int(generator.image_width / 2)
    generator.ball_pos_y = int(generator.image_height / 2)
    return generator

@pytest.fixture
def ball_tracker() -> BallTracker:
    return BallTracker(None)

@pytest.fixture
def turtle_pos() -> Pose:
    pose = Pose(x=11/2, y=11/2, theta=0.0)
    return pose
