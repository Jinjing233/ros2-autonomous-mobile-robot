# amr_control

## Status

**Planned** — Package scaffold created in Sprint 0. No control nodes or configurations yet.

## Purpose

Owns the velocity command interface and differential-drive actuation for the AMR. Bridges high-level motion commands (`/cmd_vel`) to wheel actuation and publishes odometry feedback (`/odom`) for localization and navigation stacks.

## Expected Components

| Component | Sprint | Description |
|-----------|--------|-------------|
| Diff-drive controller config | 3 | `ros2_control` or Gazebo diff-drive plugin parameters |
| `launch/teleop.launch.py` | 3 | Keyboard or joystick teleoperation |
| `config/control_params.yaml` | 3 | Velocity limits, acceleration limits, wheel parameters |
| Hardware interface (future) | 6+ | Real robot motor driver node |

## Dependencies (planned)

- `amr_description` (robot geometric parameters)
- `geometry_msgs`, `nav_msgs`
- `teleop_twist_keyboard` or `joy` (teleoperation)
- `ros2_control` / controller packages (if used)

## Related Packages

- **Depends on:** `amr_description`
- **Consumed by:** `amr_bringup`, `amr_slam`, `amr_navigation`

## Interface Contract

| Topic | Type | Direction |
|-------|------|-----------|
| `/cmd_vel` | `geometry_msgs/Twist` | Subscribe |
| `/odom` | `nav_msgs/Odometry` | Publish |

TF: `odom` → `base_footprint` (via robot state publisher / controller)
