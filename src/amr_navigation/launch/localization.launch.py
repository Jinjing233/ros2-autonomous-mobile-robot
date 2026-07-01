import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import LifecycleNode, Node
from launch_ros.descriptions import ParameterFile
from nav2_common.launch import RewrittenYaml


def generate_launch_description():
    bringup_dir = get_package_share_directory("nav2_bringup")
    pkg_share = get_package_share_directory("amr_navigation")

    namespace = LaunchConfiguration("namespace")
    map_yaml_file = LaunchConfiguration("map")
    use_sim_time = LaunchConfiguration("use_sim_time")
    params_file = LaunchConfiguration("params_file")
    autostart = LaunchConfiguration("autostart")

    declare_namespace = DeclareLaunchArgument(
        "namespace",
        default_value="",
        description="Top-level namespace",
    )

    declare_map = DeclareLaunchArgument(
        "map",
        default_value=os.path.join(pkg_share, "maps", "amr_map.yaml"),
        description="Full path to Sprint 4 saved map yaml (amr_map.yaml)",
    )

    declare_use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="Use simulation clock (true when running with Gazebo)",
    )

    declare_params_file = DeclareLaunchArgument(
        "params_file",
        default_value=os.path.join(
            get_package_share_directory("amr_navigation"),
            "config",
            "amr_nav2_params.yaml",
        ),
        description="AMR nav2 params (official baseline + TF/topic names only)",
    )

    declare_autostart = DeclareLaunchArgument(
        "autostart",
        default_value="true",
        description="Automatically activate map_server and amcl",
    )

    lifecycle_nodes = ["map_server", "amcl"]

    param_substitutions = {
        "use_sim_time": use_sim_time,
        "yaml_filename": map_yaml_file,
    }

    configured_params = ParameterFile(
        RewrittenYaml(
            source_file=params_file,
            root_key=namespace,
            param_rewrites=param_substitutions,
            convert_types=True,
        ),
        allow_substs=True,
    )

    localization_group = GroupAction(
        [
            LifecycleNode(
                package="nav2_map_server",
                executable="map_server",
                name="map_server",
                namespace=namespace,
                output="screen",
                parameters=[configured_params],
            ),
            LifecycleNode(
                package="nav2_amcl",
                executable="amcl",
                name="amcl",
                namespace=namespace,
                output="screen",
                parameters=[configured_params],
            ),
            Node(
                package="nav2_lifecycle_manager",
                executable="lifecycle_manager",
                name="lifecycle_manager_localization",
                output="screen",
                parameters=[
                    {
                        "use_sim_time": use_sim_time,
                        "autostart": autostart,
                        "node_names": lifecycle_nodes,
                    }
                ],
            ),
        ]
    )

    return LaunchDescription(
        [
            declare_namespace,
            declare_map,
            declare_use_sim_time,
            declare_params_file,
            declare_autostart,
            localization_group,
        ]
    )
