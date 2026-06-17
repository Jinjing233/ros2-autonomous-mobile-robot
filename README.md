# ROS2 Autonomous Mobile Robot (AMR)

A professional ROS2 Humble engineering platform for a differential-drive autonomous mobile robot. This repository is designed as a long-term, portfolio-grade robotics stack with clear milestones from robot modeling through simulation, SLAM, and Nav2 navigation.

## Platform Overview

| Item | Value |
|------|-------|
| ROS Distribution | ROS2 Humble |
| Target OS | Ubuntu 22.04 LTS |
| Robot Type | Differential-drive AMR (two driven wheels + caster) |
| Simulation (planned) | Gazebo Classic |
| License | MIT |

## Current Status

**Sprint 0 — Repository Initialization (complete)**

The full package architecture is in place. All packages are scaffolded with documentation; no robot functionality has been implemented yet.

See [docs/milestones.md](docs/milestones.md) for the development roadmap and sprint progress.

## Repository Structure

```
ros2-autonomous-mobile-robot/
├── docs/                    # Project documentation
├── src/
│   ├── amr_description/     # Robot URDF/Xacro model (Sprint 1)
│   ├── amr_bringup/         # System launch orchestration
│   ├── amr_gazebo/          # Gazebo Classic simulation (Sprint 2)
│   ├── amr_control/         # Motion control and teleoperation (Sprint 3)
│   ├── amr_slam/            # SLAM and mapping (Sprint 4)
│   ├── amr_navigation/      # Nav2 autonomous navigation (Sprint 5)
│   ├── amr_perception/      # Perception pipeline (future)
│   └── amr_dashboard/       # Monitoring and operator UI (future)
├── LICENSE
└── README.md
```

## Quick Start

See [docs/setup.md](docs/setup.md) for environment setup on Ubuntu 22.04 with ROS2 Humble.

```bash
# Clone and build (after ROS2 Humble is installed)
cd ros2-autonomous-mobile-robot
colcon build
source install/setup.bash
```

## Documentation

| Document | Description |
|----------|-------------|
| [architecture.md](docs/architecture.md) | System architecture, package map, and data flow |
| [setup.md](docs/setup.md) | Native Ubuntu 22.04 + ROS2 Humble setup |
| [milestones.md](docs/milestones.md) | Sprint plan, progress tracking, acceptance criteria |
| [conventions.md](docs/conventions.md) | Naming, launch, parameter, and contribution conventions |

Each package under `src/` contains its own `README.md` with purpose, status, and planned components.

## Development Roadmap

| Sprint | Focus | Status |
|--------|-------|--------|
| 0 | Repository and package architecture | **Complete** |
| 1 | URDF/Xacro model and RViz visualization | Planned |
| 2 | Gazebo Classic simulation with LiDAR and IMU | Planned |
| 3 | Differential-drive control and teleoperation | Planned |
| 4 | SLAM Toolbox mapping | Planned |
| 5 | Nav2 autonomous navigation | Planned |
| 6+ | Perception, dashboard, hardware bring-up | Future |

## License

This project is licensed under the [MIT License](LICENSE).
