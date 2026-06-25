import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    pkg_share = get_package_share_directory("amr_slam")
    slam_toolbox_share = get_package_share_directory("slam_toolbox")

    use_sim_time = LaunchConfiguration("use_sim_time")
    slam_params_file = LaunchConfiguration("slam_params_file")
    rviz_config = LaunchConfiguration("rviz_config")

    declare_use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="Use simulation clock from Gazebo",
    )

    declare_slam_params_file = DeclareLaunchArgument(
        "slam_params_file",
        default_value=os.path.join(
            slam_toolbox_share,
            "config",
            "mapper_params_online_async.yaml",
        ),
        description="Official slam_toolbox online async mapper params",
    )

    declare_rviz_config = DeclareLaunchArgument(
        "rviz_config",
        default_value=os.path.join(
            pkg_share,
            "config",
            "slam_toolbox_default.rviz",
        ),
        description="RViz config for continuous SLAM visualization",
    )

    slam_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, "launch", "online_async_slam.launch.py")
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
            "slam_params_file": slam_params_file,
        }.items(),
    )

    rviz_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, "launch", "slam_rviz.launch.py")
        ),
        launch_arguments={
            "use_sim_time": use_sim_time,
            "rviz_config": rviz_config,
        }.items(),
    )

    return LaunchDescription(
        [
            declare_use_sim_time,
            declare_slam_params_file,
            declare_rviz_config,
            slam_launch,
            rviz_launch,
        ]
    )
