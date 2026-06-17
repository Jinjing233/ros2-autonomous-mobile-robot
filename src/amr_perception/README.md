# amr_perception

## Status

**Future** — Package scaffold created in Sprint 0. Perception development begins after Sprint 5 (Nav2) is complete.

## Purpose

Extends the AMR platform with sensor processing beyond raw LiDAR scans. Will provide obstacle detection, optional depth/camera processing, and enhanced costmap inputs for navigation in dynamic environments.

## Expected Components

| Component | Sprint | Description |
|-----------|--------|-------------|
| Obstacle detection node | 6+ | Process laser or depth data for dynamic obstacles |
| Costmap layer plugins | 6+ | Nav2 costmap layer integration |
| Sensor fusion (optional) | 6+ | Combine LiDAR, IMU, and camera data |
| `config/perception_params.yaml` | 6+ | Detection thresholds and filter parameters |
| `launch/perception.launch.py` | 6+ | Perception pipeline bringup |

## Dependencies (planned)

- `amr_description`
- `sensor_msgs`, `geometry_msgs`
- Nav2 costmap interfaces (when costmap layers are added)

## Related Packages

- **Depends on:** `amr_description`
- **Enhances:** `amr_navigation` (costmap layers)
- **Must not block:** core navigation stack; perception is additive

## Notes

This package is reserved in the architecture to demonstrate forward planning. Detailed design will be finalized after the core SLAM + Nav2 pipeline is validated in simulation.
