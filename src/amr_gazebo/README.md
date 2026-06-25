# amr_gazebo

## Status

**Complete** — Sprint 2 (Gazebo + LiDAR + IMU) and Sprint 3 (unified launch with `ros2_control` controller spawners).

## Purpose

Integrates the AMR robot model with Gazebo Classic. Owns simulation worlds, robot spawning, sensor plugins, and the `gazebo_ros2_control` plugin bridge to `amr_control`.

## Usage

```bash
source install/setup.bash
ros2 launch amr_gazebo gazebo.launch.py
```

Starts Gazebo, `robot_state_publisher`, spawns AMR at ground contact (`spawn_z:=0.0`), then loads:

1. `joint_state_broadcaster`
2. `diff_drive_controller`

Optional arguments:

```bash
ros2 launch amr_gazebo gazebo.launch.py gui:=true verbose:=false
ros2 launch amr_gazebo spawn_amr.launch.py   # spawn only (Gazebo must already be running)
```

Teleop (separate terminal):

```bash
ros2 launch amr_control cmd_vel_keyboard.launch.py
```

## Components

| Component | Status | Description |
|-----------|--------|-------------|
| `worlds/empty.world` | Done | ODE solver tuning for stability |
| `launch/gazebo.launch.py` | Done | Gazebo + RSP + spawn + controller spawners |
| `launch/spawn_amr.launch.py` | Done | Spawn-only helper |
| `urdf/amr.gazebo.xacro` | Done | Full sim overlay + `libgazebo_ros2_control.so` |
| `urdf/amr_lidar.gazebo.xacro` | Done | LiDAR → `/scan` |
| `urdf/amr_imu.gazebo.xacro` | Done | IMU → `/imu` |
| `urdf/amr_base.gazebo.xacro` | Done | Chassis friction/contact |
| `urdf/amr_wheels.gazebo.xacro` | Done | Drive wheel friction |
| `urdf/amr_caster.gazebo.xacro` | Done | Caster friction |

## ROS Topics (Simulation)

| Topic | Frame | Rate (typical) |
|-------|-------|----------------|
| `/scan` | `laser_link` | sensor-dependent |
| `/imu` | `imu_link` | sensor-dependent |
| `/joint_states` | — | 50 Hz (controller) |
| `/diff_drive_controller/odom` | `odom` → `base_footprint` | 50 Hz |

## Dependencies

- `gazebo_ros`, `gazebo_ros_pkgs`, `gazebo_ros2_control`
- `controller_manager`, `joint_state_broadcaster`, `diff_drive_controller`
- `amr_description`, `amr_control`

## Related Packages

- **Depends on:** `amr_description`, `amr_control` (ros2_control yaml)
- **Consumed by:** `amr_bringup`, `amr_slam`, `amr_navigation`

## Notes

- Gazebo **Classic** for ROS2 Humble compatibility.
- Spawn uses `-topic robot_description` (not a temp URDF file).
- `base_footprint` spawns at ground level (`spawn_z:=0.0`).
