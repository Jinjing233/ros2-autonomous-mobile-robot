from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg_share = FindPackageShare("amr_gazebo")
    gazebo_ros_share = FindPackageShare("gazebo_ros")

    default_world = PathJoinSubstitution([pkg_share, "worlds", "empty.world"])

    world = LaunchConfiguration("world")
    gui = LaunchConfiguration("gui")
    verbose = LaunchConfiguration("verbose")
    use_sim_time = LaunchConfiguration("use_sim_time")
    spawn_x = LaunchConfiguration("spawn_x")
    spawn_y = LaunchConfiguration("spawn_y")
    spawn_z = LaunchConfiguration("spawn_z")

    gazebo_launch = PathJoinSubstitution(
        [gazebo_ros_share, "launch", "gazebo.launch.py"]
    )
    spawn_launch = PathJoinSubstitution(
        [pkg_share, "launch", "spawn_amr.launch.py"]
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "world",
                default_value=default_world,
                description="Full path to the Gazebo world file",
            ),
            DeclareLaunchArgument(
                "gui",
                default_value="true",
                description="Launch Gazebo GUI (gzclient)",
            ),
            DeclareLaunchArgument(
                "verbose",
                default_value="false",
                description="Enable verbose Gazebo logging",
            ),
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="true",
                description="Use simulation clock from Gazebo",
            ),
            DeclareLaunchArgument(
                "spawn_x",
                default_value="0.0",
                description="Initial spawn x position (meters)",
            ),
            DeclareLaunchArgument(
                "spawn_y",
                default_value="0.0",
                description="Initial spawn y position (meters)",
            ),
            DeclareLaunchArgument(
                "spawn_z",
                default_value="0.05",
                description="Initial spawn z position (meters)",
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(gazebo_launch),
                launch_arguments={
                    "world": world,
                    "gui": gui,
                    "verbose": verbose,
                }.items(),
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(spawn_launch),
                launch_arguments={
                    "use_sim_time": use_sim_time,
                    "spawn_x": spawn_x,
                    "spawn_y": spawn_y,
                    "spawn_z": spawn_z,
                }.items(),
            ),
        ]
    )
