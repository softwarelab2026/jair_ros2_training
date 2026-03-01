import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image


class ImageFeeder(Node):
    FPS = 25
    IMG_WIDTH = 500
    IMG_HEIGHT = 800
    BALL_RADIUS = 20

    def __init__(self) -> None:
        super().__init__('image_feeder_raw')
        self.publisher_ = self.create_publisher(Image, 'camera/raw_image', 10)
        timer_period = 1 / self.FPS
        self.timer = self.create_timer(timer_period, self._publish_img)

        self._ball_pos_x = int(self.IMG_HEIGHT / 2)
        self._ball_pos_y = int(self.IMG_WIDTH / 2)
        self._ball_dir_x = 5
        self._ball_dir_y = -5

        # img = self._create_img(self.IMG_WIDTH, self.IMG_HEIGHT)
        # self._show_image(img)

    def __delete__(self, instance):
        cv2.destroyAllWindows()

    def _show_image(self, img) -> None:
        cv2.imshow('Image', img)
        cv2.waitKey(1)

    def _get_ball_pos(self) -> tuple[int, int]:
        if self._ball_pos_x <= self.BALL_RADIUS or self._ball_pos_x + self.BALL_RADIUS >= self.IMG_HEIGHT:
            self._ball_dir_x *= -1
        elif self._ball_pos_y <= self.BALL_RADIUS or self._ball_pos_y + self.BALL_RADIUS >= self.IMG_WIDTH:
            self._ball_dir_y *= -1

        self._ball_pos_x += self._ball_dir_x
        self._ball_pos_y += self._ball_dir_y

        return self._ball_pos_x, self._ball_pos_y

    def _publish_img(self):
        img = self._create_img(self.IMG_WIDTH, self.IMG_HEIGHT)
        self.get_logger().info('Publishing: image')
        self.publisher_.publish(CvBridge().cv2_to_imgmsg(img))
        self._show_image(img)

    def _create_img(self, height: int, width: int) -> None:
        black_img = np.zeros((height, width, 3), np.uint8)

        circle_pos = (int(height / 2), int(width / 2))
        cv2.circle(black_img, self._get_ball_pos(), self.BALL_RADIUS, color=(0, 255, 0), thickness=-1)
        return black_img


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)

    image_feeder = ImageFeeder()

    rclpy.spin(image_feeder)

    image_feeder.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
