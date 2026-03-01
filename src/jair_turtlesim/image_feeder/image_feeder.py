import cv2
import numpy as np
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String


class ImageFeeder(Node):
    FPS = 30
    IMG_WIDTH = 500
    IMG_HEIGHT = 800

    def __init__(self) -> None:
        super().__init__('image_feeder_raw')
        self.publisher_ = self.create_publisher(Image, 'camera/raw_image', 10)
        timer_period = 1 / self.FPS
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

        img = self._create_img(self.IMG_WIDTH, self.IMG_HEIGHT)
        self._show_image(img)

    def _show_image(self, img) -> None:
        cv2.imshow('Black Image', img)
        # cv2.waitKey(0)
        cv2.destroyAllWindows()

    def _create_img(self, height: int, width: int) -> None:
        black_img = np.zeros((height, width, 3), np.uint8)

        circle_pos = (int(height / 2), int(width / 2))
        radius = 20
        color = (0, 255, 0)
        thickness = -1
        cv2.circle(black_img, circle_pos, radius, color, thickness)

        return black_img

    def timer_callback(self) -> None:
        msg = String()
        msg.data = f'Hello World: {self.i}'
        img = Image()
        self.publisher_.publish(img)
        self.get_logger().info(f'Publishing: "{msg.data}"')
        self.i += 1


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)

    image_feeder = ImageFeeder()

    rclpy.spin(image_feeder)

    image_feeder.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
