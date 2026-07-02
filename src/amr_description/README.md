# amr_description

URDF/Xacro for the diff-drive AMR. No dependency on other `amr_*` packages.

## Layout

- `amr_properties.xacro` — dimensions, wheel radius, etc.
- `amr_base.xacro`, `amr_wheels.xacro`, `amr_caster.xacro`, `amr_sensors.xacro`
- `amr.urdf.xacro` — top-level model
- `amr_ros2_control.xacro` — velocity interfaces (used from `amr_gazebo`)

LiDAR mount: center of base, `laser_z_offset` 0.14 m.

## View in RViz

```bash
ros2 launch amr_bringup display.launch.py
```
