import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    GroupAction,
    IncludeLaunchDescription,
    TimerAction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    bringup_dir = get_package_share_directory("nav2_bringup")
    pkg_share = get_package_share_directory("amr_navigation")
    bringup_launch_dir = os.path.join(bringup_dir, "launch")
    amr_launch_dir = os.path.join(pkg_share, "launch")

    namespace = LaunchConfiguration("namespace")
    map_yaml_file = LaunchConfiguration("map")
    use_sim_time = LaunchConfiguration("use_sim_time")
    params_file = LaunchConfiguration("params_file")
    autostart = LaunchConfiguration("autostart")
    use_composition = LaunchConfiguration("use_composition")
    use_respawn = LaunchConfiguration("use_respawn")

    declare_namespace = DeclareLaunchArgument(
        "namespace",
        default_value="",
        description="Top-level namespace",
    )

    declare_map = DeclareLaunchArgument(
        "map",
        default_value=os.path.join(pkg_share, "maps", "amr_map.yaml"),
        description="Full path to Sprint 4 saved map yaml",
    )

    declare_use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="Use simulation clock (true when running with Gazebo)",
    )

    declare_params_file = DeclareLaunchArgument(
        "params_file",
        default_value=os.path.join(pkg_share, "config", "amr_nav2_params.yaml"),
        description="AMR nav2 params (official baseline + TF/topic names only)",
    )

    declare_autostart = DeclareLaunchArgument(
        "autostart",
        default_value="true",
        description="Automatically activate Nav2 lifecycle nodes",
    )

    declare_use_composition = DeclareLaunchArgument(
        "use_composition",
        default_value="False",
        description="Use composed bringup if True",
    )

    declare_use_respawn = DeclareLaunchArgument(
        "use_respawn",
        default_value="False",
        description="Respawn crashed nodes when composition is disabled",
    )

    declare_navigation_delay = DeclareLaunchArgument(
        "navigation_delay",
        default_value="8.0",
        description=(
            "Seconds to wait after localization before starting navigation "
            "(map_server + AMCL map->odom must be ready before planner_server)"
        ),
    )

    navigation_delay = LaunchConfiguration("navigation_delay")

    localization_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(bringup_launch_dir, "localization_launch.py")
        ),
        launch_arguments={
            "namespace": namespace,
            "map": map_yaml_file,
            "use_sim_time": use_sim_time,
            "autostart": autostart,
            "params_file": params_file,
            "use_composition": use_composition,
            "use_respawn": use_respawn,
            "container_name": "nav2_container",
        }.items(),
    )

    navigation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(amr_launch_dir, "amr_nav2_navigation.launch.py")
        ),
        launch_arguments={
            "namespace": namespace,
            "use_sim_time": use_sim_time,
            "autostart": autostart,
            "params_file": params_file,
            "use_composition": use_composition,
            "use_respawn": use_respawn,
            "container_name": "nav2_container",
        }.items(),
    )

    return LaunchDescription(
        [
            declare_namespace,
            declare_map,
            declare_use_sim_time,
            declare_params_file,
            declare_autostart,
            declare_use_composition,
            declare_use_respawn,
            declare_navigation_delay,
            GroupAction(
                [
                    localization_launch,
                    TimerAction(
                        period=navigation_delay,
                        actions=[navigation_launch],
                    ),
                ]
            ),
        ]
    )
