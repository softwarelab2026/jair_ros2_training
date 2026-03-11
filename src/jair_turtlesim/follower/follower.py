import rclpy
from follower.ball_tracker import BallTracker
from geometry_msgs.msg import Twist
from rclpy.node import Node
from sensor_msgs.msg import Image
from turtlesim.msg import Pose


class Follower(Node):
    FPS = 30

    def __init__(self) -> None:
        super().__init__('turtle_follower')
        self.sub_img = self.create_subscription(Image, 'camera/raw_image', self._handle_image, 10)
        self.sub_pos = self.create_subscription(Pose, '/turtle1/pose', self._get_turtle_pose, 10)
        self.pub_turtle_vel = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)

        self.turtle_pos = Pose()
        self._ball_tracker = BallTracker(self.get_logger())

    def _handle_image(self, frame: Image) -> None:
        gas, steer = self._ball_tracker.track_ball(frame, self.turtle_pos)

        twist_msg = Twist()
        twist_msg.angular.z = float(steer)
        twist_msg.linear.x = float(gas)
        # twist_msg.linear.y = 1.0 # to the side
        self.pub_turtle_vel.publish(twist_msg)

    def _get_turtle_pose(self, turtle_pos: Pose) -> None:
        self.turtle_pos = turtle_pos
        # self.get_logger().info(f'got turtle pos: {turtle_pos}')


def main(args: list[str] | None = None) -> None:
    rclpy.init(args=args)
    follower = Follower()
    rclpy.spin(follower)
    follower.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
