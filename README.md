# ROS2 Autonomous Mobile Robot (AMR)

> A complete ROS2 Humble Autonomous Mobile Robot built from scratch, featuring simulation, motion control, SLAM mapping, localization, and autonomous navigation. This project follows an industrial robotics development workflow and serves as the flagship robotics portfolio project.

## Overview

This project is a complete Autonomous Mobile Robot (AMR) software stack developed using **ROS2 Humble** and **Gazebo Classic**.

Instead of demonstrating isolated ROS packages, this repository incrementally builds a complete robotics system following industrial development practices—from robot modeling to autonomous navigation—with a long-term roadmap toward robot perception and Physical AI.

### AMR V1 Completed Features

- Robot Description (URDF/Xacro)
- Gazebo Classic Simulation
- LiDAR & IMU Integration
- ros2_control
- Differential Drive Motion
- Wheel Odometry
- Keyboard Teleoperation
- SLAM Toolbox Mapping
- Occupancy Grid Generation
- Map Saving
- Map Server
- AMCL Localization
- Navigation2
- Global Path Planning
- Autonomous Navigation
- Goal-based Navigation in RViz

## Features

### Robot Description

- Modular URDF/Xacro architecture
- Differential-drive mobile robot
- Configurable physical parameters
- Clean package organization

### Simulation

- Gazebo Classic simulation
- Custom robot spawning
- Stable robot model
- Integrated physics engine

### Sensors

- 2D LiDAR
- IMU
- Robot State Publisher
- Joint State Broadcaster

### Motion Control

- ros2_control
- Differential Drive Controller
- Keyboard Teleoperation
- Velocity Command Interface (`/cmd_vel`)
- Wheel Odometry
- Complete TF Tree

### Mapping

- SLAM Toolbox
- Online Occupancy Grid Mapping
- Real-time Scan Matching
- Map → Odom TF
- RViz Visualization
- Map Saving (PGM + YAML)

### Localization

- Nav2 Map Server
- Adaptive Monte Carlo Localization (AMCL)
- Particle Filter Localization
- Initial Pose Estimation
- Map → Odom Transformation
- RViz Localization Visualization

### Autonomous Navigation

- Navigation2 Stack
- Planner Server
- Controller Server
- Behavior Server
- BT Navigator
- Velocity Smoother
- Global Costmap
- Local Costmap
- Global Path Planning
- Autonomous Goal Navigation
- Stable Goal Arrival

## Development Roadmap

| Sprint | Status |
| --- | --- |
| Sprint 0 – Workspace Setup | ✅ Completed |
| Sprint 1 – Robot Description | ✅ Completed |
| Sprint 2 – Gazebo Simulation | ✅ Completed |
| Sprint 3 – Motion Control & Odometry | ✅ Completed |
| Sprint 4 – SLAM Mapping & Map Saving | ✅ Completed |
| Sprint 5 – Localization (AMCL) | ✅ Completed |
| Sprint 6 – Navigation2 Autonomous Navigation | ✅ Completed (AMR V1) |
| Sprint 7 – Robot Perception | ⏳ Planned |
| Sprint 8 – Physical AI Extensions | ⏳ Planned |

## System Architecture

```text
Gazebo Classic
        │
        ▼
Robot Description (URDF/Xacro)
        │
        ▼
LiDAR + IMU
        │
        ▼
ros2_control
        │
        ▼
Differential Drive Controller
        │
        ▼
Wheel Odometry + TF
        │
        ▼
SLAM Toolbox
        │
        ▼
Occupancy Grid Map
        │
        ▼
Map Server
        │
        ▼
AMCL Localization
        │
        ▼
Navigation2
        │
        ▼
Global Planner
        │
        ▼
Controller Server
        │
        ▼
Autonomous Navigation
```

## Project Structure

```text
src/
├── amr_description/
├── amr_control/
├── amr_gazebo/
├── amr_slam/
├── amr_navigation/
└── ...
```

## Technology Stack

- ROS2 Humble
- Gazebo Classic
- RViz2
- Navigation2
- SLAM Toolbox
- AMCL
- nav2_map_server
- TF2
- URDF / Xacro
- ros2_control
- diff_drive_controller
- C++
- Python
- Ubuntu 22.04

## Current Capabilities

The robot currently supports:

- Differential-drive motion
- Keyboard teleoperation
- Wheel odometry
- Complete TF tree
- LiDAR scanning
- IMU measurements
- Real-time Gazebo simulation
- Online SLAM mapping
- Occupancy Grid generation
- Map saving (PGM / YAML)
- Map loading
- AMCL localization
- Global path planning
- Goal-based autonomous navigation
- Stable autonomous arrival

## Future Work (AMR V2)

The next development stages include:

- RGB Camera Integration
- Depth Camera Support
- OpenCV
- YOLO Object Detection
- Sensor Fusion
- Extended Kalman Filter (EKF)
- Semantic Mapping
- Mobile Manipulation
- MoveIt2
- Vision-Language-Action Models
- Physical AI
- Sim-to-Real Deployment

## Development Philosophy

This project follows an incremental engineering workflow:

1. Build a stable robotics foundation.
2. Validate every sprint before moving forward.
3. Use official ROS2 Humble implementations as the baseline for all core components.
4. Maintain a modular architecture suitable for long-term expansion.
5. Progress from simulation to mapping, localization, autonomous navigation, perception, manipulation, and Physical AI.

## License

Released under the MIT License.
