# amr_control

`ros2_control` config and keyboard teleop for the diff-drive AMR.

## Teleop

Gazebo + controllers must be running:

```bash
ros2 launch amr_control cmd_vel_keyboard.launch.py
```

Publishes to `/diff_drive_controller/cmd_vel_unstamped`. Gazebo launch also runs `cmd_vel_relay.py` so Nav2 can use `/cmd_vel`.

## Config

`config/ros2_control.yaml` — based on the gazebo_ros2_control Humble diff_drive demo. Key values match `amr_properties.xacro`:

| Param | Value |
|-------|-------|
| wheel_separation | 0.32 |
| wheel_radius | 0.05 |
| base_frame_id | base_footprint |
| enable_odom_tf | true |

Odometry topic: `/diff_drive_controller/odom`
