import random

import cv2  # pylint: disable=import-error
import numpy as np  # pylint: disable=import-error


def get_sign(value: int) -> int:
    return int(np.clip(value, -1, 1))


class ImageGenerator:
    def __init__(self, width: int = 800, height: int = 800, ball_radius: int = 20):
        self._image_width = width
        self._image_height = height
        self._ball_radius = ball_radius

        self.ball_pos_x = random.randint(self._ball_radius, self._image_width - self._ball_radius)
        self.ball_pos_y = random.randint(self._ball_radius, self._image_height - self._ball_radius)
        self._ball_jumps_x = -5
        self._ball_jumps_y = 5

    def _move_ball(self) -> tuple[int, int]:
        if self.ball_pos_x <= self._ball_radius or self.ball_pos_x + self._ball_radius >= self._image_height:
            self._ball_jumps_x = -1 * get_sign(self._ball_jumps_x) * random.randint(4, 8)
        elif self.ball_pos_y <= self._ball_radius or self.ball_pos_y + self._ball_radius >= self._image_width:
            self._ball_jumps_y = -1 * get_sign(self._ball_jumps_y) * random.randint(4, 8)

        self.ball_pos_x += self._ball_jumps_x
        self.ball_pos_y += self._ball_jumps_y
        self.ball_pos_x = np.clip(self.ball_pos_x, self._ball_radius, self._image_width - self._ball_radius)
        self.ball_pos_y = np.clip(self.ball_pos_y, self._ball_radius, self._image_height - self._ball_radius)

        return self.ball_pos_x, self.ball_pos_y

    def render_current_state(self) -> np.ndarray:
        black_img = np.zeros((self._image_height, self._image_width, 3), np.uint8)

        cv2.circle(black_img, (self.ball_pos_x, self.ball_pos_y), self._ball_radius, color=(0, 255, 0), thickness=-1)
        return black_img

    def render_frame(self) -> np.ndarray:
        self._move_ball()
        return self.render_current_state()
