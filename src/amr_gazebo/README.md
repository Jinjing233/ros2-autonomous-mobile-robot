# amr_gazebo

## Status

**In Progress** — Sprint 2 Phase 3 complete: Gazebo LiDAR plugin on `laser_link` publishing `/scan`. IMU pending next phase.

## Purpose

Integrates the AMR robot model with Gazebo Classic. Owns simulation worlds, robot spawning, and Gazebo sensor plugins (LiDAR, IMU). Provides the simulated environment used for control, SLAM, and navigation development.

## Usage

```bash
source install/setup.bash
ros2 launch amr_gazebo gazebo.launch.py
```

Spawns the AMR model from `amr_description` into `empty.world` at `(x, y, z) = (0, 0, 0.05)`.

Simulation uses `amr.gazebo.xacro` (description model + Gazebo plugins). Spawn writes `/tmp/amr_robot.urdf` via `spawn_entity.py -file`.

Optional arguments:

```bash
ros2 launch amr_gazebo gazebo.launch.py gui:=true verbose:=false
ros2 launch amr_gazebo gazebo.launch.py spawn_z:=0.05
ros2 launch amr_gazebo spawn_amr.launch.py   # spawn only (Gazebo must already be running)
```

## Expected Components

| Component | Sprint | Description |
|-----------|--------|-------------|
| `worlds/empty.world` | 2 | **Implemented** — Minimal simulation environment |
| `launch/gazebo.launch.py` | 2 | **Implemented** — Gazebo server + GUI + robot spawn |
| `launch/spawn_amr.launch.py` | 2 | **Implemented** — Robot state publisher + Gazebo spawn |
| Robot spawn | 2 | **Implemented** — via `spawn_entity.py` |
| `urdf/amr.gazebo.xacro` | 2 | **Implemented** — Simulation overlay (description + plugins) |
| `urdf/amr_lidar.gazebo.xacro` | 2 | **Implemented** — LiDAR ray sensor on `laser_link` |
| LiDAR plugin | 2 | **Implemented** — Publishes `sensor_msgs/LaserScan` on `/scan` |
| IMU plugin | 2 | Planned — Publishes `/imu` |
| Diff-drive plugin stub | 2 | Planned — Initial mobility (completed in Sprint 3) |

## Dependencies

- `gazebo_ros`, `gazebo_ros_pkgs`
- `launch`, `launch_ros`
- `amr_description` (required from Phase 2 onward for robot spawn)

## Related Packages

- **Depends on:** `amr_description` (Phase 2+)
- **Consumed by:** `amr_bringup`, `amr_control`, `amr_slam`, `amr_navigation`

## Notes

Gazebo **Classic** is used for ROS2 Humble compatibility. Migration to Gazebo Harmonic may be evaluated in a future milestone.
