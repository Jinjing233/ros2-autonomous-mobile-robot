"""Sprint 7 Phase 4 / Sprint 8 Phase 2: bring up the full amr_vision pipeline
(gray_converter + canny_detector) against a configurable image source.

This launch file only composes the two existing, independently-launchable nodes.
Node implementations are untouched; Canny parameters are loaded from config/vision.yaml.
The `image_topic` launch argument remaps both nodes' `/image_raw` subscription to an
arbitrary source topic (default: `/image_raw`, i.e. the Gazebo RGB camera), so the
same pipeline can consume e.g. a real camera published under `/real_camera/image_raw`
without any change to gray_converter.py / canny_detector.py.
"""

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    default_vision_config = os.path.join(
        get_package_share_directory("amr_vision"), "config", "vision.yaml"
    )

    vision_config = LaunchConfiguration("vision_config")
    image_topic = LaunchConfiguration("image_topic")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "vision_config",
                default_value=default_vision_config,
                description="Path to the YAML file holding amr_vision node parameters",
            ),
            DeclareLaunchArgument(
                "image_topic",
                default_value="/image_raw",
                description=(
                    "Source image topic remapped to both nodes' /image_raw "
                    "subscription (default: /image_raw, the Gazebo RGB camera)"
                ),
            ),
            Node(
                package="amr_vision",
                executable="gray_converter",
                name="amr_vision_gray_converter",
                output="screen",
                remappings=[("/image_raw", image_topic)],
            ),
            Node(
                package="amr_vision",
                executable="canny_detector",
                name="amr_vision_canny_detector",
                output="screen",
                parameters=[vision_config],
                remappings=[("/image_raw", image_topic)],
            ),
        ]
    )
