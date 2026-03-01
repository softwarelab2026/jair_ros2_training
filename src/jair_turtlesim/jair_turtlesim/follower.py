import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image


class Follower(Node):
    FPS = 30

    def __init__(self) -> None:
        super().__init__('turtle_follower')
        self.subscription = self.create_subscription(Image, 'camera/raw_image', self._handle_image, 10)

    def _extract_ball_pos(self, frame: Image) -> tuple[int, int]:
        frame = CvBridge().imgmsg_to_cv2(frame, desired_encoding='passthrough')

        low_color = np.array([0, 200, 0])
        high_color = np.array([255, 255, 255])

        mask = cv2.inRange(frame, low_color, high_color)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            area_pos = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(area_pos)

            if radius > 5:
                self.get_logger().info(f'Circle found at: x={int(x)}, y={int(y)}')
                return (int(x), int(y))
        return (0, 0)

    def _normalize_turtle_pos(self, ball_pos_x: int, ball_pos_y: int) -> tuple[float, float]:
        return (0, 0)

    def _move_turtle(self, ball_pos_x_norm: float, ball_pos_y_norm: float) -> None:
        pass

    def _handle_image(self, frame: Image) -> None:
        self.get_logger().info('I got an image...')
        ball_pos_x, ball_pos_y = self._extract_ball_pos(frame)
        self.get_logger().info(f'ball pos: {ball_pos_x},{ball_pos_y}')
        norm_ball_pox_x, norm_ball_pox_y = self._normalize_turtle_pos(ball_pos_x, ball_pos_y)
        self._move_turtle(norm_ball_pox_x, norm_ball_pox_y)

    def follow(self) -> None:
        pass


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    follower = Follower()
    rclpy.spin(follower)
    follower.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
