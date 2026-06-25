# ROS2 Autonomous Mobile Robot (AMR)

> A complete ROS2 Humble autonomous mobile robot project built from scratch, featuring simulation, control, perception, mapping, and autonomous navigation.

## Overview

This project is a long-term robotics portfolio focused on developing a complete Autonomous Mobile Robot (AMR) using **ROS2 Humble** and **Gazebo Classic**.

Instead of demonstrating isolated ROS packages, this repository incrementally builds an end-to-end robotics system following industrial development practices.

Current development includes:

- Robot modeling (URDF/Xacro)
- Gazebo simulation
- LiDAR & IMU integration
- ros2_control
- Differential drive controller
- Odometry
- Manual teleoperation

Future milestones include SLAM, Navigation2, robot perception, and Physical AI.

---

## Features

### Completed

#### Robot Description

- Modular URDF/Xacro architecture
- Differential-drive mobile robot
- Configurable physical parameters
- Clean package organization

#### Simulation

- Gazebo Classic simulation
- Custom robot spawning
- Integrated physics
- Stable robot model

#### Sensors

- 2D LiDAR
- IMU
- Robot State Publisher
- Joint State Broadcaster

#### Motion Control

- ros2_control
- Diff Drive Controller
- Keyboard Teleoperation
- Velocity Command Interface (`cmd_vel`)

#### Localization Foundation

- Wheel Odometry
- TF Tree
- Differential Drive Kinematics

---

## Development Roadmap

| Sprint | Status |
| --- | --- |
| Sprint 0 – Workspace Setup | ✅ |
| Sprint 1 – Robot Description | ✅ |
| Sprint 2 – Gazebo Simulation | ✅ |
| Sprint 3 – Motion Control & Odometry | ✅ |
| Sprint 4 – SLAM Toolbox Mapping | ⏳ |
| Sprint 5 – Navigation2 | ⏳ |
| Sprint 6 – Autonomous Navigation | ⏳ |
| Sprint 7 – Robot Perception | ⏳ |
| Sprint 8 – Physical AI Extensions | ⏳ |

---

## Project Structure

```text
src/
├── amr_description/
├── amr_control/
├── amr_gazebo/
├── ...
```

---

## Technology Stack

- ROS2 Humble
- Gazebo Classic
- URDF / Xacro
- ros2_control
- diff_drive_controller
- Joint State Broadcaster
- RViz2
- TF2
- C++
- Python
- Ubuntu 22.04

---

## Current Capabilities

The robot currently supports:

- Simulated differential-drive motion
- Keyboard teleoperation
- Wheel odometry
- TF publishing
- LiDAR scanning
- IMU measurements
- Real-time Gazebo simulation

---

## Demo

### Robot Simulation

> *(Add GIF or video here)*

![Simulation](docs/assets/simulation.gif)

### Robot Driving

> *(Add driving GIF here)*

![Driving](docs/assets/driving.gif)

### LiDAR Scan

> *(Add RViz screenshot here)*

![LiDAR](docs/assets/lidar.png)

---

## Future Work

The next development stages include:

- SLAM Toolbox
- Occupancy Grid Mapping
- Navigation2
- Path Planning
- Autonomous Navigation
- Obstacle Avoidance
- Robot Perception
- RGB Camera Integration
- OpenCV
- YOLO Object Detection
- Mobile Manipulation
- Physical AI

---

## Development Philosophy

This project follows an incremental engineering workflow:

1. Build a stable foundation.
2. Validate every milestone before moving forward.
3. Use official ROS2 Humble examples as the baseline for core components.
4. Maintain modular architecture suitable for long-term expansion.

---

## License

This project is released under the MIT License.
