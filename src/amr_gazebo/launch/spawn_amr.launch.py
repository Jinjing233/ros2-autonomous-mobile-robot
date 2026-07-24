from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import Command, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from ament_index_python.packages import get_package_share_directory
import os


def _launch_setup(context, *args, **kwargs):
    gazebo_share = get_package_share_directory("amr_gazebo")
    control_share = get_package_share_directory("amr_control")
    xacro_file = os.path.join(gazebo_share, "urdf", "amr.gazebo.xacro")
    ros2_control_config = os.path.join(control_share, "config", "ros2_control.yaml")

    use_sim_time = LaunchConfiguration("use_sim_time")
    spawn_x = LaunchConfiguration("spawn_x")
    spawn_y = LaunchConfiguration("spawn_y")
    spawn_z = LaunchConfiguration("spawn_z")

    robot_description = ParameterValue(
        Command(
            [
                "xacro ",
                xacro_file,
                " ros2_control_config:=",
                ros2_control_config,
            ]
        ),
        value_type=str,
    )

    robot_description_params = {
        "robot_description": robot_description,
        "use_sim_time": use_sim_time,
    }

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[robot_description_params],
    )

    joint_state_publisher_node = Node(
        package="joint_state_publisher",
        executable="joint_state_publisher",
        output="screen",
        parameters=[robot_description_params],
    )

    spawn_entity_node = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        output="screen",
        arguments=[
            "-entity",
            "amr",
            "-topic",
            "robot_description",
            "-x",
            spawn_x,
            "-y",
            spawn_y,
            "-z",
            spawn_z,
            "-timeout",
            "60.0",
        ],
    )

    return [
        robot_state_publisher_node,
        joint_state_publisher_node,
        spawn_entity_node,
    ]


def generate_launch_description():
    return LaunchDescription(
        [
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
                default_value="0.0",
                description="Initial spawn z position (meters); base_footprint is at ground contact",
            ),
            OpaqueFunction(function=_launch_setup),
        ]
    )
