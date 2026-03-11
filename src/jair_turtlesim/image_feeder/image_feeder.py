from typing import Any

import cv2  # pylint: disable=import-error
import numpy as np  # pylint: disable=import-error
import rclpy
from cv_bridge import CvBridge
from image_feeder.image_generator import ImageGenerator
from rclpy.node import Node
from sensor_msgs.msg import Image


# pylint: disable=too-few-public-methods
class ImageFeeder(Node):
    FPS = 25

    def __init__(self) -> None:
        super().__init__('image_feeder_raw')
        self.publisher_ = self.create_publisher(Image, 'camera/raw_image', 10)
        timer_period = 1 / self.FPS
        self.timer = self.create_timer(timer_period, self.publish_img)

        self._img_generator = ImageGenerator(width=800, height=800, ball_radius=20)

    def __delete__(self, instance: Any) -> None:
        cv2.destroyAllWindows()

    def _show_image(self, img: np.ndarray) -> None:
        cv2.imshow('Image', img)
        cv2.waitKey(1)

    def publish_img(self) -> None:
        img = self._img_generator.render_frame()
        self.publisher_.publish(CvBridge().cv2_to_imgmsg(img))
        self._show_image(img)


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)

    image_feeder = ImageFeeder()

    rclpy.spin(image_feeder)

    image_feeder.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
