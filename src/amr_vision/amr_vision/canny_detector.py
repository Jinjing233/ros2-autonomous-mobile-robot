#!/usr/bin/env python3
"""Subscribe /image_raw, run Gaussian blur + Canny edge detection, publish /image_edges."""

import cv2
import rclpy
from cv_bridge import CvBridge, CvBridgeError
from rcl_interfaces.msg import ParameterDescriptor
from rclpy.node import Node
from sensor_msgs.msg import Image


class CannyDetector(Node):
    def __init__(self) -> None:
        super().__init__("amr_vision_canny_detector")

        self.declare_parameter(
            "canny_threshold1",
            50.0,
            ParameterDescriptor(description="Canny lower hysteresis threshold"),
        )
        self.declare_parameter(
            "canny_threshold2",
            150.0,
            ParameterDescriptor(description="Canny upper hysteresis threshold"),
        )
        self.declare_parameter(
            "gaussian_blur_kernel_size",
            5,
            ParameterDescriptor(
                description="Gaussian blur kernel size (positive odd integer)"
            ),
        )
        self.declare_parameter(
            "gaussian_blur_sigma",
            0.0,
            ParameterDescriptor(
                description="Gaussian blur sigmaX (0.0 = computed from kernel size)"
            ),
        )

        self._bridge = CvBridge()
        self._publisher = self.create_publisher(Image, "/image_edges", 10)
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

        threshold1 = self.get_parameter("canny_threshold1").value
        threshold2 = self.get_parameter("canny_threshold2").value
        kernel_size = self.get_parameter("gaussian_blur_kernel_size").value
        sigma = self.get_parameter("gaussian_blur_sigma").value

        if kernel_size <= 0 or kernel_size % 2 == 0:
            self.get_logger().warn(
                f"gaussian_blur_kernel_size must be a positive odd integer, "
                f"got {kernel_size}; skipping frame"
            )
            return

        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        blurred_image = cv2.GaussianBlur(
            gray_image, (kernel_size, kernel_size), sigma
        )
        edges_image = cv2.Canny(blurred_image, threshold1, threshold2)

        edges_msg = self._bridge.cv2_to_imgmsg(edges_image, encoding="mono8")
        edges_msg.header = msg.header
        self._publisher.publish(edges_msg)


def main() -> None:
    rclpy.init()
    node = CannyDetector()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
