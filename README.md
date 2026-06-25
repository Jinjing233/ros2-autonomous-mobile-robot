# ROS2 Autonomous Mobile Robot (AMR)

> A complete ROS2 Humble Autonomous Mobile Robot built from scratch, featuring simulation, motion control, real-time SLAM mapping, and map saving. This project is designed as a long-term robotics portfolio following industrial robotics development practices.

## Overview

This project is a long-term robotics portfolio focused on building a complete Autonomous Mobile Robot (AMR) using **ROS2 Humble** and **Gazebo Classic**.

Instead of demonstrating isolated ROS packages, the project incrementally develops a complete robotics software stack, progressing from robot modeling to autonomous navigation and eventually toward Physical AI.

Current development has completed:

- Robot Description (URDF/Xacro)
- Gazebo Simulation
- LiDAR and IMU Integration
- ros2_control
- Differential Drive Motion
- Wheel Odometry
- Keyboard Teleoperation
- Real-time SLAM Mapping
- Occupancy Grid Generation
- Map Saving

Future milestones include localization (AMCL), Navigation2, robot perception, mobile manipulation, and Physical AI.

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

### SLAM Mapping

- SLAM Toolbox (ROS2 Humble)
- Online Occupancy Grid Mapping
- Real-time Scan Matching
- Map to Odom TF
- RViz Visualization
- Map Saving (PGM + YAML)

## Development Roadmap

| Sprint | Status |
| --- | --- |
| Sprint 0 – Workspace Setup | Done |
| Sprint 1 – Robot Description | Done |
| Sprint 2 – Gazebo Simulation | Done |
| Sprint 3 – Motion Control and Odometry | Done |
| Sprint 4 – SLAM Mapping and Map Saving | Done |
| Sprint 5 – Localization (AMCL) | Planned |
| Sprint 6 – Navigation2 | Planned |
| Sprint 7 – Robot Perception | Planned |
| Sprint 8 – Physical AI Extensions | Planned |

## System Architecture

```text
Gazebo Classic
        |
        v
Differential Drive Robot
        |
        v
LiDAR + IMU
        |
        v
ros2_control
        |
        v
Diff Drive Controller
        |
        v
Odometry + TF
        |
        v
SLAM Toolbox
        |
        v
Occupancy Grid Mapping
        |
        v
Map Saving
```

## Project Structure

```text
src/
├── amr_description/
├── amr_control/
├── amr_gazebo/
├── amr_slam/
└── ...
```

## Technology Stack

- ROS2 Humble
- Gazebo Classic
- RViz2
- TF2
- URDF / Xacro
- ros2_control
- diff_drive_controller
- SLAM Toolbox
- nav2_map_server
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

## Demo

### Robot Simulation

*(Add simulation GIF here)*

### Robot Driving

*(Add driving GIF here)*

### SLAM Mapping

*(Add SLAM mapping GIF here)*

### Saved Map

*(Add saved map image here)*

## Future Work

The next development stages include:

- Adaptive Monte Carlo Localization (AMCL)
- Navigation2
- Global Path Planning
- Local Path Planning
- Autonomous Navigation
- Dynamic Obstacle Avoidance
- RGB Camera Integration
- OpenCV
- YOLO Object Detection
- Extended Kalman Filter (EKF)
- Mobile Manipulation
- Physical AI

## Development Philosophy

This project follows an incremental engineering workflow:

1. Build a stable robotics foundation.
2. Validate every sprint before moving forward.
3. Use official ROS2 Humble implementations as the baseline for all core components.
4. Maintain a modular architecture suitable for long-term expansion.
5. Progress from simulation to autonomy, perception, manipulation, and Physical AI.

## License

Released under the MIT License.
