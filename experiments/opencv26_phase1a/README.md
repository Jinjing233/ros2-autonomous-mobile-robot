# Phase 1A — OpenCV 5 cat/dog detection feasibility

Scope: prove that OpenCV 5 `cv.dnn` can load and run a lightweight ONNX detector
and detect cats/dogs well enough to continue. No ROS2, no AWS, no robot control.
Nothing here touches the Ubuntu system OpenCV (4.5.4), ROS2 Humble, `cv_bridge`
or any existing `amr_*` package.

## Isolation

* `virtualenv.pyz` 21.14.1, pinned to get-virtualenv commit `986dc71b…`,
  SHA256 `e1d7c93f…e689` (recorded by us: upstream publishes no checksum for it).
* venv at `~/opencv26_work/venv` (outside the repo, no system site-packages).
* `opencv-python-headless==5.0.0.93` (official PyPI wheel), `numpy 2.2.6`.
* No `sudo`, no `apt`. Rollback: `rm -rf ~/opencv26_work` (and this directory).
* The ROS shell exports `PYTHONPATH`/`LD_LIBRARY_PATH`; run everything with
  `env -u PYTHONPATH -u LD_LIBRARY_PATH <venv python> -E -s script.py`.

## Model

| | |
|---|---|
| Model | YOLOX-s, COCO 80 classes (cat = 15, dog = 16, 0-based) |
| Source | OpenCV Zoo `models/object_detection_yolox`, commit `47534e27…` (Git LFS) |
| Files | `object_detection_yolox_2022nov.onnx` 35,858,002 B, SHA256 `c5c2d13e…8063` (= LFS oid); `…_int8.onnx` 9,079,452 B, SHA256 `01a3b0f4…3935` (= LFS oid) |
| Licence | Apache-2.0 (directory `LICENSE`, repo-root `LICENSE`). The model directory states no separate weights licence; weights derive from the upstream Megvii YOLOX (Apache-2.0). Re-check before publication. |

## cv.dnn engine

`cv2.dnn.readNetFromONNX(path, engine)` with `ENGINE_NEW` (main) and
`ENGINE_CLASSIC` (comparison), backend `DNN_BACKEND_OPENCV`, target `DNN_TARGET_CPU`.
OpenCV 5 also exposes `ENGINE_ORT`; it is deliberately **never used**
(`cv2.getBuildInformation()` reports `ONNX Runtime: NO`). The new engine ignores
`setPreferableTarget` (OpenCV prints a warning) and is CPU-only.
Only pre/post-processing (letterbox, grid decode) is NumPy; NMS is `cv2.dnn.NMSBoxesBatched`.

## Data

COCO val2017 (IDs, licences and source URLs in `results/manifest.json`; no images are
stored in the repo). Only licence ids 4 (CC BY), 5 (CC BY-SA), 7, 8 are used;
NonCommercial/NoDerivs images are excluded. Seeded selection (`fetch_assets.py`).
Positives: 29 cats + 23 dogs (single pet, box >= 5 % of the image; 30/30 was not
reachable under the licence filter). Negatives: 30 general, 10 teddy bears,
10 couch/bed scenes (none contain cat/dog annotations).
Degradations are synthetic: occlusion (grey box over 40/70 % of the GT box),
Gaussian blur (sigma 3/6), low light (x0.4/x0.2 + noise), distance (image scaled to 1/3, 1/5).

## Reproduce

```bash
./setup_env.sh
env -u PYTHONPATH -u LD_LIBRARY_PATH ~/opencv26_work/venv/bin/python -E -s fetch_assets.py
env -u PYTHONPATH -u LD_LIBRARY_PATH ~/opencv26_work/venv/bin/python -E -s run_eval.py   # ~5 min
```

Outputs: `results/samples.csv` (per sample: class, confidence, boxes, timings, correct),
`results/summary.md`, `results/summary.json`, `results/gate.json`.

## Limitations

* Small samples (23 dogs: a 1-image change moves dog recall by 4 points).
* Degradations are synthetic; grey-box occlusion is not real furniture/limbs.
* "detect" requires IoU >= 0.5 with the full GT box, so partial-view boxes count as misses;
  the `presence` column (no IoU) is the better proxy for "a pet is in view".
* Latency is one laptop CPU (i7-11800H, 4 threads); Graviton is not measured yet.
* Not tested: real-camera frames, toys, pets shown on a screen (planned follow-up).
