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
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (7, 7), 0)

        ret, mask = cv2.threshold(blurred, 75, 255, cv2.THRESH_BINARY)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            area_pos = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(area_pos)

            if radius > 5:
                # self.get_logger().info(f'Circle found at: x={int(x)}, y={int(y)}')
                return (int(x), int(y))
        return (0, 0)

    def _normalize_ball_pos(self, frame: Image, ball_pos_x: int, ball_pos_y: int) -> tuple[float, float]:
        norm_x = np.interp(ball_pos_x, [0, frame.width], [0, 1])
        norm_y = np.interp(ball_pos_y, [0, frame.height], [0, 1])
        return norm_x, norm_y

    def _move_turtle(self, ball_pos_x_norm: float, ball_pos_y_norm: float) -> None:
        pass

    def _handle_image(self, frame: Image) -> None:
        ball_pos_x, ball_pos_y = self._extract_ball_pos(frame)
        norm_ball_pox_x, norm_ball_pox_y = self._normalize_ball_pos(frame, ball_pos_x, ball_pos_y)
        self.get_logger().info(f'ball pos: {round(norm_ball_pox_x, 4)},{round(norm_ball_pox_y, 4)}')
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
