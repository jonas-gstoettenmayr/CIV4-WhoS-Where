"""Some utitlity functions for this project"""
from pathlib import Path
from typing import Literal

cwd = Path.cwd().resolve()
PROJECT_ROOT = cwd.parent if cwd.name == "notebooks" else cwd
SPLITS = ("train", "val", "test")
IMG_SIZES = (1024, 1024)


def resolve_frame_paths(frame_id: str) -> tuple[Literal['train', 'val', 'test'], Path, Path]:
    """Find the split (train/val/test) where both image and label exist for a frame.
    
    Args:
        frame_id (str): the id of the frame to search for, e.g. 103_1111
    
    Returns:
        tuple[Literal['train', 'val', 'test'], Path, Path]: the split as a str, the path of the image and the path of the label
    """
    for split in SPLITS:
        image_path = PROJECT_ROOT / "data" / "rgb_images" / split / f"{frame_id}.jpg"
        label_path = PROJECT_ROOT / "data" / "labels_matched_rgb" / split / f"{frame_id}.txt"
        if image_path.exists() and label_path.exists():
            return split, image_path, label_path

    raise FileNotFoundError(
        f"Could not find matching JPG and TXT for frame '{frame_id}' in train/val/test."
    )