#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node
from tf2_ros import Buffer, TransformListener
from tf2_ros import LookupException, ConnectivityException, ExtrapolationException


def quaternion_to_rpy(qx, qy, qz, qw):
    """
    Quaternionをroll, pitch, yawに変換する。
    授業では詳細な導出は扱わず、表示用の関数として使う。
    """

    # roll
    sinr_cosp = 2.0 * (qw * qx + qy * qz)
    cosr_cosp = 1.0 - 2.0 * (qx * qx + qy * qy)
    roll = math.atan2(sinr_cosp, cosr_cosp)

    # pitch
    sinp = 2.0 * (qw * qy - qz * qx)
    if abs(sinp) >= 1.0:
        pitch = math.copysign(math.pi / 2.0, sinp)
    else:
        pitch = math.asin(sinp)

    # yaw
    siny_cosp = 2.0 * (qw * qz + qx * qy)
    cosy_cosp = 1.0 - 2.0 * (qy * qy + qz * qz)
    yaw = math.atan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw


class LidarTfListener(Node):
    def __init__(self):
        super().__init__("lidar_tf_listener")

        self.target_frame = "body_link"
        self.source_frame = "lidar1"
        # souce_frame(lidar1座標系)の値を target_framen(body_link座標系)の値に変換する

        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)

        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        try:
            transform = self.tf_buffer.lookup_transform(
                self.target_frame,
                self.source_frame,
                rclpy.time.Time()
            )

        except (LookupException, ConnectivityException, ExtrapolationException) as e:
            self.get_logger().warn(
                f"Could not get transform from {self.target_frame} to {self.source_frame}: {e}"
            )
            return

        t = transform.transform.translation
        q = transform.transform.rotation

        roll, pitch, yaw = quaternion_to_rpy(q.x, q.y, q.z, q.w)

        self.get_logger().info(
            "\n"
            f"Transform: {self.target_frame} <- {self.source_frame}\n"
            f"  position [m]\n"
            f"    x: {t.x:.3f}\n"
            f"    y: {t.y:.3f}\n"
            f"    z: {t.z:.3f}\n"
            f"  orientation [deg]\n"
            f"    roll : {math.degrees(roll):.2f}\n"
            f"    pitch: {math.degrees(pitch):.2f}\n"
            f"    yaw  : {math.degrees(yaw):.2f}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = LidarTfListener()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()