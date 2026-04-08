from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil
import tkinter as tk
from tkinter import messagebox

from PIL import Image, ImageTk, UnidentifiedImageError


IMAGE_EXTENSIONS = {".jpg"}
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 980
MAX_DISPLAY_WIDTH = 1100
MAX_DISPLAY_HEIGHT = 840

# Easy to modify: map number key -> class folder name.
CLASS_LABELS: dict[str, str] = {
    "0": "show",
    "1": "john ground",
    "2": "jane ground",
    "3": "TREEEEEEEEEEEEEEEEEEEEEEEEEE",
    "4": "rock",
    "5": "orck",
    "6": "kcor",
    "7": "not ground",
    "8": "lava",
    "9": "H U H",
}


@dataclass(slots=True)
class ImageEntry:
    path: Path
    split: str


class ImageClassifierApp:
    def __init__(self, root: tk.Tk, data_root: Path) -> None:
        self.root = root
        self.data_root = data_root
        self.unclassified_root = self.data_root / "cut_images" / "unclassified"
        self.classified_root = self.data_root / "cut_images" / "classified"

        self.entries: list[ImageEntry] = self._load_entries()
        self.current_index = 0
        self.current_tk_image: ImageTk.PhotoImage | None = None
        self.split_counts = self._compute_split_counts()
        self.class_help_text = " | ".join(
            f"{k}:{v}" for k, v in sorted(CLASS_LABELS.items(), key=lambda item: item[0])
        )

        self._build_ui()
        self._bind_keys()
        self._show_current_image()

    def _build_ui(self) -> None:
        self.root.title("CIV4 Image Classifier")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.root.maxsize(WINDOW_WIDTH, WINDOW_HEIGHT)

        self.main_frame = tk.Frame(self.root, padx=12, pady=12)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.info_label = tk.Label(
            self.main_frame,
            text="",
            anchor="w",
            justify=tk.LEFT,
            font=("Segoe UI", 11),
        )
        self.info_label.pack(fill=tk.X, pady=(0, 10))

        self.image_container = tk.Frame(
            self.main_frame,
            width=MAX_DISPLAY_WIDTH,
            height=MAX_DISPLAY_HEIGHT,
            bg="#111111",
        )
        self.image_container.pack(fill=tk.BOTH, expand=False)
        self.image_container.pack_propagate(False)

        self.image_label = tk.Label(self.image_container, bg="#111111")
        self.image_label.pack(fill=tk.BOTH, expand=True)

        self.help_label = tk.Label(
            self.main_frame,
            text=f"Class keys: {self.class_help_text} | Press Q to quit.",
            anchor="w",
            justify=tk.LEFT,
            font=("Segoe UI", 10),
            wraplength=WINDOW_WIDTH - 40,
        )
        self.help_label.pack(fill=tk.X, pady=(10, 0))

    def _bind_keys(self) -> None:
        self.root.bind("<Key>", self._on_key_press)

    def _load_entries(self) -> list[ImageEntry]:
        entries: list[ImageEntry] = []
        if not self.unclassified_root.exists():
            return entries

        for split_dir in sorted(p for p in self.unclassified_root.iterdir() if p.is_dir()):
            split = split_dir.name
            for file_path in sorted(split_dir.rglob("*")):
                if file_path.is_file() and file_path.suffix.lower() in IMAGE_EXTENSIONS:
                    entries.append(ImageEntry(path=file_path, split=split))
        return entries

    def _compute_split_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for entry in self.entries:
            counts[entry.split] = counts.get(entry.split, 0) + 1
        return counts

    def _on_key_press(self, event: tk.Event) -> None:
        key = event.char
        if not key:
            return

        if key.lower() == "q":
            self.root.destroy()
            return

        if key in CLASS_LABELS:
            self._classify_current_image(key)

    def _classify_current_image(self, class_id: str) -> None:
        if not self.entries:
            return

        class_label = CLASS_LABELS[class_id]
        entry = self.entries[self.current_index]
        destination_dir = self.classified_root / entry.split / class_label
        destination_dir.mkdir(parents=True, exist_ok=True)

        destination_path = self._get_available_destination(destination_dir, entry.path.name)
        shutil.move(str(entry.path), str(destination_path))

        self.split_counts[entry.split] = max(0, self.split_counts.get(entry.split, 1) - 1)
        del self.entries[self.current_index]

        if self.current_index >= len(self.entries):
            self.current_index = 0

        self._show_current_image()

    @staticmethod
    def _get_available_destination(destination_dir: Path, filename: str) -> Path:
        candidate = destination_dir / filename
        if not candidate.exists():
            return candidate

        stem = candidate.stem
        suffix = candidate.suffix
        counter = 1
        while True:
            next_candidate = destination_dir / f"{stem}_{counter}{suffix}"
            if not next_candidate.exists():
                return next_candidate
            counter += 1

    def _show_current_image(self) -> None:
        if not self.entries:
            self.image_label.configure(
                image="",
                text="No images left to classify.",
                fg="white",
                font=("Segoe UI", 18),
            )
            self.info_label.configure(text="Done. No unclassified images found.")
            return

        entry = self.entries[self.current_index]
        info_text = (
            f"Image: {entry.path.name} | "
            f"Split: {entry.split} | "
            f"Remaining in split: {self.split_counts.get(entry.split, 0)} | "
            f"Total remaining: {len(self.entries)}"
        )
        self.info_label.configure(text=info_text)

        try:
            with Image.open(entry.path) as image:
                image = image.convert("RGB")
                image.thumbnail((MAX_DISPLAY_WIDTH, MAX_DISPLAY_HEIGHT), Image.Resampling.LANCZOS)
                self.current_tk_image = ImageTk.PhotoImage(image)
        except (UnidentifiedImageError, OSError) as exc:
            messagebox.showwarning("Unreadable image", f"Skipping unreadable image:\n{entry.path}\n\n{exc}")
            del self.entries[self.current_index]
            if self.current_index >= len(self.entries):
                self.current_index = 0
            self._show_current_image()
            return

        self.image_label.configure(image=self.current_tk_image, text="")


def main() -> None:
    project_root = Path(__file__).resolve().parents[1]
    data_root = project_root / "data"

    root = tk.Tk()
    ImageClassifierApp(root=root, data_root=data_root)
    root.mainloop()


if __name__ == "__main__":
    main()
