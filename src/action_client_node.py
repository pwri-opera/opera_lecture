#!/usr/bin/env python3

import argparse

import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

from action_msgs.msg import GoalStatus
from turtlesim.action import RotateAbsolute


class SampleActionClient(Node):
    def __init__(self, action_name: str):
        super().__init__("sample_action_client")

        self._action_client = ActionClient(
            self,
            RotateAbsolute,
            action_name,
        )

    def send_goal(self, theta: float):
        goal_msg = RotateAbsolute.Goal()
        goal_msg.theta = theta

        self.get_logger().info("Waiting for action server...")
        self._action_client.wait_for_server()

        self.get_logger().info(f"Sending goal: theta = {theta:.3f}")

        send_goal_future = self._action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback,
        )

        send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().error("Goal was rejected.")
            rclpy.shutdown()
            return

        self.get_logger().info("Goal accepted.")

        result_future = goal_handle.get_result_async()
        result_future.add_done_callback(self.result_callback)

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback

        self.get_logger().info(
            f"Feedback received: remaining = {feedback.remaining:.3f}"
        )

    def result_callback(self, future):
        result_response = future.result()

        status = result_response.status
        result = result_response.result

        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("Action succeeded.")
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().error("Action aborted.")
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().warn("Action canceled.")
        else:
            self.get_logger().warn(f"Action finished with status: {status}")

        self.get_logger().info(f"Result received: delta = {result.delta:.3f}")

        rclpy.shutdown()


def main(args=None):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--theta",
        type=float,
        default=3.14,
        help="Goal value sent to the action server.",
    )
    parser.add_argument(
        "--action-name",
        type=str,
        default="/rotate_absolute_sample",
        help="Action name.",
    )

    parsed_args, ros_args = parser.parse_known_args()

    rclpy.init(args=ros_args)

    node = SampleActionClient(parsed_args.action_name)
    node.send_goal(parsed_args.theta)

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == "__main__":
    main()