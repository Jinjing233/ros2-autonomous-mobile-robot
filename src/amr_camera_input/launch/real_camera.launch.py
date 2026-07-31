"""Sprint 8 Phase 3: bring up the real (physical) camera via the official
ROS2 Humble `v4l2_camera` node.

This package writes no custom camera driver; it only configures and launches
the upstream `v4l2_camera` node and remaps its output to a dedicated namespace
so it never collides with the Gazebo-published `/image_raw` topic used by
`amr_vision` / `amr_gazebo`.

Published topics:
  /real_camera/image_raw
  /real_camera/camera_info

Parameter names below were confirmed against the actually-installed
`ros-humble-v4l2-camera` (0.6.2) node via `ros2 param list` on a running
instance, not guessed:
  - `video_device`  (string)                — matches 1:1.
  - `image_size`    (integer array [W, H])  — there is NO separate
    `image_width` / `image_height` parameter in this v4l2_camera version.
    This launch file exposes `image_width` / `image_height` as convenience
    launch arguments and composes them into the real `image_size` parameter.
  - `frame_rate` does not exist as a parameter in this v4l2_camera version.
    It is exposed here only as an informational launch argument (default 30,
    matching the confirmed 30 fps capability of the tested camera at
    640x480 YUYV/MJPG); it is NOT forwarded to the node, since no such
    parameter exists to forward it to. Actual frame rate is fixed by the
    (pixel_format, image_size) pair the device negotiates.
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo, OpaqueFunction
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def _launch_v4l2_camera(context, *args, **kwargs):
    """Build the v4l2_camera Node after resolving launch arguments to real
    Python values. image_width/image_height must be resolved to actual
    integers here (not left as LaunchConfiguration substitutions inside a
    list) because ROS2 rejects a mixed-type / stringified list for the
    'image_size' integer-array parameter (InvalidParameterTypeException).
    """
    video_device = LaunchConfiguration("video_device").perform(context)
    image_width = int(LaunchConfiguration("image_width").perform(context))
    image_height = int(LaunchConfiguration("image_height").perform(context))
    camera_config = LaunchConfiguration("camera_config").perform(context)

    node = Node(
        package="v4l2_camera",
        executable="v4l2_camera_node",
        name="v4l2_camera",
        output="screen",
        parameters=[
            camera_config,
            {
                "video_device": video_device,
                "image_size": [image_width, image_height],
            },
        ],
        remappings=[
            ("image_raw", "/real_camera/image_raw"),
            ("camera_info", "/real_camera/camera_info"),
        ],
    )
    return [node]


def generate_launch_description():
    frame_rate = LaunchConfiguration("frame_rate")

    default_camera_config = PathJoinSubstitution(
        [FindPackageShare("amr_camera_input"), "config", "real_camera.yaml"]
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "video_device",
                default_value="/dev/video0",
                description="V4L2 device path (v4l2_camera parameter: video_device)",
            ),
            DeclareLaunchArgument(
                "image_width",
                default_value="640",
                description=(
                    "Requested image width; composed with image_height into "
                    "the v4l2_camera 'image_size' [W, H] parameter"
                ),
            ),
            DeclareLaunchArgument(
                "image_height",
                default_value="480",
                description=(
                    "Requested image height; composed with image_width into "
                    "the v4l2_camera 'image_size' [W, H] parameter"
                ),
            ),
            DeclareLaunchArgument(
                "frame_rate",
                default_value="30",
                description=(
                    "Informational only: v4l2_camera 0.6.2 has no 'frame_rate' "
                    "parameter, so this value is NOT forwarded to the node. "
                    "Actual frame rate is fixed by the (pixel_format, image_size) "
                    "pair reported by the device (30 fps confirmed for "
                    "640x480 YUYV/MJPG on the tested camera)."
                ),
            ),
            DeclareLaunchArgument(
                "camera_config",
                default_value=default_camera_config,
                description=(
                    "Base v4l2_camera parameters YAML (pixel_format, "
                    "output_encoding, camera_frame_id, etc.); video_device "
                    "and image_size below override this file's values."
                ),
            ),
            LogInfo(
                msg=[
                    "amr_camera_input: 'frame_rate' launch argument (",
                    frame_rate,
                    ") is informational only and is not forwarded to "
                    "v4l2_camera — no such parameter exists in this version.",
                ]
            ),
            OpaqueFunction(function=_launch_v4l2_camera),
        ]
    )
