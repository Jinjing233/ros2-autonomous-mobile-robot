"""Sprint 8 Phase 4: single-command real-camera vision pipeline.

This launch file performs no camera or OpenCV work itself — it only composes
two already-existing, independently-launchable launch files:

  - amr_camera_input/launch/real_camera.launch.py   (official v4l2_camera node)
  - amr_vision/launch/perception.launch.py           (gray_converter + canny_detector)

`amr_vision`'s `image_topic` is pinned to `/real_camera/image_raw` so the
vision pipeline consumes the real camera instead of the Gazebo-published
`/image_raw`. `video_device`, `image_width`, `image_height`, and `frame_rate`
are forwarded to `amr_camera_input`'s launch file unchanged.

Does not touch Gazebo, Nav2, SLAM, or ros2_control.

Camera calibration note: `amr_camera_input`/`v4l2_camera` reports
"Camera calibration file ... not found" at startup (no calibration file is
shipped or fabricated by this package). `/real_camera/camera_info` is
therefore published with an uncalibrated (identity/zero) intrinsics matrix.
This is recorded here as a known gap, not silently worked around.
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    video_device = LaunchConfiguration("video_device")
    image_width = LaunchConfiguration("image_width")
    image_height = LaunchConfiguration("image_height")
    frame_rate = LaunchConfiguration("frame_rate")

    real_camera_launch = PathJoinSubstitution(
        [FindPackageShare("amr_camera_input"), "launch", "real_camera.launch.py"]
    )
    vision_perception_launch = PathJoinSubstitution(
        [FindPackageShare("amr_vision"), "launch", "perception.launch.py"]
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "video_device",
                default_value="/dev/video0",
                description="Forwarded to amr_camera_input real_camera.launch.py",
            ),
            DeclareLaunchArgument(
                "image_width",
                default_value="640",
                description="Forwarded to amr_camera_input real_camera.launch.py",
            ),
            DeclareLaunchArgument(
                "image_height",
                default_value="480",
                description="Forwarded to amr_camera_input real_camera.launch.py",
            ),
            DeclareLaunchArgument(
                "frame_rate",
                default_value="30",
                description=(
                    "Forwarded to amr_camera_input real_camera.launch.py "
                    "(informational only there — v4l2_camera has no frame_rate parameter)"
                ),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(real_camera_launch),
                launch_arguments={
                    "video_device": video_device,
                    "image_width": image_width,
                    "image_height": image_height,
                    "frame_rate": frame_rate,
                }.items(),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(vision_perception_launch),
                launch_arguments={
                    "image_topic": "/real_camera/image_raw",
                }.items(),
            ),
        ]
    )
