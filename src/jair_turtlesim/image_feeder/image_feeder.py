import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String


class ImageFeeder(Node):
    FPS = 30

    def __init__(self):
        super().__init__('image_feeder_raw')
        self.publisher_ = self.create_publisher(Image, 'camera/raw_image', 10)
        timer_period = 1 / self.FPS
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def _create_img(self):
        pass

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        img = Image()
        self.publisher_.publish(img)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


def main(args=None):
    rclpy.init(args=args)

    image_feeder = ImageFeeder()

    rclpy.spin(image_feeder)

    image_feeder.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
