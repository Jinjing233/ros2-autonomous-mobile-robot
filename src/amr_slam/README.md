# amr_slam

## Status

**Planned** — Package scaffold created in Sprint 0. No SLAM configuration yet.

## Purpose

Integrates SLAM Toolbox for 2D LiDAR-based mapping and localization. Owns SLAM parameter files, mapping launch configurations, and map persistence workflows.

## Expected Components

| Component | Sprint | Description |
|-----------|--------|-------------|
| `config/slam_toolbox_params.yaml` | 4 | SLAM Toolbox tuning for the AMR |
| `launch/online_async_slam.launch.py` | 4 | Online mapping while driving |
| `launch/localization.launch.py` | 5 | Localization on a saved map |
| `maps/` | 4 | Saved occupancy grid maps (gitignored at runtime) |

## Dependencies (planned)

- `slam_toolbox`
- `amr_description`
- Running `/scan`, `/odom`, and TF from simulation or hardware stack

## Related Packages

- **Depends on:** `amr_description`
- **Consumed by:** `amr_bringup`, `amr_navigation`

## Interface Contract

| Topic | Type | Direction |
|-------|------|-----------|
| `/scan` | `sensor_msgs/LaserScan` | Subscribe |
| `/odom` | `nav_msgs/Odometry` | Subscribe |
| `/map` | `nav_msgs/OccupancyGrid` | Publish |

TF: publishes / maintains `map` → `odom`
