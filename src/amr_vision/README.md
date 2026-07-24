# amr_vision

**Status:** Implemented (Sprint 7 Phases 2–4). Standalone `ament_python` package — independent from all other `amr_*` packages, not referenced by `amr_bringup` or any shared/top-level launch file.

**Purpose:** OpenCV-based image processing for the AMR platform, built on `/image_raw` from the Gazebo RGB camera (Sprint 7 Phase 1).

## Nodes

| Node | Subscribes | Publishes | Processing |
|---|---|---|---|
| `gray_converter` | `/image_raw` (`sensor_msgs/Image`, `bgr8`) | `/image_gray` (`sensor_msgs/Image`, `mono8`) | `cv_bridge` → `cv2.cvtColor(BGR2GRAY)` |
| `canny_detector` | `/image_raw` (`sensor_msgs/Image`, `bgr8`) | `/image_edges` (`sensor_msgs/Image`, `mono8`) | `cv_bridge` → grayscale → `cv2.GaussianBlur` → `cv2.Canny` |

Both nodes subscribe to `/image_raw` independently; neither depends on the other's output.

## Parameters (`canny_detector`)

| Parameter | Default | Description |
|---|---|---|
| `canny_threshold1` | `50.0` | Canny lower hysteresis threshold |
| `canny_threshold2` | `150.0` | Canny upper hysteresis threshold |
| `gaussian_blur_kernel_size` | `5` | Gaussian blur kernel size (positive odd integer) |
| `gaussian_blur_sigma` | `0.0` | Gaussian blur sigmaX (`0.0` = computed from kernel size) |

Defined in `config/vision.yaml`, keyed by node name `amr_vision_canny_detector`.

## Launch files

| Launch file | Starts | Notes |
|---|---|---|
| `vision.launch.py` | `gray_converter` only | Independent, no parameters |
| `canny.launch.py` | `canny_detector` only | Exposes `canny_threshold1`, `canny_threshold2`, `gaussian_blur_kernel_size`, `gaussian_blur_sigma` as launch arguments |
| `perception.launch.py` | `gray_converter` + `canny_detector` | Combined pipeline; `canny_detector` parameters loaded from `vision_config` launch argument (default: `config/vision.yaml`) |

## Run

Requires `/image_raw` already publishing (e.g. `amr_gazebo` with the RGB camera running):

```bash
# Grayscale only
ros2 launch amr_vision vision.launch.py

# Canny edge detection only
ros2 launch amr_vision canny.launch.py

# Combined pipeline (gray_converter + canny_detector)
ros2 launch amr_vision perception.launch.py
```

Or run nodes directly:

```bash
ros2 run amr_vision gray_converter
ros2 run amr_vision canny_detector
```

## Parameter overrides

```bash
# Per-argument override via canny.launch.py
ros2 launch amr_vision canny.launch.py canny_threshold1:=30.0 canny_threshold2:=90.0 gaussian_blur_kernel_size:=3

# Custom YAML file via perception.launch.py
ros2 launch amr_vision perception.launch.py vision_config:=/path/to/custom_vision.yaml

# Runtime override on a running node
ros2 param set /amr_vision_canny_detector canny_threshold1 30.0
```

## Build

```bash
cd /home/jinjing/robot_project
colcon build --symlink-install --packages-select amr_vision
source install/setup.bash
```

## Verification

```bash
ros2 topic hz /image_gray
ros2 topic hz /image_edges
ros2 param list /amr_vision_canny_detector
ros2 run rqt_image_view rqt_image_view   # select /image_gray or /image_edges
```

## Integration status

`amr_vision` is **not** wired into `amr_bringup` or any shared/top-level launch file. It must be launched separately from the main simulation stack, and consumes `/image_raw` from whichever source is currently publishing it (Gazebo RGB camera or otherwise).

## Expected components (future)

- Integration into a broader perception pipeline (`amr_perception`) once real-camera input and Sprint 8+ scope are defined.
