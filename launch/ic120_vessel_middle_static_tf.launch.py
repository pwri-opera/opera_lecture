from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    parent_frame = LaunchConfiguration('parent_frame')
    child_frame = LaunchConfiguration('child_frame')

    x = LaunchConfiguration('x')
    y = LaunchConfiguration('y')
    z = LaunchConfiguration('z')
    roll = LaunchConfiguration('roll')
    pitch = LaunchConfiguration('pitch')
    yaw = LaunchConfiguration('yaw')

    return LaunchDescription([
        DeclareLaunchArgument(
            'parent_frame',
            default_value='ic120_tf/base_link',
            description='Parent frame ID'
        ),
        DeclareLaunchArgument(
            'child_frame',
            default_value='ic120_tf/vessel_middle_link',
            description='Child frame ID'
        ),
        DeclareLaunchArgument('x', default_value='-1.8'),
        DeclareLaunchArgument('y', default_value='0.0'),
        DeclareLaunchArgument('z', default_value='2.1'),
        DeclareLaunchArgument('roll', default_value='0.0'),
        DeclareLaunchArgument('pitch', default_value='0.0'),
        DeclareLaunchArgument('yaw', default_value='0.0'),

        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='lidar_static_tf_publisher',
            arguments=[
                '--x', x,
                '--y', y,
                '--z', z,
                '--roll', roll,
                '--pitch', pitch,
                '--yaw', yaw,
                '--frame-id', parent_frame,
                '--child-frame-id', child_frame,
            ],
        ),
    ])