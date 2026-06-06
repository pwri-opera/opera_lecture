#!/usr/bin/env python3

import time

import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node

from turtlesim.action import RotateAbsolute


class SampleActionServer(Node):
    def __init__(self):
        super().__init__("sample_action_server")

        self._action_server = ActionServer(
            self,
            RotateAbsolute,
            "rotate_absolute_sample",
            self.execute_callback,
        )

        self.get_logger().info("Sample action server started.")
        self.get_logger().info("Action name: /rotate_absolute_sample")
        self.get_logger().info("Action type: turtlesim/action/RotateAbsolute")

    def execute_callback(self, goal_handle):
        target = goal_handle.request.theta

        self.get_logger().info(f"Received goal: theta = {target:.3f}")

        feedback_msg = RotateAbsolute.Feedback()

        steps = 20
        start_value = 0.0

        for i in range(steps + 1):
            ratio = i / steps

            current_value = start_value + ratio * (target - start_value)
            remaining = target - current_value

            feedback_msg.remaining = remaining

            goal_handle.publish_feedback(feedback_msg)

            self.get_logger().info(
                f"Feedback: current = {current_value:.3f}, "
                f"remaining = {remaining:.3f}"
            )

            time.sleep(0.2)

        goal_handle.succeed()

        result = RotateAbsolute.Result()
        result.delta = target - start_value

        self.get_logger().info(f"Result: delta = {result.delta:.3f}")
        self.get_logger().info("Goal succeeded.")

        return result


def main(args=None):
    rclpy.init(args=args)

    node = SampleActionServer()

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