# amr_vision

**Status:** Implemented (Sprint 7 Phase 2)

**Purpose:** Standalone OpenCV-based image processing for the AMR platform. `ament_python` package, independent from all other `amr_*` packages — not referenced by any shared/top-level launch file.

## Node

`gray_converter` — subscribes `/image_raw` (`sensor_msgs/Image`), converts to grayscale via `cv_bridge` + OpenCV (`cv2.cvtColor`, `BGR2GRAY`), publishes `/image_gray` (`sensor_msgs/Image`, `mono8`).

## Run

Requires `/image_raw` already publishing (e.g. `amr_gazebo` with the RGB camera running):

```bash
ros2 launch amr_vision vision.launch.py
```

Or run the node directly:

```bash
ros2 run amr_vision gray_converter
```

## Expected components (future)

- Additional CV nodes (edge detection, feature tracking, etc.) as Sprint 7 Phase 2+ progresses.
