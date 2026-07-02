# ROS2 Autonomous Mobile Robot (AMR)

Diff-drive mobile robot on **ROS2 Humble** and **Gazebo Classic**: simulation, SLAM, AMCL, Nav2.

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

## Data flow

```text
Gazebo → /scan, /odom
      → SLAM (mapping) or AMCL + map_server (nav)
      → Nav2 → /cmd_vel → diff_drive_controller
```

## Status

| Milestone | Done |
|-----------|------|
| Robot model + Gazebo | yes |
| ros2_control + teleop | yes |
| SLAM + map save | yes |
| AMCL + Nav2 | yes |
| Office world (V1.1) | yes |
| Perception / manipulation | no |

Nav2 config is based on `nav2_bringup` (Humble) with AMR frame/topic names and small controller tweaks for sim.

## License

MIT
