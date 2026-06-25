# Sprint 3 Final Freeze

> **Frozen:** 2026-06-24  
> **Status:** Ubuntu final acceptance passed. Do not modify frozen modules without re-running Sprint 3 acceptance.

---

## ① Final System Architecture

```
Keyboard
   ↓
teleop_twist_keyboard  (official, interactive TTY)
   ↓
/cmd_vel  (project-unified velocity interface, geometry_msgs/Twist)
   ↓
cmd_vel_relay  (amr_control — QoS-compatible bridge)
   ↓
/diff_drive_controller/cmd_vel_unstamped
   ↓
diff_drive_controller  (ros2_control, use_stamped_vel: false)
   ↓
left_wheel_joint / right_wheel_joint  (velocity command interface)
   ↓
gazebo_ros2_control / GazeboSystem
   ↓
Gazebo Classic physics
   ↓
Robot (forward / backward / turn)
```

**Parallel paths (unchanged):**

- `joint_state_broadcaster` → `/joint_states`
- `diff_drive_controller` → `/diff_drive_controller/odom` + TF `odom` → `base_footprint`

**Launch entry:** `ros2 launch amr_gazebo gazebo.launch.py`

**Teleop entry:** `ros2 run teleop_twist_keyboard teleop_twist_keyboard` (native Ubuntu terminal, `/dev/pts/*`)

---

## ② Frozen Module List

| Module | Package / Path | Role |
|--------|----------------|------|
| Motion control config | `amr_control/config/ros2_control.yaml` | Controller manager, diff_drive, odom params |
| cmd_vel bridge | `amr_control/scripts/cmd_vel_relay.py` | `/cmd_vel` → `/diff_drive_controller/cmd_vel_unstamped` |
| ros2_control hardware | `amr_description/urdf/amr_ros2_control.xacro` | Wheel velocity interfaces |
| Gazebo sim launch | `amr_gazebo/launch/gazebo.launch.py` | Gazebo, spawn, spawners, cmd_vel_relay |
| Gazebo ros2_control plugin | `amr_gazebo/urdf/amr.gazebo.xacro` | `libgazebo_ros2_control.so` + yaml load |
| Wheel kinematics | `amr_description/urdf/amr_wheels.xacro` | Both wheel axes `0 1 0` |
| Gazebo wheel friction | `amr_gazebo/urdf/amr_wheels.gazebo.xacro` | Drive wheel contact |

---

## ③ Files That Later Sprints Must NOT Modify

```
src/amr_control/config/ros2_control.yaml
src/amr_control/scripts/cmd_vel_relay.py
src/amr_control/CMakeLists.txt          # cmd_vel_relay install rule
src/amr_control/package.xml             # relay dependencies

src/amr_description/urdf/amr_ros2_control.xacro
src/amr_description/urdf/amr_wheels.xacro   # drive wheel axis / joint names

src/amr_gazebo/launch/gazebo.launch.py      # spawner chain + cmd_vel_relay node
src/amr_gazebo/urdf/amr.gazebo.xacro          # gazebo_ros2_control plugin block
src/amr_gazebo/urdf/amr_wheels.gazebo.xacro   # wheel friction (motion stability)
```

**Frozen topic contract:**

| Topic | Type | Direction |
|-------|------|-----------|
| `/cmd_vel` | `geometry_msgs/Twist` | In (teleop, Nav2, test pub) |
| `/diff_drive_controller/cmd_vel_unstamped` | `geometry_msgs/Twist` | Internal (relay → controller) |
| `/diff_drive_controller/odom` | `nav_msgs/Odometry` | Out |
| `/joint_states` | `sensor_msgs/JointState` | Out |

---

## ④ If a Future Sprint Must Touch Frozen Files

Re-run **full Sprint 3 motion acceptance** before merging:

1. `ros2 launch amr_gazebo gazebo.launch.py` — spawn + both controllers active
2. `ros2 topic pub --once /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.2}, angular: {z: 0.0}}"` — robot moves forward
3. `ros2 run teleop_twist_keyboard teleop_twist_keyboard` in native TTY — `i/j/l` drive robot; **no QoS incompatible warnings**
4. `ros2 topic echo /diff_drive_controller/odom` — pose updates while moving
5. `ros2 control list_hardware_interfaces` — wheel velocity interfaces `[claimed]`
6. Backward + turn behavior in Gazebo

---

## Code Audit (Freeze Checklist)

| Check | Result |
|-------|--------|
| Deprecated `cmd_vel_keyboard.launch.py` | **Absent** (removed; teleop is official `ros2 run`) |
| Invalid spawner `--controller-ros-args` | **Absent** (unsupported on stock Humble) |
| Plugin-level cmd_vel remap | **Absent** (ineffective with spawner-loaded controllers) |
| `topic_tools relay` workaround | **Removed** (QoS incompatible with teleop) |
| Debug / TODO / FIXME in frozen paths | **None** |
| Sprint 4 debug code in frozen packages | **None** |

**Final bridge:** `cmd_vel_relay.py` with RELIABLE + VOLATILE QoS (depth 10).

---

## Sprint 3 Acceptance Record

- Robot stable in Gazebo Classic
- `joint_state_broadcaster` active
- `diff_drive_controller` active
- Official `teleop_twist_keyboard` controls robot
- `/cmd_vel` is unified project velocity interface
- Forward, backward, left/right turn verified in Gazebo

**Sprint 4 (SLAM) must not begin until this freeze is reviewed and approved.**
