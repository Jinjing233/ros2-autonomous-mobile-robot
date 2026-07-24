from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="amr_vision",
                executable="gray_converter",
                name="amr_vision_gray_converter",
                output="screen",
            ),
        ]
    )
