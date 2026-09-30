"""OpenCV 5 cv.dnn YOLOX-s detector wrapper (Phase 1A feasibility only).

Adapted from the OpenCV Zoo reference implementation
(opencv_zoo/models/object_detection_yolox/yolox.py, Apache-2.0).
Inference is executed by cv2.dnn; the engine is selected explicitly so the
ONNX Runtime engine (cv2.dnn.ENGINE_ORT) can never be used by accident.
"""
import time
from pathlib import Path

import cv2
import numpy as np

WORK = Path.home() / "opencv26_work"
MODEL_FP32 = WORK / "models" / "object_detection_yolox_2022nov.onnx"
MODEL_INT8 = WORK / "models" / "object_detection_yolox_2022nov_int8.onnx"

COCO_CAT, COCO_DOG = 15, 16  # 0-based indices in the 80-class COCO list
CLASS_NAMES = {COCO_CAT: "cat", COCO_DOG: "dog"}

ENGINES = {
    "new": cv2.dnn.ENGINE_NEW,
    "classic": cv2.dnn.ENGINE_CLASSIC,
}  # ENGINE_ORT deliberately excluded


def letterbox(img, size=640):
    padded = np.full((size, size, 3), 114.0, np.float32)
    ratio = min(size / img.shape[0], size / img.shape[1])
    h, w = int(img.shape[0] * ratio), int(img.shape[1] * ratio)
    padded[:h, :w] = cv2.resize(img, (w, h), interpolation=cv2.INTER_LINEAR)
    return padded, ratio


class YoloxDetector:
    def __init__(self, model_path=MODEL_FP32, engine="new", conf=0.05, nms=0.5):
        self.engine_name = engine
        self.net = cv2.dnn.readNetFromONNX(str(model_path), ENGINES[engine])
        self.net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
        self.net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)
        self.conf, self.nms = conf, nms
        self.size, self.strides = 640, [8, 16, 32]
        self.out_name = self.net.getUnconnectedOutLayersNames()
        grids, strides = [], []
        for s in self.strides:
            n = self.size // s
            xv, yv = np.meshgrid(np.arange(n), np.arange(n))
            g = np.stack((xv, yv), 2).reshape(1, -1, 2)
            grids.append(g)
            strides.append(np.full((1, g.shape[1], 1), s))
        self.grids = np.concatenate(grids, 1)
        self.expanded_strides = np.concatenate(strides, 1)

    def detect(self, bgr):
        """Return (detections, timing_ms). detections rows:
        [x, y, w, h, score, class_id] in original-image pixels."""
        t0 = time.perf_counter()
        padded, ratio = letterbox(bgr, self.size)
        blob = np.transpose(padded, (2, 0, 1))[np.newaxis]
        self.net.setInput(blob)
        t1 = time.perf_counter()
        out = self.net.forward(self.out_name)[0][0]
        t2 = time.perf_counter()

        d = out.copy()
        d[:, :2] = (d[:, :2] + self.grids[0]) * self.expanded_strides[0]
        d[:, 2:4] = np.exp(d[:, 2:4]) * self.expanded_strides[0]
        xywh = np.empty((len(d), 4), np.float32)
        xywh[:, 0] = d[:, 0] - d[:, 2] / 2
        xywh[:, 1] = d[:, 1] - d[:, 3] / 2
        xywh[:, 2:] = d[:, 2:4]
        scores = d[:, 4:5] * d[:, 5:]
        best = scores.max(1)
        cls = scores.argmax(1)
        keep = cv2.dnn.NMSBoxesBatched(
            xywh.tolist(), best.tolist(), cls.tolist(), self.conf, self.nms
        )
        if len(keep) == 0:
            dets = np.zeros((0, 6), np.float32)
        else:
            keep = np.array(keep).reshape(-1)
            dets = np.concatenate(
                [xywh[keep] / ratio, best[keep, None], cls[keep, None]], 1
            )
        t3 = time.perf_counter()
        return dets, {
            "pre_ms": (t1 - t0) * 1e3,
            "forward_ms": (t2 - t1) * 1e3,
            "post_ms": (t3 - t2) * 1e3,
            "total_ms": (t3 - t0) * 1e3,
        }


def iou_xywh(a, b):
    ax2, ay2, bx2, by2 = a[0] + a[2], a[1] + a[3], b[0] + b[2], b[1] + b[3]
    iw = max(0.0, min(ax2, bx2) - max(a[0], b[0]))
    ih = max(0.0, min(ay2, by2) - max(a[1], b[1]))
    inter = iw * ih
    union = a[2] * a[3] + b[2] * b[3] - inter
    return inter / union if union > 0 else 0.0
