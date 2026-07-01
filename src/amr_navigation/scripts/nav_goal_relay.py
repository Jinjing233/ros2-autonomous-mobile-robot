#!/usr/bin/env python3
"""Send NavigateToPose from RViz goal_pose_rviz with sim-time stamp and long action timeout."""

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from geometry_msgs.msg import PoseStamped
from nav2_msgs.action import NavigateToPose


class NavGoalRelay(Node):
    """Reliable NavigateToPose client for Gazebo sim-time bringup."""

    def __init__(self):
        super().__init__("nav_goal_relay")
        self._action_client = ActionClient(self, NavigateToPose, "navigate_to_pose")
        self._goal_handle = None
        self._subscription = self.create_subscription(
            PoseStamped,
            "goal_pose_rviz",
            self._goal_callback,
            10,
        )
        self._action_client.wait_for_server(timeout_sec=30.0)
        self.get_logger().info("nav_goal_relay ready (subscribes /goal_pose_rviz)")

    def _goal_callback(self, msg: PoseStamped) -> None:
        goal = NavigateToPose.Goal()
        goal.pose = msg
        goal.pose.header.stamp = self.get_clock().now().to_msg()
        if not goal.pose.header.frame_id:
            goal.pose.header.frame_id = "map"

        self.get_logger().info(
            "NavigateToPose goal (%.2f, %.2f) frame=%s"
            % (
                goal.pose.pose.position.x,
                goal.pose.pose.position.y,
                goal.pose.header.frame_id,
            )
        )

        if self._goal_handle is not None:
            self.get_logger().info("Canceling previous NavigateToPose goal")
            cancel_future = self._goal_handle.cancel_goal_async()
            cancel_future.add_done_callback(
                lambda _f: self._send_goal(goal)
            )
            return

        self._send_goal(goal)

    def _send_goal(self, goal: NavigateToPose.Goal) -> None:
        send_future = self._action_client.send_goal_async(goal)
        send_future.add_done_callback(self._goal_response_callback)

    def _goal_response_callback(self, future) -> None:
        self._goal_handle = future.result()
        if not self._goal_handle.accepted:
            self.get_logger().error("NavigateToPose goal rejected by bt_navigator")
            self._goal_handle = None
            return

        self.get_logger().info("NavigateToPose goal accepted")


def main(args=None):
    rclpy.init(args=args)
    node = NavGoalRelay()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
