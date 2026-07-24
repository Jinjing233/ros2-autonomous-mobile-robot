# ROS2 Autonomous Mobile Robot (AMR)

Diff-drive mobile robot on **ROS2 Humble** and **Gazebo Classic**: simulation, LiDAR/IMU/RGB camera sensing, SLAM, AMCL, Nav2. **AMR V1 / V1.1: complete.**

Demo: [YouTube](https://youtu.be/XBV4MKnJ9yI)

## Quick start

```bash
cd ~/your_ws
colcon build
source /opt/ros/humble/setup.bash
source install/setup.bash
```

### 1. Gazebo

```bash
ros2 launch amr_gazebo gazebo.launch.py
# office demo:
ros2 launch amr_gazebo gazebo.launch.py world:=office.world
```

### 2. SLAM mapping

`mapping.launch.py` already starts RViz — do **not** also run `slam_rviz.launch.py`.

```bash
ros2 launch amr_slam mapping.launch.py use_sim_time:=true
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

Save map when done:

```bash
ros2 launch amr_slam save_map.launch.py map_name:=my_map
```

### 3. Navigation

Use a saved map (empty world or office — each needs its own map):

```bash
ros2 launch amr_navigation navigation.launch.py use_sim_time:=true
ros2 launch amr_navigation navigation_rviz.launch.py use_sim_time:=true
```

In RViz use **2D Goal Pose**. The Nav2 panel goal tool often fails under sim time.

## Packages

| Package | What it does |
|---------|----------------|
| `amr_description` | URDF / Xacro |
| `amr_gazebo` | Gazebo worlds, spawn, sim plugins |
| `amr_control` | `ros2_control` + keyboard teleop |
| `amr_slam` | SLAM Toolbox mapping |
| `amr_navigation` | map_server, AMCL, Nav2 |
| `amr_vision` | Standalone OpenCV image processing (`ament_python`); not wired into any shared launch |

## Data flow

```text
Gazebo → /scan, /odom, /image_raw
      → SLAM (mapping) or AMCL + map_server (nav)
      → Nav2 → /cmd_vel → diff_drive_controller
```

`amr_vision` (standalone, run separately — not part of the flow above):

```text
/image_raw → amr_vision (OpenCV, cv_bridge) → /image_gray
```

```bash
ros2 launch amr_vision vision.launch.py
```

## Status

| Milestone | Done |
|-----------|------|
| Robot model + Gazebo | yes |
| ros2_control + teleop | yes |
| RGB camera (Sprint 7 Phase 1) | yes |
| OpenCV grayscale, `amr_vision` (Sprint 7 Phase 2) | yes |
| SLAM + map save | yes |
| AMCL localization | yes |
| Nav2 navigation | yes |
| Office world (V1.1) | yes |
| Perception / manipulation | no |

Nav2 config is based on `nav2_bringup` (Humble) with AMR frame/topic names and small controller tweaks for sim.

## Roadmap

AMR V1 / V1.1 (this repo, complete) → **V2 Perception** → **V3 Mobile Manipulation** → **Physical AI**

## Development logs

- [Gazebo ros2_control parser failure — 2026-07-24](docs/development_logs/2026-07-24_gazebo_ros2_control_parser_failure.md)
- [AMR V1 Final Validation — 2026-07-24](docs/development_logs/2026-07-24_AMR_V1_Final_Validation.md)
- [Sprint 7 Phase 2 — OpenCV Grayscale (amr_vision) — 2026-07-24](docs/development_logs/2026-07-24_Sprint7_Phase2_OpenCV.md)

## License

MIT
