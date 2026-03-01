import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image


class Follower(Node):
    FPS = 30

    def __init__(self) -> None:
        super().__init__('turtle_follower')
        self.subscription = self.create_subscription(Image, 'camera/raw_image', self._handle_image, 10)

    def _handle_image(self, img: Image) -> None:
        self.get_logger().info(f'I got an image: "{img.data}"')

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
