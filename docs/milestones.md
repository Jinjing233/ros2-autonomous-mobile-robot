# Development Milestones

This document tracks sprint progress, deliverables, and acceptance criteria for the AMR platform.

## Progress Overview

| Sprint | Focus | Status |
|--------|-------|--------|
| 0 | Repository and package architecture | **Complete** |
| 1 | Robot model and RViz visualization | **Complete** |
| 2 | Gazebo Classic simulation with sensors | **Complete** |
| 3 | Differential-drive control, teleop, odometry | **Complete** |
| 4 | SLAM Toolbox mapping | Planned |
| 5 | Nav2 autonomous navigation | Planned |
| 6+ | Perception, dashboard, hardware bring-up | Future |

> **New session?** Read [handoff.md](handoff.md) for ROS graph, key files, known issues, and next tasks.

---

## Sprint 0 — Repository Initialization

**Status: Complete**

### Goal

Establish the full package architecture, project documentation, and buildable ROS2 workspace scaffold without implementing robot functionality.

### Deliverables

- [x] Root `README.md`, `LICENSE` (MIT), ROS2 `.gitignore`
- [x] Documentation: `architecture.md`, `setup.md`, `milestones.md`, `conventions.md`
- [x] Eight ROS2 packages under `src/` with `package.xml`, `CMakeLists.txt`, and package `README.md`
- [x] Development roadmap with sprint alignment

### Out of Scope

- URDF/Xacro, RViz, Gazebo, sensors, SLAM, Nav2, control algorithms, dashboard

### Acceptance Criteria

- [x] Repository clones cleanly on Ubuntu 22.04
- [x] `colcon build` succeeds for all eight packages
- [x] Every package documents status, purpose, and planned components
- [x] No `build/`, `install/`, or `log/` directories committed

---

## Sprint 1 — Robot Model and RViz Visualization

**Status: Complete**

### Goal

Define the differential-drive AMR kinematic and visual model; display it in RViz with a correct TF tree.

### Packages

- `amr_description` — primary implementation
- `amr_bringup` — `display.launch.py` entry point

### Deliverables

- Xacro robot description (base, wheels, caster, sensor mounts)
- `robot_state_publisher` integration
- RViz configuration
- `joint_state_publisher_gui` for manual joint inspection (optional)

### Acceptance Criteria

- [x] `ros2 launch amr_bringup display.launch.py` opens RViz with the robot model
- [x] TF tree includes `base_link`, `base_footprint`, `laser_link`, `imu_link`
- [x] Wheel joints are defined with correct axis and limits
- [x] No Gazebo or navigation dependencies required

---

## Sprint 2 — Gazebo Classic Simulation

**Status: Complete**

### Goal

Simulate the AMR in Gazebo Classic with LiDAR and IMU sensors publishing standard ROS topics.

### Packages

- `amr_gazebo` — primary implementation
- `amr_bringup` — `gazebo.launch.py` entry point

### Deliverables

- Gazebo world file
- Robot spawn from URDF/Xacro
- 2D LiDAR plugin publishing `/scan`
- IMU plugin publishing `/imu`
- Diff-drive Gazebo plugin stub (full control in Sprint 3)

### Acceptance Criteria

- [x] Robot spawns correctly in Gazebo Classic
- [x] `/scan` and `/imu` topics publish at expected rates
- [x] Sensor frames match URDF (`laser_link`, `imu_link`)
- [x] RViz can visualize laser scan in simulation

---

## Sprint 3 — Motion Control and Teleoperation

**Status: Complete**

### Goal

Enable velocity command control of the simulated robot with odometry feedback.

### Packages

- `amr_control` — primary implementation
- `amr_bringup` — `control.launch.py` entry point

### Deliverables

- [x] Phase 1: `ros2_control` skeleton + Gazebo plugin (`amr_ros2_control.xacro`, `ros2_control.yaml`)
- [x] Phase 2: `joint_state_broadcaster`
- [x] Phase 3: `diff_drive_controller` (official Humble params)
- [x] Phase 4: Keyboard teleop (`cmd_vel_keyboard.launch.py`)
- [x] Phase 5: Odometry (`enable_odom_tf`, covariances, `open_loop`)
- [x] Kinematics: both drive wheels axis `0 1 0` (left/right via controller wheel names)
- [x] Stability: dual casters + Gazebo friction overlays + ODE tuning + `spawn_z:=0.0`

### Acceptance Criteria

- [x] Teleoperation drives the robot in Gazebo (Phase 4)
- [x] `/diff_drive_controller/odom` reflects motion; TF `odom` → `base_footprint` (Phase 5)
- [x] Forward: x increases; turn: yaw changes; no unwanted spin at rest
- [x] `/scan`, `/imu`, `/joint_states`, both controllers remain active (regression)

---

## Sprint 4 — SLAM Mapping

**Status: Planned**

### Goal

Build a 2D occupancy grid map of the simulated environment using SLAM Toolbox.

### Packages

- `amr_slam` — primary implementation
- `amr_bringup` — `slam.launch.py` entry point

### Deliverables

- SLAM Toolbox configuration
- Online async SLAM launch
- Map save and load workflow

### Acceptance Criteria

- [ ] SLAM produces a coherent `/map` while driving via teleop
- [ ] Map can be saved and reloaded
- [ ] TF chain `map` → `odom` → `base_footprint` is consistent

---

## Sprint 5 — Nav2 Autonomous Navigation

**Status: Planned**

### Goal

Navigate autonomously to goal poses in simulation using Nav2.

### Packages

- `amr_navigation` — primary implementation
- `amr_bringup` — `navigation.launch.py` entry point

### Deliverables

- Nav2 parameter files (costmaps, planners, controllers, behavior tree)
- Localization with saved map (AMCL or SLAM Toolbox localization mode)
- RViz2 Nav2 goal interface

### Acceptance Criteria

- [ ] Robot localizes on a saved map
- [ ] Nav2 plans and executes paths to goal poses
- [ ] Robot avoids static obstacles from the laser scan
- [ ] `full_system.launch.py` composes simulation + navigation stack

---

## Sprint 6+ — Extensions

**Status: Future**

### Planned Work

| Area | Package | Examples |
|------|---------|----------|
| Perception | `amr_perception` | Depth processing, obstacle segmentation, costmap layers |
| Dashboard | `amr_dashboard` | Foxglove, rosbridge, mission status UI |
| DevOps | Repository root | Docker dev environment, CI/CD pipeline |
| Hardware | `amr_control`, `amr_bringup` | Real robot driver, hardware interface launch |

Detailed acceptance criteria for Sprint 6+ will be defined when Sprint 5 is complete.
