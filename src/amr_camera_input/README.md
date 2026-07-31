# amr_camera_input

**Status:** Implemented (Sprint 8 Phase 3). Standalone `ament_cmake` package — no custom camera driver code. Wraps the official ROS2 Humble `v4l2_camera` node for real (physical) camera bring-up, independent from `amr_gazebo`'s simulated `/image_raw` and from `amr_vision`.

**Purpose:** Publish a real webcam/USB camera feed under a dedicated `/real_camera/*` namespace so it never collides with the Gazebo RGB camera topics, and can be fed into `amr_vision` via its `image_topic` launch argument (Sprint 8 Phase 2).

## Published topics

| Topic | Type |
|---|---|
| `/real_camera/image_raw` | `sensor_msgs/Image` |
| `/real_camera/camera_info` | `sensor_msgs/CameraInfo` |

## Launch arguments

| Argument | Default | Forwarded as |
|---|---|---|
| `video_device` | `/dev/video0` | `v4l2_camera` parameter `video_device` (1:1) |
| `image_width` | `640` | Composed with `image_height` into `v4l2_camera` parameter `image_size: [W, H]` |
| `image_height` | `480` | Composed with `image_width` into `v4l2_camera` parameter `image_size: [W, H]` |
| `frame_rate` | `30` | **Not forwarded** — see note below |
| `camera_config` | `config/real_camera.yaml` | Base `v4l2_camera` parameters (`pixel_format`, `output_encoding`, `camera_frame_id`); `video_device`/`image_size` above override this file |

### Important: real `v4l2_camera` (0.6.2, ROS2 Humble) parameter interface

Verified directly against a running instance (`ros2 param list` / `ros2 param get`), not guessed:

- There is **no** separate `image_width` / `image_height` parameter on the node. The real parameter is `image_size`, an integer array `[width, height]`. This launch file exposes `image_width` / `image_height` as convenience arguments and composes them into `image_size`.
- There is **no** `frame_rate` parameter at all in this version (confirmed via `ros2 param list` and by `strings`-scanning the compiled `libv4l2_camera.so` for any `frame_rate`/`fps`/`time_per_frame` symbol — none found). The `frame_rate` launch argument is kept for interface convenience/documentation but is **not** passed to the node. Actual frame rate is fixed by the `(pixel_format, image_size)` pair the device negotiates; run `v4l2-ctl -d /dev/video0 --list-formats-ext` to see the fps each combination supports. On the camera used for validation (`Integrated_Webcam_HD`, `uvcvideo`), both `YUYV 640x480` and `MJPG 640x480` report 30 fps, matching the `frame_rate` default here.

## Run

```bash
ros2 launch amr_camera_input real_camera.launch.py
```

With overrides:

```bash
ros2 launch amr_camera_input real_camera.launch.py \
  video_device:=/dev/video0 image_width:=640 image_height:=480
```

## Verification

```bash
ros2 topic list | grep real_camera
ros2 topic hz /real_camera/image_raw
ros2 param get /v4l2_camera image_size
ros2 run rqt_image_view rqt_image_view   # select /real_camera/image_raw
```

## Feeding into amr_vision

```bash
ros2 launch amr_camera_input real_camera.launch.py
ros2 launch amr_vision perception.launch.py image_topic:=/real_camera/image_raw
```

## Integration status

Standalone package: not referenced by `amr_bringup`, `amr_gazebo`, `amr_vision`, or any shared/top-level launch file.
