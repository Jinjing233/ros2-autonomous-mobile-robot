import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    use_sim_time = LaunchConfiguration("use_sim_time")
    map_topic = LaunchConfiguration("map_topic")
    map_file = LaunchConfiguration("map_file")

    declare_use_sim_time = DeclareLaunchArgument(
        "use_sim_time",
        default_value="true",
        description="Use simulation clock (true when saving from Gazebo SLAM)",
    )

    declare_map_topic = DeclareLaunchArgument(
        "map_topic",
        default_value="/map",
        description="Occupancy grid topic published by slam_toolbox",
    )

    declare_map_file = DeclareLaunchArgument(
        "map_file",
        default_value=os.path.join("maps", "amr_map"),
        description="Output map prefix; writes <prefix>.yaml and <prefix>.pgm",
    )

    map_saver_cli = Node(
        package="nav2_map_server",
        executable="map_saver_cli",
        output="screen",
        arguments=["-f", map_file],
        parameters=[
            {
                "use_sim_time": use_sim_time,
                "map_subscribe_transient_local": True,
            }
        ],
        remappings=[("map", map_topic)],
    )

    return LaunchDescription(
        [
            declare_use_sim_time,
            declare_map_topic,
            declare_map_file,
            map_saver_cli,
        ]
    )
