#!/usr/bin/env python3
"""Subscribe /image_raw, convert to grayscale via OpenCV, publish /image_gray."""

import cv2
import rclpy
from cv_bridge import CvBridge, CvBridgeError
from rclpy.node import Node
from sensor_msgs.msg import Image


class GrayConverter(Node):
    def __init__(self) -> None:
        super().__init__("amr_vision_gray_converter")

        self._bridge = CvBridge()
        self._publisher = self.create_publisher(Image, "/image_gray", 10)
        self._subscription = self.create_subscription(
            Image,
            "/image_raw",
            self._on_image,
            10,
        )

    def _on_image(self, msg: Image) -> None:
        try:
            bgr_image = self._bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
        except CvBridgeError as exc:
            self.get_logger().warn(f"cv_bridge conversion failed: {exc}")
            return

        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)

        gray_msg = self._bridge.cv2_to_imgmsg(gray_image, encoding="mono8")
        gray_msg.header = msg.header
        self._publisher.publish(gray_msg)


def main() -> None:
    rclpy.init()
    node = GrayConverter()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
