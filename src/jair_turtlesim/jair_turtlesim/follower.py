import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image

class Follower(Node):
    FPS = 30

    def __init__(self):
        super().__init__('turtle_follower')
        self.subscription = self.create_subscription(Image, 'camera/raw_image', self._handle_image, 10)

    def _handle_image(self, img):
        self.get_logger().info('I got an image: "%s"' % img.data)

    def follow(self):
        pass


def main(args = None):
    rclpy.init(args=args)
    follower = Follower()
    rclpy.spin(follower)
    follower.destroy_node()
    rclpy.shutdown()



if __name__ == '__main__':
    main()
