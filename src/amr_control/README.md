# amr_control

## Status

**Complete** — Sprint 3. `ros2_control` stack with `joint_state_broadcaster`, `diff_drive_controller`, keyboard teleop, and wheel odometry.

## Purpose

Owns differential-drive actuation via `ros2_control` and keyboard teleoperation. Publishes wheel odometry and `odom` → `base_footprint` TF through `diff_drive_controller`.

## Components

| Component | Status | Description |
|-----------|--------|-------------|
| `config/ros2_control.yaml` | Done | `controller_manager`, `joint_state_broadcaster`, `diff_drive_controller` + odom params (official Humble demo template) |
| `launch/cmd_vel_keyboard.launch.py` | Done | `teleop_twist_keyboard` → `/diff_drive_controller/cmd_vel_unstamped` |

## Usage

```bash
# After Gazebo is running with controllers loaded:
ros2 launch amr_control cmd_vel_keyboard.launch.py
```

## Configuration

`config/ros2_control.yaml` follows [gazebo_ros2_control Humble diff_drive demo](https://github.com/ros-controls/gazebo_ros2_control/blob/humble/gazebo_ros2_control_demos/config/diff_drive_controller.yaml).

Key parameters (must match `amr_properties.xacro`):

| Parameter | Value |
|-----------|-------|
| `left_wheel_names` / `right_wheel_names` | `left_wheel_joint`, `right_wheel_joint` |
| `wheel_separation` | 0.32 |
| `wheel_radius` | 0.05 |
| `base_frame_id` | `base_footprint` |
| `odom_frame_id` | `odom` |
| `enable_odom_tf` | `true` |
| `open_loop` | `true` |
| `use_stamped_vel` | `false` |

Loaded by Gazebo plugin in `amr_gazebo/urdf/amr.gazebo.xacro`:

```xml
<parameters>$(find amr_control)/config/ros2_control.yaml</parameters>
```

## Interface Contract

| Topic | Actual name | Type |
|-------|-------------|------|
| Velocity command | `/diff_drive_controller/cmd_vel_unstamped` | `geometry_msgs/Twist` |
| Odometry | `/diff_drive_controller/odom` | `nav_msgs/Odometry` |

Teleop remaps `/cmd_vel` → `cmd_vel_unstamped`. Official ros2_control uses controller-namespaced topics; remap to `/odom` in launch if needed for downstream stacks.

TF: `odom` → `base_footprint` (from `diff_drive_controller` when `enable_odom_tf: true`)

## Dependencies

- `amr_description`, `amr_gazebo` (simulation loads this config)
- `controller_manager`, `joint_state_broadcaster`, `diff_drive_controller`
- `teleop_twist_keyboard`

## Related Packages

- **Depends on:** `amr_description`
- **Consumed by:** `amr_bringup`, `amr_slam`, `amr_navigation`
