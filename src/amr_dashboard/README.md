# amr_dashboard

## Status

**Future** — Package scaffold created in Sprint 0. Dashboard development begins after the core navigation stack is complete.

## Purpose

Provides an operator-facing interface for monitoring robot state, visualizing diagnostics, and optionally submitting navigation goals or mission commands. Decouples human interaction from the core autonomy stack.

## Expected Components

| Component | Sprint | Description |
|-----------|--------|-------------|
| Foxglove layout | 6+ | Preconfigured visualization layout |
| rosbridge_server integration | 6+ | WebSocket bridge for web clients |
| Mission status panel | 6+ | Navigation state, battery, diagnostics |
| `launch/dashboard.launch.py` | 6+ | Dashboard services bringup |
| Custom web UI (optional) | 6+ | React/Vue front-end over rosbridge |

## Dependencies (planned)

- `amr_bringup` (system must be running)
- `foxglove_bridge` or `rosbridge_suite` (TBD during design)
- Standard ROS2 diagnostic and topic interfaces

## Related Packages

- **Depends on:** `amr_bringup` (orchestration reference)
- **Observes:** topics and actions from all running `amr_*` packages
- **Must not own:** navigation logic, control, or SLAM

## Notes

Technology selection (Foxglove vs custom web UI vs both) will be decided when Sprint 6 planning begins. The package exists now to reserve a clear extension point in the architecture.
