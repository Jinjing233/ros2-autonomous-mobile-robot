#!/usr/bin/env python3
"""Bridge /cmd_vel to diff_drive_controller cmd_vel_unstamped with teleop-compatible QoS."""

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node
from rclpy.qos import DurabilityPolicy, HistoryPolicy, QoSProfile, ReliabilityPolicy


class CmdVelRelay(Node):
    def __init__(self) -> None:
        super().__init__("cmd_vel_relay")

        # Match teleop_twist_keyboard and ros2 topic pub defaults: reliable + volatile.
        qos = QoSProfile(
            reliability=ReliabilityPolicy.RELIABLE,
            durability=DurabilityPolicy.VOLATILE,
            history=HistoryPolicy.KEEP_LAST,
            depth=10,
        )

        self._publisher = self.create_publisher(
            Twist,
            "/diff_drive_controller/cmd_vel_unstamped",
            qos,
        )
        self._subscription = self.create_subscription(
            Twist,
            "/cmd_vel",
            self._relay,
            qos,
        )

    def _relay(self, msg: Twist) -> None:
        self._publisher.publish(msg)


def main() -> None:
    rclpy.init()
    node = CmdVelRelay()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
