# Sprint 7 Phase 2 — OpenCV Grayscale (`amr_vision`) — 2026-07-24

## Scope

New standalone `ament_python` package `amr_vision`. Independent from all other `amr_*` packages; not referenced by any shared/top-level launch file. No existing package modified.

## What was built

- `amr_vision/gray_converter.py`: subscribes `/image_raw` (`sensor_msgs/Image`), converts via `cv_bridge` + OpenCV (`cv2.cvtColor`, `BGR2GRAY`), publishes `/image_gray` (`sensor_msgs/Image`, `mono8`).
- `launch/vision.launch.py`: standalone launch, single node, no dependency on `amr_bringup` or any other package's launch files.

## Validation

| Check | Result | Verified by |
|---|---|---|
| `colcon build --symlink-install --packages-select amr_vision` | Success, 1 package, no errors | Cursor |
| `ros2 pkg executables amr_vision` → `gray_converter` registered | Pass | Cursor |
| Node instantiation / launch file parse | Pass | Cursor |
| Synthetic image test (`bgr8` in → `mono8` out, dimensions preserved) | Pass (`80x60` in, `mono8` `80x60` out) | Cursor (headless, synthetic publisher) |
| Real Gazebo camera feed (`/image_raw` from `amr_gazebo` RGB camera) → `/image_gray` | Pass | User (Ubuntu GUI) |
| `/image_gray` publish rate | ~10 Hz | User (Ubuntu GUI) |
| RViz `Image` display on `/image_gray` | Status: OK | User (Ubuntu GUI) |

## Regression / scope check

- No file outside `src/amr_vision/` was created or modified.
- No frozen module (`amr_description`, `amr_gazebo`, `amr_control`, `amr_slam`, `amr_navigation`) was touched.
- `amr_vision` is not included by any existing launch file or package dependency — confirmed via `grep -rn "amr_vision" src/` (no hits outside `src/amr_vision/` itself).

## Not commited

No `git commit` / `git push` performed as part of this work.
