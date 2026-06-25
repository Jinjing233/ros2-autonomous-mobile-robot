# Session Handoff — AMR Platform

> Last updated: 2026-06-24. Use this document to resume work in a new conversation without re-reading the full chat history.

## One-Line Summary

ROS2 Humble differential-drive AMR: **Sprint 0–3 complete** (model → Gazebo → ros2_control → teleop → odometry). **Next: Sprint 4 — SLAM Toolbox.**

---

## Engineering Rules (Non-Negotiable)

1. **Official templates only** — For `ros2_control`, `diff_drive_controller`, Nav2, SLAM Toolbox, etc., copy from **ROS2 Humble official examples**. Do not invent controller/nav configs.
2. **Minimal diffs** — Change only what the sprint requires. Do not refactor unrelated code.
3. **Plan before code** — For new phases, propose a plan and wait for approval when the user asks for phased work.
4. **No scope creep** — Do not add Nav2, EKF, AMCL, or README edits unless explicitly requested.
5. **Platform** — Ubuntu 22.04, ROS2 Humble, **Gazebo Classic** (not Harmonic).
6. **Naming** — Packages prefixed `amr_*`; TF per REP-105 (`base_footprint`, `base_link`, `odom`, `laser_link`, `imu_link`).

---

## Sprint Progress

| Sprint | Focus | Status |
|--------|-------|--------|
| 0 | Repo architecture | **Complete** |
| 1 | URDF/Xacro + RViz | **Complete** |
| 2 | Gazebo + LiDAR + IMU | **Complete** |
| 3 | ros2_control + diff_drive + teleop + odom | **Complete** |
| 4 | SLAM Toolbox | **Next** |
| 5 | Nav2 | Planned |

### Sprint 3 Summary (Complete)

| Phase | Deliverable | Status |
|-------|-------------|--------|
| 1 | `ros2_control` skeleton + Gazebo plugin | Done |
| 2 | `joint_state_broadcaster` | Done |
| 3 | `diff_drive_controller` | Done |
| 4 | Keyboard teleop (`cmd_vel_keyboard.launch.py`) | Done |
| 5 | Odometry (`enable_odom_tf`, covariances, `open_loop`) | Done |

**Kinematics note:** Both drive wheels use axis `0 1 0`. `diff_drive_controller` distinguishes left/right via `left_wheel_names` / `right_wheel_names` — do not mirror right wheel axis in URDF.

---

## How to Run (Ubuntu)

```bash
source /opt/ros/humble/setup.bash
cd ~/robot_project   # or your clone path
colcon build --packages-select amr_description amr_gazebo amr_control amr_bringup
source install/setup.bash

# Terminal 1 — simulation + controllers
ros2 launch amr_gazebo gazebo.launch.py

# Terminal 2 — keyboard teleop
ros2 launch amr_control cmd_vel_keyboard.launch.py

# RViz (optional, no Gazebo)
ros2 launch amr_bringup display.launch.py
```

---

## ROS Graph (Current)

| Topic / TF | Name | Notes |
|------------|------|-------|
| cmd_vel (teleop) | `/diff_drive_controller/cmd_vel_unstamped` | Remapped from `/cmd_vel` in teleop launch |
| odometry | `/diff_drive_controller/odom` | Official ros2_control namespaced topic |
| joint states | `/joint_states` | From `joint_state_broadcaster` |
| LiDAR | `/scan` | Gazebo ray plugin on `laser_link` |
| IMU | `/imu` | Gazebo IMU plugin on `imu_link` |
| TF | `odom` → `base_footprint` | From `diff_drive_controller` (`enable_odom_tf: true`) |
| TF | `base_footprint` → `base_link` → sensors/wheels | From `robot_state_publisher` (URDF fixed joints) |

### Controllers

```bash
ros2 control list_controllers
# Expected: joint_state_broadcaster [active], diff_drive_controller [active]
```

---

## Key Files

| File | Role |
|------|------|
| `src/amr_control/config/ros2_control.yaml` | Controller manager + diff_drive + odom params |
| `src/amr_gazebo/launch/gazebo.launch.py` | Gazebo + RSP + spawn + controller spawners |
| `src/amr_gazebo/urdf/amr.gazebo.xacro` | Sim overlay: sensors, friction, `libgazebo_ros2_control.so` |
| `src/amr_description/urdf/amr_properties.xacro` | Mechanical params (`wheel_radius=0.05`, `wheel_separation=0.32`, etc.) |
| `src/amr_description/urdf/amr_wheels.xacro` | Drive wheels; both axes `0 1 0` |
| `src/amr_control/launch/cmd_vel_keyboard.launch.py` | Teleop → `cmd_vel_unstamped` |

### Robot Geometry (Quick Reference)

- Chassis: 0.50 × 0.40 × 0.12 m, 20 kg
- Wheels: radius 0.05 m, separation 0.32 m, z offset −0.06 m on `base_link`
- `base_link_z` = 0.11 m above `base_footprint` (wheel ground contact)
- LiDAR: `laser_link`, z = 0.14 m; IMU: `imu_link`, z = 0.06 m

### Official diff_drive Reference

Template: [gazebo_ros2_control Humble `diff_drive_controller.yaml`](https://github.com/ros-controls/gazebo_ros2_control/blob/humble/gazebo_ros2_control_demos/config/diff_drive_controller.yaml)

---

## Suggested Next Tasks (Sprint 4)

1. SLAM Toolbox configuration (official Humble async online mapping template)
2. `amr_slam` package implementation + `slam.launch.py` in `amr_bringup`
3. Verify TF chain `map` → `odom` → `base_footprint` while teleop driving
4. Map save/load workflow

---

## What NOT to Change (Unless User Asks)

- Sprint 3 controller yaml, teleop launch, wheel kinematics (accepted)
- LiDAR / IMU Gazebo plugins
- Nav2, EKF, AMCL packages (scaffold only)
