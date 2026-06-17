# amr_description

## Status

**Planned** — Package scaffold created in Sprint 0. No robot model files yet.

## Purpose

Owns the kinematic and visual description of the differential-drive AMR. This is the single source of truth for robot geometry, link hierarchy, joint definitions, and sensor frame mounts used by simulation, control, and navigation packages.

## Expected Components

| Component | Sprint | Description |
|-----------|--------|-------------|
| `urdf/amr.urdf.xacro` | 1 | Top-level robot Xacro |
| `urdf/amr_base.xacro` | 1 | Base link, footprint, and physical dimensions |
| `urdf/amr_wheel.xacro` | 1 | Drive wheel macro (left/right) |
| `urdf/amr_caster.xacro` | 1 | Passive caster wheel |
| `urdf/amr_sensors.xacro` | 1 | LiDAR and IMU link mounts |
| `rviz/display.rviz` | 1 | RViz2 visualization configuration |
| `meshes/` | 1 | Visual and collision meshes (optional STL/DAE) |

## Dependencies (planned)

- `robot_state_publisher`
- `xacro`
- `joint_state_publisher` / `joint_state_publisher_gui`
- `rviz2`

## Related Packages

- **Consumed by:** `amr_bringup`, `amr_gazebo`, `amr_control`, `amr_navigation`
- **Must not depend on:** any other `amr_*` package
