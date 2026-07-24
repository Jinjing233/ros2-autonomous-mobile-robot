from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    canny_threshold1 = LaunchConfiguration("canny_threshold1")
    canny_threshold2 = LaunchConfiguration("canny_threshold2")
    gaussian_blur_kernel_size = LaunchConfiguration("gaussian_blur_kernel_size")
    gaussian_blur_sigma = LaunchConfiguration("gaussian_blur_sigma")

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "canny_threshold1",
                default_value="50.0",
                description="Canny lower hysteresis threshold",
            ),
            DeclareLaunchArgument(
                "canny_threshold2",
                default_value="150.0",
                description="Canny upper hysteresis threshold",
            ),
            DeclareLaunchArgument(
                "gaussian_blur_kernel_size",
                default_value="5",
                description="Gaussian blur kernel size (positive odd integer)",
            ),
            DeclareLaunchArgument(
                "gaussian_blur_sigma",
                default_value="0.0",
                description="Gaussian blur sigmaX (0.0 = computed from kernel size)",
            ),
            Node(
                package="amr_vision",
                executable="canny_detector",
                name="amr_vision_canny_detector",
                output="screen",
                parameters=[
                    {
                        "canny_threshold1": canny_threshold1,
                        "canny_threshold2": canny_threshold2,
                        "gaussian_blur_kernel_size": gaussian_blur_kernel_size,
                        "gaussian_blur_sigma": gaussian_blur_sigma,
                    }
                ],
            ),
        ]
    )
