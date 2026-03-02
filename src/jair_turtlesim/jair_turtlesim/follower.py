import cv2
import numpy as np
import rclpy
from cv_bridge import CvBridge
from rclpy.node import Node
from sensor_msgs.msg import Image
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist


class Follower(Node):
    FPS = 30

    def __init__(self) -> None:
        super().__init__('turtle_follower')
        self.sub_img = self.create_subscription(Image, 'camera/raw_image', self._handle_image, 10)
        self.sub_pos = self.create_subscription(Pose, '/turtle1/pose', self._get_turtle_pose, 10)
        self.pub_turtle_vel = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.turtle_pos = Pose()

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

    def _normalize_turtle_pos(self) -> tuple[float, float, float]:
        norm_x = np.interp(self.turtle_pos.x, [0, 11], [0, 1])
        norm_y = np.interp(self.turtle_pos.y, [0, 11], [0, 1])
        return norm_x, norm_y, self.turtle_pos.theta

    def _move_turtle(self, ball_pos_x_norm: float, ball_pos_y_norm: float,
                     norm_turtle_pos_x: float, norm_turtle_pos_y: float) -> None:
        twist_msg = Twist()
        twist_msg.angular.z = 1.0
        twist_msg.linear.x = 1.0
        # twist_msg.linear.y = 1.0 # to the side
        self.pub_turtle_vel.publish(twist_msg)

    def _handle_image(self, frame: Image) -> None:
        ball_pos_x, ball_pos_y = self._extract_ball_pos(frame)
        norm_ball_pos_x, norm_ball_pos_y = self._normalize_ball_pos(frame, ball_pos_x, ball_pos_y)
        norm_turtle_pos_x, norm_turtle_pos_y, norm_turtle_theta = self._normalize_turtle_pos()
        self.get_logger().info(f'ball pos: {round(norm_ball_pos_x, 4)},{round(norm_ball_pos_y, 4)}')
        self.get_logger().info(f'turtle pos: {round(norm_turtle_pos_x, 4)},{round(norm_turtle_pos_y, 4)}')
        self._move_turtle(norm_ball_pos_x, norm_ball_pos_y, norm_turtle_pos_x, norm_turtle_pos_y)

    def follow(self) -> None:
        pass

    def _get_turtle_pose(self, turtle_pos:Pose) -> None:
        self.turtle_pos = turtle_pos
        self.get_logger().info(f"got turtle pos: {turtle_pos}")

def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    follower = Follower()
    rclpy.spin(follower)
    follower.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
