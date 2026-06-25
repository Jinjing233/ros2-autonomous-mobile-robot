# ROS2 Autonomous Mobile Robot (AMR)

A professional ROS2 Humble engineering platform for a differential-drive autonomous mobile robot. This repository is designed as a long-term, portfolio-grade robotics stack with clear milestones from robot modeling through simulation, SLAM, and Nav2 navigation.

## Platform Overview

| Item | Value |
|------|-------|
| ROS Distribution | ROS2 Humble |
| Target OS | Ubuntu 22.04 LTS |
| Robot Type | Differential-drive AMR (two driven wheels + dual casters) |
| Simulation | Gazebo Classic |
| License | MIT |

## Current Status

**Sprint 1 — Robot model and RViz:** Complete  
**Sprint 2 — Gazebo Classic + LiDAR + IMU:** Complete  
**Sprint 3 — Motion control, teleop, odometry:** **Complete**

| Sprint 3 Phase | Deliverable | Status |
|----------------|-------------|--------|
| 1 | `ros2_control` + Gazebo plugin | Done |
| 2 | `joint_state_broadcaster` | Done |
| 3 | `diff_drive_controller` | Done |
| 4 | Keyboard teleop | Done |
| 5 | Odometry + `enable_odom_tf` | Done |

**Next:** Sprint 4 — SLAM Toolbox mapping. See [docs/milestones.md](docs/milestones.md).

### Sprint 3 Highlights

- `gazebo_ros2_control` + official Humble `diff_drive_controller` params
- Keyboard teleop via `teleop_twist_keyboard` → `/diff_drive_controller/cmd_vel_unstamped`
- Wheel odometry at `/diff_drive_controller/odom` and TF `odom` → `base_footprint`
- Drive wheels share joint axis `0 1 0`; left/right handled by controller `left_wheel_names` / `right_wheel_names`
- Gazebo stability: dual casters, contact/friction overlays, ODE tuning, `spawn_z:=0.0`

### Quick Run (Ubuntu)

```bash
source /opt/ros/humble/setup.bash
colcon build --symlink-install
source install/setup.bash

ros2 launch amr_gazebo gazebo.launch.py          # simulation + controllers
ros2 launch amr_control cmd_vel_keyboard.launch.py  # teleop (separate terminal)
ros2 launch amr_bringup display.launch.py        # RViz only
```

See [docs/setup.md](docs/setup.md) for full environment setup.

### ROS Graph (Sprint 3)

| Topic / TF | Name |
|------------|------|
| Velocity (teleop) | `/diff_drive_controller/cmd_vel_unstamped` |
| Odometry | `/diff_drive_controller/odom` |
| Joint states | `/joint_states` |
| LiDAR | `/scan` |
| IMU | `/imu` |
| TF | `odom` → `base_footprint` → `base_link` → sensors/wheels |

## Repository Structure

```
ros2-autonomous-mobile-robot/
├── docs/                    # Project documentation (+ handoff for new sessions)
├── src/
│   ├── amr_description/     # Robot URDF/Xacro model (Sprint 1 ✓)
│   ├── amr_bringup/         # display.launch.py (Sprint 1 ✓)
│   ├── amr_gazebo/          # Gazebo Classic simulation (Sprint 2 ✓)
│   ├── amr_control/         # ros2_control + teleop + odom (Sprint 3 ✓)
│   ├── amr_slam/            # SLAM and mapping (Sprint 4 — planned)
│   ├── amr_navigation/      # Nav2 autonomous navigation (Sprint 5 — planned)
│   ├── amr_perception/      # Perception pipeline (future)
│   └── amr_dashboard/       # Monitoring and operator UI (future)
├── LICENSE
└── README.md
```

## Documentation

| Document | Description |
|----------|-------------|
| [**handoff.md**](docs/handoff.md) | **Session handoff** — progress, ROS graph, next tasks |
| [architecture.md](docs/architecture.md) | System architecture, package map, and data flow |
| [setup.md](docs/setup.md) | Native Ubuntu 22.04 + ROS2 Humble setup |
| [milestones.md](docs/milestones.md) | Sprint plan, progress tracking, acceptance criteria |
| [conventions.md](docs/conventions.md) | Naming, launch, parameter, and contribution conventions |

Each package under `src/` contains its own `README.md` with purpose, status, and components.

## Development Roadmap

| Sprint | Focus | Status |
|--------|-------|--------|
| 0 | Repository and package architecture | **Complete** |
| 1 | URDF/Xacro model and RViz visualization | **Complete** |
| 2 | Gazebo Classic simulation with LiDAR and IMU | **Complete** |
| 3 | Differential-drive control, teleoperation, odometry | **Complete** |
| 4 | SLAM Toolbox mapping | Planned |
| 5 | Nav2 autonomous navigation | Planned |
| 6+ | Perception, dashboard, hardware bring-up | Future |

## Engineering Rules

- Use **ROS2 Humble official examples** as templates for controllers, Nav2, and SLAM — do not invent configs.
- Keep changes minimal and scoped to the current sprint phase.
- Gazebo **Classic** for Humble compatibility.

## License

This project is licensed under the [MIT License](LICENSE).
