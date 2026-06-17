# amr_bringup

## Status

**In Progress** — Sprint 1: `display.launch.py` implemented. Additional launches planned for later sprints.

## Usage

```bash
source install/setup.bash
ros2 launch amr_bringup display.launch.py
```

Starts `robot_state_publisher`, `joint_state_publisher_gui`, and RViz2 with the AMR model.

## Purpose

Provides top-level launch entry points that compose nodes and configurations from other `amr_*` packages. This package orchestrates the system but does not own robot logic, algorithms, or hardware drivers.

## Expected Components

| Component | Sprint | Description |
|-----------|--------|-------------|
| `launch/display.launch.py` | 1 | **Implemented** — Robot model + RViz visualization |
| `launch/gazebo.launch.py` | 2 | Gazebo Classic simulation with sensors |
| `launch/control.launch.py` | 3 | Teleoperation and odometry stack |
| `launch/slam.launch.py` | 4 | SLAM Toolbox mapping |
| `launch/navigation.launch.py` | 5 | Nav2 autonomous navigation |
| `launch/full_system.launch.py` | 5 | Composed simulation + navigation stack |
| `config/` | 1+ | Shared parameter files referenced by launches |

## Dependencies (planned)

- All functional `amr_*` packages (via `IncludeLaunchDescription`)
- Standard ROS2 runtime packages as required per launch

## Related Packages

- **Depends on:** `amr_description`, `amr_gazebo`, `amr_control`, `amr_slam`, `amr_navigation`
- **Invoked by:** operators, CI smoke tests, `amr_dashboard` (future)
