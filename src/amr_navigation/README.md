# amr_navigation

## Status

**Planned** — Package scaffold created in Sprint 0. No Nav2 configuration yet.

## Purpose

Configures and launches the Nav2 navigation stack for autonomous goal-directed motion. Owns costmap parameters, planner/controller selection, behavior trees, and localization integration for the AMR platform.

## Expected Components

| Component | Sprint | Description |
|-----------|--------|-------------|
| `config/nav2_params.yaml` | 5 | Nav2 stack parameters (costmaps, planners, controllers) |
| `config/amcl_params.yaml` | 5 | AMCL localization (if used alongside saved maps) |
| `launch/navigation.launch.py` | 5 | Full Nav2 bringup |
| `behavior_trees/` | 5 | Custom Nav2 behavior trees (if needed) |
| `maps/` | 5 | Reference to maps produced by `amr_slam` |

## Dependencies (planned)

- `navigation2`, `nav2_bringup`
- `amr_description`, `amr_slam`
- Running `/scan`, `/odom`, `/map`, and TF chain

## Related Packages

- **Depends on:** `amr_description`, `amr_slam`
- **Consumed by:** `amr_bringup`

## Interface Contract

| Topic / Action | Type | Direction |
|--------------|------|-----------|
| `/cmd_vel` | `geometry_msgs/Twist` | Publish |
| `/scan` | `sensor_msgs/LaserScan` | Subscribe |
| `/map` | `nav_msgs/OccupancyGrid` | Subscribe |
| `navigate_to_pose` | Nav2 action | Server |
