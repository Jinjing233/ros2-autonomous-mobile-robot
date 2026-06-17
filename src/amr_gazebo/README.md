# amr_gazebo

## Status

**Planned** — Package scaffold created in Sprint 0. No simulation files yet.

## Purpose

Integrates the AMR robot model with Gazebo Classic. Owns simulation worlds, robot spawning, and Gazebo sensor plugins (LiDAR, IMU). Provides the simulated environment used for control, SLAM, and navigation development.

## Expected Components

| Component | Sprint | Description |
|-----------|--------|-------------|
| `worlds/amr_empty.world` | 2 | Default simulation environment |
| `launch/gazebo_sim.launch.py` | 2 | Gazebo server + robot spawn |
| `urdf/amr.gazebo.xacro` | 2 | Gazebo-specific plugins and sensor definitions |
| LiDAR plugin | 2 | Publishes `sensor_msgs/LaserScan` on `/scan` |
| IMU plugin | 2 | Publishes `sensor_msgs/Imu` on `/imu` |
| Diff-drive plugin stub | 2 | Initial mobility plugin (completed in Sprint 3) |

## Dependencies (planned)

- `amr_description`
- `gazebo_ros`, `gazebo_ros_pkgs`
- `robot_state_publisher`

## Related Packages

- **Depends on:** `amr_description`
- **Consumed by:** `amr_bringup`, `amr_control`, `amr_slam`, `amr_navigation`

## Notes

Gazebo **Classic** is used for ROS2 Humble compatibility. Migration to Gazebo Harmonic may be evaluated in a future milestone.
