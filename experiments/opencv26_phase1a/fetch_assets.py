"""Select and download the Phase 1A evaluation images from COCO val2017.

Only ID/licence/source metadata is written into the repo (manifest.json).
Images are downloaded to ~/opencv26_work/images and never committed.

Licence filter: only COCO licence ids 4 (CC BY), 5 (CC BY-SA),
7 (no known copyright) and 8 (US Gov) are used. NonCommercial and
NoDerivs images are excluded.
"""
import json
import random
import urllib.request
from pathlib import Path

WORK = Path.home() / "opencv26_work"
ANN = WORK / "cache" / "annotations" / "instances_val2017.json"
IMG_DIR = WORK / "images"
OUT = Path(__file__).parent / "results" / "manifest.json"

ALLOWED_LICENSES = {4, 5, 7, 8}
CAT, DOG, TEDDY, COUCH, BED = 17, 18, 88, 63, 65  # COCO category ids (1-based)
SEED = 26
N_CAT, N_DOG, N_NEG, N_HARD_TEDDY, N_HARD_FURN = 30, 30, 30, 10, 10
MIN_BOX_FRAC = 0.05  # "clear" pet: box covers >= 5% of the image (10% gave only 27 cats/19 dogs under the licence filter)


def main():
    d = json.load(open(ANN))
    imgs = {i["id"]: i for i in d["images"]}
    anns_by_img = {}
    for a in d["annotations"]:
        anns_by_img.setdefault(a["image_id"], []).append(a)

    def cats_in(iid):
        return {a["category_id"] for a in anns_by_img.get(iid, [])}

    def ok_license(iid):
        return imgs[iid]["license"] in ALLOWED_LICENSES

    def clear_single(iid, cat):
        anns = [a for a in anns_by_img.get(iid, []) if a["category_id"] in (CAT, DOG)]
        if len(anns) != 1 or anns[0]["category_id"] != cat or anns[0]["iscrowd"]:
            return None
        w, h = imgs[iid]["width"], imgs[iid]["height"]
        bw, bh = anns[0]["bbox"][2], anns[0]["bbox"][3]
        return anns[0] if bw * bh >= MIN_BOX_FRAC * w * h else None

    rng = random.Random(SEED)
    ids = sorted(imgs)
    rng.shuffle(ids)

    entries = []

    def take(role, cat, n, pred):
        got = 0
        for iid in ids:
            if got >= n:
                break
            if not ok_license(iid) or any(e["coco_id"] == iid for e in entries):
                continue
            a = pred(iid)
            if a is None:
                continue
            im = imgs[iid]
            entries.append({
                "role": role, "coco_id": iid, "file": im["file_name"],
                "coco_url": im["coco_url"], "flickr_url": im["flickr_url"],
                "license_id": im["license"], "width": im["width"], "height": im["height"],
                "gt_class": {CAT: "cat", DOG: "dog"}.get(a) if isinstance(a, int) else None,
                "gt_bbox": a["bbox"] if isinstance(a, dict) else None,
            })
            if isinstance(a, dict):
                entries[-1]["gt_class"] = {CAT: "cat", DOG: "dog"}[a["category_id"]]
            got += 1
        print(f"{role}: selected {got}/{n}")

    take("pos_cat", CAT, N_CAT, lambda i: clear_single(i, CAT))
    take("pos_dog", DOG, N_DOG, lambda i: clear_single(i, DOG))
    no_pet = lambda i: not (cats_in(i) & {CAT, DOG})
    take("hard_neg_teddy", None, N_HARD_TEDDY,
         lambda i: 0 if no_pet(i) and TEDDY in cats_in(i) else None)
    take("hard_neg_furniture", None, N_HARD_FURN,
         lambda i: 0 if no_pet(i) and (cats_in(i) & {COUCH, BED}) and TEDDY not in cats_in(i) else None)
    take("neg", None, N_NEG,
         lambda i: 0 if no_pet(i) and not (cats_in(i) & {TEDDY, COUCH, BED}) else None)

    IMG_DIR.mkdir(parents=True, exist_ok=True)
    for e in entries:
        p = IMG_DIR / e["file"]
        if not p.exists():
            urllib.request.urlretrieve(e["coco_url"], p)
    OUT.parent.mkdir(exist_ok=True)
    json.dump({"seed": SEED, "allowed_license_ids": sorted(ALLOWED_LICENSES),
               "licenses": {str(l["id"]): l["name"] for l in d["licenses"]},
               "entries": entries}, open(OUT, "w"), indent=1)
    print("total", len(entries), "->", OUT)


if __name__ == "__main__":
    main()
