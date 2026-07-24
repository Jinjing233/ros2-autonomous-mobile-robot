"""Sprint 7 Phase 4: bring up the full amr_vision pipeline (gray_converter + canny_detector).

This launch file only composes the two existing, independently-launchable nodes.
Node implementations are untouched; Canny parameters are loaded from config/vision.yaml.
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

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "vision_config",
                default_value=default_vision_config,
                description="Path to the YAML file holding amr_vision node parameters",
            ),
            Node(
                package="amr_vision",
                executable="gray_converter",
                name="amr_vision_gray_converter",
                output="screen",
            ),
            Node(
                package="amr_vision",
                executable="canny_detector",
                name="amr_vision_canny_detector",
                output="screen",
                parameters=[vision_config],
            ),
        ]
    )
