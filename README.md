# ROS2 Autonomous Mobile Robot (AMR)

> A complete ROS2 Humble Autonomous Mobile Robot built from scratch, featuring simulation, motion control, SLAM mapping, localization, autonomous navigation, and a realistic indoor office simulation environment. This project follows industrial robotics development practices and serves as my flagship robotics portfolio project.

## Project Demonstration

📺 [YouTube Demo](https://youtu.be/XBV4MKnJ9yI)

## Overview

This project is a complete Autonomous Mobile Robot (AMR) software stack developed using **ROS2 Humble** and **Gazebo Classic**.

Rather than demonstrating isolated ROS packages, this repository incrementally builds an end-to-end robotics system following industrial robotics development practices—from robot modeling to autonomous navigation—with a long-term roadmap toward robot perception, mobile manipulation, and Physical AI.

The project is organized into sprint-based milestones, where every sprint is independently verified before progressing to the next stage.

## AMR V1.1 Completed Features

### Robot Platform

- Robot Description (URDF/Xacro)
- Gazebo Classic Simulation
- Indoor Office Simulation Environment
- LiDAR & IMU Integration
- ros2_control
- Differential Drive Motion
- Wheel Odometry
- Keyboard Teleoperation

### Mapping

- SLAM Toolbox
- Online Occupancy Grid Mapping
- Real-time Scan Matching
- Occupancy Grid Generation
- Map Saving (PGM + YAML)

### Localization

- Nav2 Map Server
- Adaptive Monte Carlo Localization (AMCL)
- Initial Pose Estimation
- Particle Filter Localization

### Autonomous Navigation

- Navigation2
- Global Path Planning
- Controller Server
- Behavior Server
- Velocity Smoother
- Goal-based Navigation
- Stable Goal Arrival
- RViz Goal Interface

## Features

### Robot Description

- Modular URDF/Xacro architecture
- Differential-drive mobile robot
- Configurable physical parameters
- Industrial ROS2 package organization

### Simulation

- Gazebo Classic
- Indoor Office Environment
- Custom Robot Spawning
- Static Obstacles
- Stable Physics Simulation

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

### SLAM Mapping

- SLAM Toolbox
- Online Occupancy Grid Mapping
- Real-time Scan Matching
- Map → Odom TF
- RViz Visualization
- Map Saving

### Localization

- Nav2 Map Server
- Adaptive Monte Carlo Localization
- Particle Filter Localization
- Initial Pose Estimation
- RViz Visualization

### Autonomous Navigation

- Navigation2 Stack
- Planner Server
- Controller Server
- Behavior Server
- BT Navigator
- Velocity Smoother
- Global Costmap
- Local Costmap
- Autonomous Goal Navigation
- Stable Goal Arrival

## Demo

### Demo 1 — Gazebo Simulation

- Indoor office environment
- Differential-drive robot
- LiDAR visualization

### Demo 2 — SLAM Mapping

- Online mapping
- Occupancy Grid generation
- Map saving

### Demo 3 — AMCL Localization

- Map loading
- Particle filter localization
- Initial pose estimation

### Demo 4 — Autonomous Navigation

- Navigation2
- Global path planning
- Goal-based navigation
- Autonomous goal arrival

## Development Roadmap

| Sprint | Status |
| --- | --- |
| Sprint 0 – Workspace Setup | ✅ Completed |
| Sprint 1 – Robot Description | ✅ Completed |
| Sprint 2 – Gazebo Simulation | ✅ Completed |
| Sprint 3 – Motion Control & Odometry | ✅ Completed |
| Sprint 4 – SLAM Mapping | ✅ Completed |
| Sprint 5 – Localization (AMCL) | ✅ Completed |
| Sprint 6 – Navigation2 Autonomous Navigation | ✅ Completed |
| **AMR V1.1 – Indoor Office Demo Environment** | ✅ Completed |
| Sprint 7 – Robot Perception | ⏳ Planned |
| Sprint 8 – Mobile Manipulation | ⏳ Planned |
| Sprint 9 – Physical AI | ⏳ Planned |

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
Occupancy Grid Mapping
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
├── amr_navigation/
├── amr_slam/
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
- Python
- C++
- Ubuntu 22.04

## Current Capabilities

The robot currently supports:

- Indoor office simulation
- Differential-drive motion
- Keyboard teleoperation
- Wheel odometry
- Complete TF tree
- LiDAR scanning
- IMU measurements
- Online SLAM mapping
- Occupancy Grid generation
- Map saving & loading
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
- Robot Perception
- Sensor Fusion
- Extended Kalman Filter (EKF)
- Semantic Mapping
- Mobile Manipulation
- MoveIt2
- Vision-Language-Action (VLA) Models
- World Models
- Physical AI
- Sim-to-Real Deployment

## Development Philosophy

This project follows an incremental engineering workflow:

1. Build a stable robotics foundation.
2. Verify every sprint before moving forward.
3. Use official ROS2 Humble implementations whenever possible.
4. Maintain a modular and scalable architecture.
5. Progress from simulation to mapping, localization, navigation, perception, manipulation, and ultimately Physical AI.

## License

Released under the MIT License.
