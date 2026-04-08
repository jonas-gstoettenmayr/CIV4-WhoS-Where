"""Some utitlity functions for this project"""
from pathlib import Path
from typing import Literal

import numpy as np
from sklearn.cluster import DBSCAN
import pandas as pd

cwd = Path.cwd().resolve()
PROJECT_ROOT = cwd.parent if cwd.name == "notebooks" else cwd
SPLITS = ("train", "val", "test")
IMG_SIZES = (1024, 1024)


def resolve_frame_paths(frame_id: str) -> tuple[Literal['train', 'val', 'test'], Path, Path]:
    """Find the split (train/val/test) where both image and label exist for a frame.
    
    Args:
        frame_id (str): the id of the frame to search for, e.g. 103_1111
    
    Returns:
        tuple[Literal['train', 'val', 'test'], Path, Path]: the split as a str,
        the path of the image and the path of the label
    """
    for split in SPLITS:
        image_path = PROJECT_ROOT / "data" / "rgb_images" / split / f"{frame_id}.jpg"
        label_path = PROJECT_ROOT / "data" / "labels_matched_rgb" / split / f"{frame_id}.txt"
        if image_path.exists() and label_path.exists():
            return split, image_path, label_path

    raise FileNotFoundError(
        f"Could not find matching JPG and TXT for frame '{frame_id}' in train/val/test."
    )

def build_group_boxes(
    frame_boxes: pd.DataFrame,
    padding_ratio: float = 0.2,
    min_size: float = 100.0,
    eps_scale: float = 4
) -> pd.DataFrame:
    """
    Cluster animal boxes for a single frame with DBSCAN and return grouped boxes.

    Expected input columns: class_id, txt_x1, txt_y1, txt_w, txt_h
    Returns one row per cluster with padded group box + species list.

    padding_ratio is percentage padding per side (0.12 = 12% of cluster width/height).
    """
    required_cols = ["class_id", "txt_x1", "txt_y1", "txt_x2", "txt_y2", "txt_w", "txt_h"]
    if padding_ratio < 0:
        raise ValueError("padding_ratio must be >= 0")
    if frame_boxes.empty:
        return pd.DataFrame(columns=["cluster_id","group_x1","group_y1",\
            "group_w","group_h","n_animals","species_in_cluster"])

    boxes = frame_boxes[required_cols].copy()


    boxes["cx"] = boxes["txt_x1"] + boxes["txt_w"] / 2.0
    boxes["cy"] = boxes["txt_y1"] + boxes["txt_h"] / 2.0

    if len(boxes) == 1:
        boxes["cluster_id"] = 0
    else:
        diag = np.sqrt(np.square(boxes["txt_w"].values) + np.square(boxes["txt_h"].values))
        dynamic_eps = max(20.0, float(np.median(diag)) * eps_scale)
        features = boxes[["cx", "cy"]].to_numpy()
        labels = DBSCAN(eps=dynamic_eps, min_samples=1).fit_predict(features)
        boxes["cluster_id"] = labels

    grouped_rows = []
    for cluster_id, group in boxes.groupby("cluster_id", sort=True):
        raw_x1 = float(group["txt_x1"].min())
        raw_y1 = float(group["txt_y1"].min())
        raw_x2 = float(group["txt_x2"].max())
        raw_y2 = float(group["txt_y2"].max())

        raw_w = max(1.0, raw_x2 - raw_x1)
        raw_h = max(1.0, raw_y2 - raw_y1)
        pad_x = raw_w * padding_ratio
        pad_y = raw_h * padding_ratio

        x1 = raw_x1 - pad_x
        y1 = raw_y1 - pad_y
        x2 = raw_x2 + pad_x
        y2 = raw_y2 + pad_y

        width = x2 - x1
        height = y2 - y1

        if width < min_size:
            delta = (min_size - width) / 2.0
            x1 -= delta
            x2 += delta
            width = min_size

        if height < min_size:
            delta = (min_size - height) / 2.0
            y1 -= delta
            y2 += delta
            height = min_size

        # species_list = group["class_id"].astype(str).unique().tolist()
        counts = group["class_id"].value_counts().to_dict()
        grouped_rows.append(
            {
                "cluster_id": cluster_id,
                "group_x1": max(0.0, x1),
                "group_y1": max(0.0, y1),
                "group_w": width,
                "group_h": height,
                "n_animals": int(len(group)),
                "species_in_cluster": [(species, count) for species, count in counts.items()],
            }
        )

    return pd.DataFrame(grouped_rows).sort_values("cluster_id").reset_index(drop=True)

if __name__ == "__main__":
    print("Hi")
