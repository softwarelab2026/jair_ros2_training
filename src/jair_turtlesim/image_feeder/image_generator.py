import random

import cv2  # pylint: disable=import-error
import numpy as np  # pylint: disable=import-error


def limit(_value: int, _min: int, _max: int) -> int:
    _value = max(_min, _value)
    _value = min(_max, _value)
    return _value


def get_sign(value: int) -> int:
    return limit(value, -1, 1)


# pylint: disable=too-few-public-methods
class ImageGenerator:
    def __init__(self, width: int = 800, height: int = 800, ball_radius: int = 20):
        self.image_width = width
        self.image_height = height
        self.ball_radius = ball_radius

        self._ball_pos_x = random.randint(self.ball_radius, self.image_width - self.ball_radius)
        self._ball_pos_y = random.randint(self.ball_radius, self.image_height - self.ball_radius)
        self._ball_jumps_x = -5
        self._ball_jumps_y = 5

    def _move_ball(self) -> tuple[int, int]:
        if self._ball_pos_x <= self.ball_radius or self._ball_pos_x + self.ball_radius >= self.image_height:
            self._ball_jumps_x *= -1
            self._ball_jumps_x = get_sign(self._ball_jumps_x) * random.randint(4, 8)
        elif self._ball_pos_y <= self.ball_radius or self._ball_pos_y + self.ball_radius >= self.image_width:
            self._ball_jumps_y *= -1
            self._ball_jumps_y = get_sign(self._ball_jumps_y) * random.randint(4, 7)

        self._ball_pos_x += self._ball_jumps_x
        self._ball_pos_y += self._ball_jumps_y
        self._ball_pos_x = limit(self._ball_pos_x, self.ball_radius, self.image_width - self.ball_radius)
        self._ball_pos_y = limit(self._ball_pos_y, self.ball_radius, self.image_height - self.ball_radius)

        return self._ball_pos_x, self._ball_pos_y

    def render_frame(self) -> np.ndarray:
        black_img = np.zeros((self.image_height, self.image_width, 3), np.uint8)

        cv2.circle(black_img, self._move_ball(), self.ball_radius, color=(0, 255, 0), thickness=-1)
        return black_img
