import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LifecycleNode, Node


def generate_launch_description():
    pkg_share = get_package_share_directory("amr_navigation")

    use_sim_time = LaunchConfiguration("use_sim_time")
    map_yaml_file = LaunchConfiguration("map")
    namespace = LaunchConfiguration("namespace")

    declare_use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="false",
        description="Use simulation clock (set true when running with Gazebo)",
    )

    declare_namespace = DeclareLaunchArgument(
        "namespace",
        default_value="",
        description="Top-level namespace for map_server",
    )

    declare_map = DeclareLaunchArgument(
        "map",
        default_value=os.path.join(pkg_share, "maps", "amr_map.yaml"),
        description="Full path to Sprint 4 saved map yaml (amr_map.yaml)",
    )

    lifecycle_nodes = ["map_server"]

    load_map_server = GroupAction(
        [
            LifecycleNode(
                package="nav2_map_server",
                executable="map_server",
                name="map_server",
                namespace=namespace,
                output="screen",
                parameters=[
                    {
                        "use_sim_time": use_sim_time,
                        "yaml_filename": map_yaml_file,
                    }
                ],
            ),
            Node(
                package="nav2_lifecycle_manager",
                executable="lifecycle_manager",
                name="lifecycle_manager_map_server",
                output="screen",
                parameters=[
                    {
                        "use_sim_time": use_sim_time,
                        "autostart": True,
                        "node_names": lifecycle_nodes,
                    }
                ],
            ),
        ]
    )

    return LaunchDescription(
        [
            declare_use_sim_time,
            declare_namespace,
            declare_map,
            load_map_server,
        ]
    )
