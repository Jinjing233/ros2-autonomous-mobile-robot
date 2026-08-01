# amr_perception

**Status:** Partially implemented (Sprint 8 Phase 4: single-command real-camera vision pipeline). Costmap layers and other future perception work remain placeholders.

## `real_camera_perception.launch.py`

Composes two already-existing, independently-launchable launch files — no camera or OpenCV node code is duplicated here:

- `amr_camera_input/launch/real_camera.launch.py` (official `v4l2_camera` node)
- `amr_vision/launch/perception.launch.py` (`gray_converter` + `canny_detector`), with `image_topic` pinned to `/real_camera/image_raw`

```bash
ros2 launch amr_perception real_camera_perception.launch.py
```

### Launch arguments (forwarded to `amr_camera_input`)

| Argument | Default |
|---|---|
| `video_device` | `/dev/video0` |
| `image_width` | `640` |
| `image_height` | `480` |
| `frame_rate` | `30` (informational only — see `amr_camera_input` README) |

### Topics produced

| Topic | Source |
|---|---|
| `/real_camera/image_raw`, `/real_camera/camera_info` | `amr_camera_input` (`v4l2_camera`) |
| `/image_gray` | `amr_vision` (`gray_converter`) |
| `/image_edges` | `amr_vision` (`canny_detector`) |

### Known gap: camera calibration

No calibration file is shipped or fabricated for the real camera. `v4l2_camera` logs `Camera calibration file ... not found` at startup, and `/real_camera/camera_info` is published with uncalibrated (identity/zero) intrinsics. This is a recorded gap, not a silent workaround — running `camera_calibration` and pointing `amr_camera_input`'s `camera_config` at the resulting file is a future task.

### Not touched

Gazebo, Nav2, SLAM, and `ros2_control` are unaffected by this launch file.

## Future perception work

Costmap layers and other camera-based perception beyond the vision pipeline above remain placeholders.
