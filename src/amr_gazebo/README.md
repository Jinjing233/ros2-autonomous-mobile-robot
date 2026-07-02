# amr_gazebo

Gazebo Classic sim for the AMR: worlds, spawn, LiDAR/IMU plugins, `gazebo_ros2_control`.

## Run

```bash
ros2 launch amr_gazebo gazebo.launch.py
ros2 launch amr_gazebo gazebo.launch.py world:=office.world
```

Loads `joint_state_broadcaster` and `diff_drive_controller` after spawn. Teleop in another terminal:

```bash
ros2 launch amr_control cmd_vel_keyboard.launch.py
```

Spawn only (Gazebo already up):

```bash
ros2 launch amr_gazebo spawn_amr.launch.py
```

## Worlds

| File | Notes |
|------|--------|
| `empty.world` | default |
| `office.world` | ~15×10 m robot lab; needs its own SLAM map |

## Topics

| Topic | Notes |
|-------|--------|
| `/scan` | LiDAR |
| `/imu` | IMU |
| `/diff_drive_controller/odom` | wheel odom + TF |
| `/cmd_vel` | relayed to controller (see `amr_control`) |
