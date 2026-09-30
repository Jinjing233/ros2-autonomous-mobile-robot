#!/usr/bin/env bash
# Phase 1A: create the isolated OpenCV 5 environment under ~/opencv26_work.
# No sudo, no apt, nothing installed into the system Python / ROS2.
# Idempotent: existing files are verified, not re-downloaded.
set -euo pipefail

WORK="${HOME}/opencv26_work"
mkdir -p "${WORK}"/{tools,models,images,cache}

# 1) virtualenv.pyz pinned to a get-virtualenv commit (tag 21.14.1) + SHA256
VENV_COMMIT=986dc71bcc5f130da71f6321fee99dc1efc3a7da
VENV_SHA256=e1d7c93fd9607f84a7b262d36458c5eae95f42c26fcb03a86ad55f687bd1e689
PYZ="${WORK}/tools/virtualenv.pyz"
[ -f "${PYZ}" ] || curl -sSL -o "${PYZ}" \
  "https://raw.githubusercontent.com/pypa/get-virtualenv/${VENV_COMMIT}/public/virtualenv.pyz"
echo "${VENV_SHA256}  ${PYZ}" | sha256sum -c -

# 2) isolated venv (no system site-packages) + pinned dependencies
[ -x "${WORK}/venv/bin/python" ] || python3 "${PYZ}" --no-download "${WORK}/venv"
"${WORK}/venv/bin/python" -m pip install --no-cache-dir opencv-python-headless==5.0.0.93

# 3) OpenCV Zoo YOLOX-s models (Git LFS), pinned commit, verified against LFS oid
ZOO_COMMIT=47534e27c9851bb1128ccc0102f1145e27f23f98
ZOO_DIR=models/object_detection_yolox
declare -A OID=(
  [object_detection_yolox_2022nov.onnx]=c5c2d13e59ae883e6af3b45daea64af4833a4951c92d116ec270d9ddbe998063
  [object_detection_yolox_2022nov_int8.onnx]=01a3b0f400b30bc1e45230e991b2e499ab42622485a330021947333fbaf03935
)
for f in "${!OID[@]}"; do
  [ -f "${WORK}/models/${f}" ] || curl -sSL -o "${WORK}/models/${f}" \
    "https://media.githubusercontent.com/media/opencv/opencv_zoo/${ZOO_COMMIT}/${ZOO_DIR}/${f}"
  echo "${OID[$f]}  ${WORK}/models/${f}" | sha256sum -c -
done
[ -f "${WORK}/models/LICENSE.yolox" ] || curl -sSL -o "${WORK}/models/LICENSE.yolox" \
  "https://raw.githubusercontent.com/opencv/opencv_zoo/${ZOO_COMMIT}/${ZOO_DIR}/LICENSE"

# 4) COCO val2017 annotations (ids, boxes, per-image licence); images are fetched by fetch_assets.py
if [ ! -f "${WORK}/cache/annotations/instances_val2017.json" ]; then
  curl -sSL -o "${WORK}/cache/ann.zip" http://images.cocodataset.org/annotations/annotations_trainval2017.zip
  (cd "${WORK}/cache" && "${WORK}/venv/bin/python" -m zipfile -e ann.zip .)
fi

echo "Environment ready. Run (ROS-safe):"
echo "  env -u PYTHONPATH -u LD_LIBRARY_PATH ${WORK}/venv/bin/python -E -s fetch_assets.py"
echo "  env -u PYTHONPATH -u LD_LIBRARY_PATH ${WORK}/venv/bin/python -E -s run_eval.py"
