"""Phase 1A evaluation: OpenCV 5 cv.dnn + YOLOX-s cat/dog detection.

Run with the isolated venv, e.g.
  env -u PYTHONPATH -u LD_LIBRARY_PATH ~/opencv26_work/venv/bin/python -I run_eval.py

Writes results/samples.csv, results/summary.json, results/summary.md.
No ROS2, AWS or robot control is involved.
"""
import csv
import json
import platform
import statistics as st
from pathlib import Path

import cv2
import numpy as np

from common import (CLASS_NAMES, COCO_CAT, COCO_DOG, MODEL_FP32, MODEL_INT8,
                    WORK, YoloxDetector, iou_xywh)

HERE = Path(__file__).parent
RES = HERE / "results"
IMG_DIR = WORK / "images"
CONF_T, IOU_T = 0.4, 0.5
GATE = {"recall": 0.85, "fp": 0.05, "latency_ms": 200.0}
RNG = np.random.default_rng(26)

POS_CONDITIONS = ["clear", "occ40", "occ70", "blur3", "blur6",
                  "dark40", "dark20", "far33", "far20"]
NEG_CONDITIONS = ["clear", "blur6", "dark20"]


# ---- degradations (applied to a copy; GT box adjusted where geometry changes)
def occlude(img, box, frac, idx):
    x, y, w, h = [int(v) for v in box]
    out = img.copy()
    if idx % 2 == 0:  # from the bottom (furniture-like)
        out[y + int(h * (1 - frac)): y + h, x: x + w] = (60, 60, 60)
    else:             # from the left
        out[y: y + h, x: x + int(w * frac)] = (60, 60, 60)
    return out


def darken(img, gain):
    f = img.astype(np.float32) * gain + RNG.normal(0, 6, img.shape)
    return np.clip(f, 0, 255).astype(np.uint8)


def shrink(img, box, s):
    h, w = img.shape[:2]
    small = cv2.resize(img, (int(w * s), int(h * s)), interpolation=cv2.INTER_AREA)
    canvas = np.full_like(img, 114)
    ox, oy = (w - small.shape[1]) // 2, (h - small.shape[0]) // 2
    canvas[oy: oy + small.shape[0], ox: ox + small.shape[1]] = small
    nb = [box[0] * s + ox, box[1] * s + oy, box[2] * s, box[3] * s]
    return canvas, nb


def apply(cond, img, box, idx):
    if cond == "clear":
        return img, box
    if cond == "occ40":
        return occlude(img, box, 0.4, idx), box
    if cond == "occ70":
        return occlude(img, box, 0.7, idx), box
    if cond == "blur3":
        return cv2.GaussianBlur(img, (0, 0), 3), box
    if cond == "blur6":
        return cv2.GaussianBlur(img, (0, 0), 6), box
    if cond == "dark40":
        return darken(img, 0.4), box
    if cond == "dark20":
        return darken(img, 0.2), box
    if cond == "far33":
        return shrink(img, box, 1 / 3)
    if cond == "far20":
        return shrink(img, box, 1 / 5)
    raise ValueError(cond)


# ---- evaluation of one image
def evaluate(det, e, cond, img, box, idx):
    im, gt_box = apply(cond, img, box, idx)
    dets, tm = det.detect(im)
    pet = dets[np.isin(dets[:, 5], [COCO_CAT, COCO_DOG])]
    best = {n: float(pet[pet[:, 5] == c][:, 4].max()) if (pet[:, 5] == c).any() else 0.0
            for c, n in CLASS_NAMES.items()}
    above = pet[pet[:, 4] >= CONF_T]
    row = {"coco_id": e["coco_id"], "role": e["role"], "condition": cond,
           "gt_class": e.get("gt_class") or "", "best_cat_conf": round(best["cat"], 3),
           "best_dog_conf": round(best["dog"], 3),
           "n_pet_dets_ge_0.4": len(above),
           "pred": ";".join(f"{CLASS_NAMES[int(r[5])]}:{r[4]:.2f}:[{r[0]:.0f},{r[1]:.0f},{r[2]:.0f},{r[3]:.0f}]"
                            for r in above),
           "pre_ms": round(tm["pre_ms"], 1), "forward_ms": round(tm["forward_ms"], 1),
           "post_ms": round(tm["post_ms"], 1), "total_ms": round(tm["total_ms"], 1)}
    if e["role"].startswith("pos"):
        gt_c = COCO_CAT if e["gt_class"] == "cat" else COCO_DOG
        cls_ok = any(r[5] == gt_c and iou_xywh(r[:4], gt_box) >= IOU_T for r in above)
        any_ok = any(iou_xywh(r[:4], gt_box) >= IOU_T for r in above)
        row.update(correct=int(cls_ok), pet_any_correct=int(any_ok),
                   gt_conf=round(best[e["gt_class"]], 3))
    else:
        row.update(correct=int(len(above) == 0), pet_any_correct="", gt_conf="")  # correct = no false alarm
    return row


def run_config(det, entries, label, pos_conds, neg_conds):
    rows = []
    for i, e in enumerate(entries):
        img = cv2.imread(str(IMG_DIR / e["file"]))
        conds = pos_conds if e["role"].startswith("pos") else neg_conds
        for c in conds:
            r = evaluate(det, e, c, img, e["gt_bbox"], i)
            r["config"] = label
            rows.append(r)
    return rows


def pct(n, d):
    return round(100.0 * n / d, 1) if d else None


def summarize(rows):
    out = {}
    for cond in POS_CONDITIONS:
        for grp, roles in (("cat", ("pos_cat",)), ("dog", ("pos_dog",)),
                           ("pets", ("pos_cat", "pos_dog"))):
            rs = [r for r in rows if r["role"] in roles and r["condition"] == cond]
            if not rs:
                continue
            confs = [r["gt_conf"] for r in rs]
            out[f"pos/{grp}/{cond}"] = {
                "n": len(rs),
                "detect_rate_pct": pct(sum(r["correct"] for r in rs), len(rs)),
                "pet_any_rate_pct": pct(sum(r["pet_any_correct"] for r in rs), len(rs)),
                # presence: any cat/dog detection >= CONF_T anywhere (no IoU requirement)
                "presence_rate_pct": pct(sum(1 for r in rs if r["n_pet_dets_ge_0.4"] > 0), len(rs)),
                "gt_conf_median": round(st.median(confs), 3),
                "gt_conf_q1_q3": [round(float(np.percentile(confs, 25)), 3),
                                  round(float(np.percentile(confs, 75)), 3)],
                "gt_conf_min_max": [min(confs), max(confs)],
            }
    for grp, roles in (("all_neg", ("neg", "hard_neg_teddy", "hard_neg_furniture")),
                       ("easy_neg", ("neg",)), ("hard_teddy", ("hard_neg_teddy",)),
                       ("hard_furniture", ("hard_neg_furniture",))):
        for cond in NEG_CONDITIONS:
            rs = [r for r in rows if r["role"] in roles and r["condition"] == cond]
            if not rs:
                continue
            fps = [r for r in rs if not r["correct"]]
            mx = [max(r["best_cat_conf"], r["best_dog_conf"]) for r in rs]
            out[f"neg/{grp}/{cond}"] = {
                "n": len(rs), "false_alarm_pct": pct(len(fps), len(rs)),
                "false_alarm_ids": [r["coco_id"] for r in fps],
                "max_pet_conf_median": round(st.median(mx), 3),
                "max_pet_conf_max": round(max(mx), 3)}
    # paired: degraded failure vs clear success
    pos = [r for r in rows if r["role"].startswith("pos")]
    clear = {r["coco_id"]: r["correct"] for r in pos if r["condition"] == "clear"}
    paired = {}
    for cond in POS_CONDITIONS[1:]:
        rs = [r for r in pos if r["condition"] == cond]
        fail = [r for r in rs if not r["correct"]]
        rec = [r for r in fail if clear.get(r["coco_id"])]
        paired[cond] = {"n": len(rs), "failed_when_degraded": len(fail),
                        "of_which_detected_when_clear": len(rec),
                        "recovered_by_clear_view_pct": pct(len(rec), len(fail)),
                        "clear_detect_pct": pct(sum(clear[r["coco_id"]] for r in rs), len(rs)),
                        "degraded_detect_pct": pct(len(rs) - len(fail), len(rs))}
    out["paired"] = paired
    return out


def latency(rows):
    t = [r["total_ms"] for r in rows]
    f = [r["forward_ms"] for r in rows]
    return {"n": len(t), "total_ms_mean": round(st.mean(t), 1),
            "total_ms_median": round(st.median(t), 1),
            "total_ms_p95": round(float(np.percentile(t, 95)), 1),
            "forward_ms_mean": round(st.mean(f), 1),
            "fps_mean": round(1000.0 / st.mean(t), 2)}


def write_markdown(info, lat, summaries, gate):
    s = summaries["fp32-new"]
    L = ["# Phase 1A results (auto-generated by run_eval.py)", "",
         f"OpenCV {info['cv2_version']} / numpy {info['numpy']} / {info['cpu']} / "
         f"{info['threads']} threads. cv.dnn backend={info['dnn_backend']}, "
         f"target={info['dnn_target']}, engine=ENGINE_NEW (main), ENGINE_CLASSIC (comparison). "
         f"Build: {'; '.join(info['build_lines'])}.", "",
         f"Decision: conf >= {CONF_T}; 'detect' = right class and IoU >= {IOU_T} with the GT box; "
         "'presence' = any cat/dog detection >= threshold (no IoU).", "",
         "## Positives by condition (n = cats + dogs)", "",
         "| condition | n | detect % | presence % | GT-class conf median [Q1,Q3] | cat % | dog % |",
         "|---|---|---|---|---|---|---|"]
    for c in POS_CONDITIONS:
        a, k, d = s[f"pos/pets/{c}"], s[f"pos/cat/{c}"], s[f"pos/dog/{c}"]
        L.append(f"| {c} | {a['n']} | {a['detect_rate_pct']} | {a['presence_rate_pct']} | "
                 f"{a['gt_conf_median']} {a['gt_conf_q1_q3']} | {k['detect_rate_pct']} | {d['detect_rate_pct']} |")
    L += ["", "## Negatives: false-alarm % (any cat/dog >= threshold)", "",
          "| group | clear | blur6 | dark20 | n (clear) | false-alarm COCO ids (clear) |", "|---|---|---|---|---|---|"]
    for g in ("easy_neg", "hard_teddy", "hard_furniture", "all_neg"):
        v = s[f"neg/{g}/clear"]
        L.append(f"| {g} | {v['false_alarm_pct']} | {s[f'neg/{g}/blur6']['false_alarm_pct']} | "
                 f"{s[f'neg/{g}/dark20']['false_alarm_pct']} | {v['n']} | {v['false_alarm_ids']} |")
    L += ["", "## Paired: degraded failures vs clear view", "",
          "| condition | detect % degraded | detect % clear | failed when degraded | of which detected when clear | recovered % |",
          "|---|---|---|---|---|---|"]
    for c, v in s["paired"].items():
        L.append(f"| {c} | {v['degraded_detect_pct']} | {v['clear_detect_pct']} | {v['failed_when_degraded']} | "
                 f"{v['of_which_detected_when_clear']} | {v['recovered_by_clear_view_pct']} |")
    L += ["", "## Latency (ms per frame, end-to-end = preprocess + forward + postprocess)", "",
          "| config | n | total mean | median | p95 | forward mean | FPS |", "|---|---|---|---|---|---|---|"]
    for k, v in lat.items():
        L.append(f"| {k} | {v['n']} | {v['total_ms_mean']} | {v['total_ms_median']} | {v['total_ms_p95']} | "
                 f"{v['forward_ms_mean']} | {v['fps_mean']} |")
    L += ["", "## Gate", "", "```json", json.dumps(gate, indent=1), "```", ""]
    (RES / "summary.md").write_text("\n".join(L))


def warmup(det, img, n=5):
    for _ in range(n):
        det.detect(img)


def main():
    RES.mkdir(exist_ok=True)
    man = json.load(open(RES / "manifest.json"))
    entries = man["entries"]
    warm_img = cv2.imread(str(IMG_DIR / entries[0]["file"]))

    bi = cv2.getBuildInformation()
    info = {
        "cv2_version": cv2.__version__, "cv2_file": cv2.__file__.replace(str(Path.home()), "~"),
        "numpy": np.__version__, "python": platform.python_version(),
        "dnn_backend": "DNN_BACKEND_OPENCV", "dnn_target": "DNN_TARGET_CPU",
        "threads": cv2.getNumThreads(),
        "build_lines": [l.strip() for l in bi.splitlines()
                        if any(k in l for k in ("ONNX Runtime", "Parallel framework", "DNN MLAS"))],
        "cpu": next((l.split(":", 1)[1].strip() for l in open("/proc/cpuinfo")
                     if l.startswith("model name")), "?"),
        "model_fp32": MODEL_FP32.name, "model_fp32_bytes": MODEL_FP32.stat().st_size,
        "model_int8": MODEL_INT8.name, "model_int8_bytes": MODEL_INT8.stat().st_size,
        "conf_threshold": CONF_T, "iou_threshold": IOU_T,
    }

    # ---- main configuration: FP32 + new engine, all conditions
    det = YoloxDetector(MODEL_FP32, engine="new")
    warmup(det, warm_img)
    rows = run_config(det, entries, "fp32-new", POS_CONDITIONS, NEG_CONDITIONS)
    summaries = {"fp32-new": summarize(rows)}
    lat = {"fp32-new": latency(rows)}
    lat["fp32-new/clear-only"] = latency([r for r in rows if r["condition"] == "clear"])

    # ---- comparison configurations: clear images only
    clear_only = (["clear"], ["clear"])
    for label, path, eng in (("fp32-classic", MODEL_FP32, "classic"),
                             ("int8-new", MODEL_INT8, "new")):
        d = YoloxDetector(path, engine=eng)
        warmup(d, warm_img)
        rs = run_config(d, entries, label, *clear_only)
        rows += rs
        summaries[label] = summarize(rs)
        lat[label] = latency(rs)

    cv2.setNumThreads(1)
    d1 = YoloxDetector(MODEL_FP32, engine="new")
    warmup(d1, warm_img)
    rs = run_config(d1, entries, "fp32-new-1thread", *clear_only)
    rows += rs
    lat["fp32-new-1thread"] = latency(rs)
    cv2.setNumThreads(info["threads"])

    cols = list(rows[0].keys())
    cols = ["config"] + [c for c in cols if c != "config"]
    with open(RES / "samples.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    json.dump({"info": info, "latency": lat, "summary": summaries},
              open(RES / "summary.json", "w"), indent=1)

    # ---- gate check on the main configuration
    s = summaries["fp32-new"]
    g = {
        "clear_recall_pets_pct": s["pos/pets/clear"]["detect_rate_pct"],
        "clear_recall_cat_pct": s["pos/cat/clear"]["detect_rate_pct"],
        "clear_recall_dog_pct": s["pos/dog/clear"]["detect_rate_pct"],
        "all_negative_false_alarm_pct": s["neg/all_neg/clear"]["false_alarm_pct"],
        "hard_negative_false_alarm_pct": pct(
            sum(len(s[f"neg/{k}/clear"]["false_alarm_ids"]) for k in ("hard_teddy", "hard_furniture")),
            s["neg/hard_teddy/clear"]["n"] + s["neg/hard_furniture/clear"]["n"]),
        "latency_total_ms_mean": lat["fp32-new/clear-only"]["total_ms_mean"],
    }
    g["pass_recall"] = g["clear_recall_pets_pct"] >= GATE["recall"] * 100
    g["pass_false_alarm"] = g["all_negative_false_alarm_pct"] <= GATE["fp"] * 100
    g["pass_latency"] = g["latency_total_ms_mean"] <= GATE["latency_ms"]
    json.dump(g, open(RES / "gate.json", "w"), indent=1)
    write_markdown(info, lat, summaries, g)
    print(json.dumps({"info": info, "gate": g, "latency": lat}, indent=1))


if __name__ == "__main__":
    main()
