# Sprint 7 Final Validation — 2026-07-24

## 1. Scope

This log consolidates the acceptance state of Sprint 7 (Vision Perception Pipeline) across all four phases, delivered entirely within the standalone `amr_vision` package (plus the Phase 1 RGB camera addition to `amr_gazebo`).

This document distinguishes categories of evidence, and does not claim confirmation that was not actually performed:

- **Verified (headless, Cursor)** — direct command/log evidence captured in headless SSH sessions during implementation.
- **Verified (Ubuntu GUI, user)** — confirmed interactively by the user in a graphical Ubuntu session (Gazebo camera feed, `rqt_image_view`).

## 2. Sprint 7 Phases

| Phase | Deliverable | Package |
|---|---|---|
| Phase 1 | RGB camera integration (`/image_raw`, `/camera_info`) | `amr_gazebo` |
| Phase 2 | `gray_converter` node — OpenCV grayscale conversion, `/image_gray` | `amr_vision` (new) |
| Phase 3 | `canny_detector` node — Gaussian blur + Canny edge detection, `/image_edges`, ROS2 parameters | `amr_vision` |
| Phase 4 | `perception.launch.py` combining both nodes, Canny parameters loaded from `config/vision.yaml` | `amr_vision` |

## 3. Packages Added / Modified

- **Added**: `src/amr_vision/` (new `ament_python` package) — `gray_converter.py`, `canny_detector.py`, `vision.launch.py`, `canny.launch.py`, `perception.launch.py`, `config/vision.yaml`, package `README.md`.
- **Modified** (this session, latest fix only): `src/amr_vision/amr_vision/gray_converter.py` — `finally: rclpy.shutdown()` guarded with `if rclpy.ok():` to eliminate a redundant-shutdown `RCLError` on `SIGINT` (see Section 6).
- **Not modified**: `amr_description`, `amr_gazebo` core (world/spawn/`ros2_control` plugins — the camera link/plugin were added under the already-accepted Phase 1 scope), `amr_control`, `amr_slam`, `amr_navigation`, `amr_bringup`.

## 4. Automated Test Results (headless, Cursor)

| Check | Result |
|---|---|
| `colcon build --symlink-install --packages-select amr_vision` | Success, no errors |
| Synthetic image test — `gray_converter` (`bgr8` in → `mono8` out) | Pass |
| Synthetic image test — `canny_detector` (`bgr8` in → `mono8` edges out, 320×240, 920 nonzero edge pixels on a synthetic rectangle+circle frame) | Pass |
| Synthetic image test — `perception.launch.py` (`/image_gray` and `/image_edges` both received from a single `/image_raw` publisher, 50 frames) | Pass — 24 `/image_gray`, 26 `/image_edges` messages received |
| `ros2 param list` / `ros2 param get` on `/amr_vision_canny_detector` | All 4 parameters present with correct type (`Double`/`Integer`) and default values |
| YAML parameter loading — default `config/vision.yaml` (50.0 / 150.0 / 5 / 0.0) | Confirmed via `ros2 param get`, and via process listing showing `--params-file .../config/vision.yaml` |
| YAML parameter loading — overridden `vision_config` argument, distinct values (20.0 / 60.0 / 3 / 1.5) | Confirmed via `ros2 param get`, values matched the override file exactly (not defaults) |
| Duplicate-launch check — `perception.launch.py` started twice | Both instances run; `ros2 node list` reports a name-collision warning as expected ROS2 graph behavior; no crash |

## 5. Gazebo Camera Test (Ubuntu GUI, user)

| Check | Result | Verified by |
|---|---|---|
| Real Gazebo RGB camera feed (`/image_raw`) → `/image_gray` | Pass | User (Ubuntu GUI) |
| Real Gazebo RGB camera feed (`/image_raw`) → `/image_edges` | Pass | User (Ubuntu GUI) |
| `/image_gray` publish rate | ~30 Hz | User (Ubuntu GUI) |
| `/image_edges` publish rate | ~30 Hz | User (Ubuntu GUI) |
| `rqt_image_view` visual confirmation of both `/image_gray` and `/image_edges` | Status: OK | User (Ubuntu GUI) |

The ~30 Hz figures above reflect the Gazebo camera plugin's configured publish rate as observed by the user with a live camera feed; Cursor's headless synthetic-image tests (Section 4) exercise correctness of the image pipeline logic but do not produce a comparable sustained-rate measurement without a real or simulated camera feed.

## 6. Node Shutdown Behavior

- **Found**: under `ros2 launch`, `SIGINT` triggers `rclpy`'s own signal handler, which shuts down the context before the node's `finally: rclpy.shutdown()` runs, producing `RCLError: rcl_shutdown already called` and a non-zero exit code for both `gray_converter` and `canny_detector`.
- **Fixed**: both nodes' `main()` now guard the call with `if rclpy.ok(): rclpy.shutdown()`.
- **Verified** (headless, Cursor): `ros2 launch amr_vision perception.launch.py`, then `SIGINT` —

```
[INFO] [gray_converter-1]: sending signal 'SIGINT' to process[gray_converter-1]
[INFO] [gray_converter-1]: process has finished cleanly [pid 41847]
[INFO] [canny_detector-2]: process has finished cleanly [pid 41849]
```

Both nodes now report `process has finished cleanly`. No orphaned processes remained after shutdown (confirmed via `pgrep`).

## 7. Integration / Regression Scope

- **Not integrated into `amr_bringup`**: confirmed via `grep -rn "amr_vision" src/` — no references outside `src/amr_vision/` itself.
- **Not integrated into any shared/top-level launch file**: `vision.launch.py`, `canny.launch.py`, and `perception.launch.py` are only referenced from within `amr_vision`.
- **No frozen V1 core module modified**: `amr_description`, `amr_gazebo` core simulation/control plugins, `amr_control`, `amr_slam`, `amr_navigation` were not touched during Sprint 7 Phases 2–4 (Phase 1's camera addition to `amr_gazebo`/`amr_description` was reviewed and accepted separately, prior to this validation log).
- All four phases' code changes were scoped exclusively to `src/amr_vision/` (Phases 2–4) plus the previously-accepted Phase 1 camera addition.

## 8. Not Committed

No `git commit` / `git push` performed as part of this work.

## 9. Next Stage

Sprint 8 (planned): real-camera input — replacing/augmenting the simulated Gazebo `/image_raw` source with a physical camera driver, subject to the same standalone-package-first validation method used throughout Sprint 7.
