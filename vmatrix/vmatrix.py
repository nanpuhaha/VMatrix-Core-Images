import itertools
from pathlib import Path
from typing import NamedTuple

import cv2
import numpy as np
from cv import contains_alpha_channel, imread, write
from PIL import Image

PROJECT_DIR = Path(__file__).parent.parent
IMG_DIR = PROJECT_DIR / "img"
SKILL_DIR = IMG_DIR / "skills"
UI_DIR = IMG_DIR / "VMatrixUI"
LEFT_MASK = imread(UI_DIR / "VMatrix.iconMask.3A_32.png")
UP_MASK = imread(UI_DIR / "VMatrix.iconMask.3B_32.png")
RIGHT_MASK = cv2.flip(LEFT_MASK, 1)


class Mask(NamedTuple):
    directions = ["left", "right", "up"]
    left = np.where((LEFT_MASK[:, :, 3] == 0))

    right = np.where((RIGHT_MASK[:, :, 3] == 0))
    up = np.where((UP_MASK[:, :, 3] == 0))

    def masking(self, img):
        if not contains_alpha_channel(img):
            raise Exception("image does not have alpha channel.")

        left_masked = img.copy()
        left_masked[self.left] = (0, 0, 0, 0)

        right_masked = img.copy()
        right_masked[self.right] = (0, 0, 0, 0)

        up_masked = img.copy()
        up_masked[self.up] = (0, 0, 0, 0)

        return {"left": left_masked, "right": right_masked, "up": up_masked}


class VMatrixIconPath(NamedTuple):
    hexagon = UI_DIR / "VMatrix.SlotState.Equip_ENCore.png"
    frame = UI_DIR / "VMatrix.iconFrame.frame3.png"
    lock = UI_DIR / "VMatrix.ProtectLock.0.png"


class VMatrixIcon(NamedTuple):
    hexagon = Image.open(VMatrixIconPath.hexagon)
    frame = Image.open(VMatrixIconPath.frame)
    lock = Image.open(VMatrixIconPath.lock)
    blank = Image.new("RGBA", (32, 32), (0, 0, 0, 0))
    mask = Mask()

    @property
    def crop_lock(self):
        cropped_lock = self.lock.crop((0, 0, 13, 14))  # lock 15x17 -> 13x14
        return self.add_margin(cropped_lock, 32 - 14, 0, 0, 32 - 13, (0, 0, 0, 0))

    @property
    def background(self):
        left, top = self.align_center(self.hexagon, self.blank)
        return self.hexagon.crop((left, top, left + 32, top + 32))

    def add_margin(self, pil_img, top, right, bottom, left, color):
        width, height = pil_img.size

        new_width = width + right + left
        new_height = height + top + bottom

        result = Image.new(pil_img.mode, (new_width, new_height), color)
        result.paste(pil_img, (left, top), pil_img)

        return result

    def align_center(self, frame: Image, image: Image):
        diff = np.array(frame.size) - np.array(image.size)
        half_diff_int = np.int64(diff / 2)
        return tuple(half_diff_int)


class VMatrixImage:
    mask = Mask()
    icon = VMatrixIcon()

    def __init__(self, skill_icon_path: Path):
        self.path = skill_icon_path

    def create(self):
        self.create_masking_image()
        self.combinate()
        self.add_frame()
        self.add_lock()

        self.remove_masking_images()
        self.remove_comb_images()

    def remove(self):
        self.remove_masking_images()
        self.remove_comb_images()

    @property
    def skill_icons(self):
        return self.get_pngs(self.path)

    def get_pngs(self, directory):
        files = directory.iterdir()
        files = [f for f in files if f.suffix == ".png"]
        return files

    def create_masking_directory(self):
        for direction in self.mask.directions:
            subdir = self.path / direction
            subdir.mkdir(exist_ok=True)

    def create_combination_directory(self):
        subdir = self.path / "comb"
        subdir.mkdir(exist_ok=True)

    def create_masking_image(self):
        self.create_masking_directory()

        for skill_icon in self.skill_icons:
            img = imread(skill_icon)
            h, w, c = img.shape
            if w != 32 or h != 32 or c != 4:
                raise Exception(f"{skill_icon} is {img.shape}, not (32, 32, 4).")
            try:
                masked_dict = self.mask.masking(img)
            except ValueError as err:
                print(f"ValueError on {skill_icon.name}.")
                print(err)
            else:
                for direction, masked_img in masked_dict.items():
                    write(self.path / direction / skill_icon.name, masked_img)

    def combinate(self):
        self.create_combination_directory()

        for a, b, c in itertools.permutations(self.skill_icons, 3):
            left = imread(self.path / "left" / a.name)
            right = imread(self.path / "right" / b.name)
            up = imread(self.path / "up" / c.name)

            combination = left + right + up
            filename = f"{a.stem}+{b.stem}+{c.stem}.png"
            write(self.path / "comb" / filename, combination)

    def add_frame(self):
        files = self.composite("comb+frame", "comb")
        for file in files:
            img = Image.alpha_composite(Image.open(file), self.icon.frame)
            img_with_frame = Image.alpha_composite(self.icon.background, img)
            img_with_frame.save(self.path / "comb+frame" / file.name)

    def add_lock(self):
        files = self.composite("comb+frame+lock", "comb+frame")
        for file in files:
            img = Image.alpha_composite(Image.open(file), self.icon.crop_lock)
            img.save(self.path / "comb+frame+lock" / file.name)

    def composite(self, arg0, arg1):
        subdir = self.path / arg0
        subdir.mkdir(exist_ok=True)
        comb_dir = self.path / arg1
        return self.get_pngs(comb_dir)

    def remove_masking_images(self):
        for direction in self.mask.directions:
            subdir = self.path / direction
            if subdir.exists():
                for file in subdir.iterdir():
                    file.unlink()
                subdir.rmdir()

    def remove_comb_images(self):
        subdir = self.path / "comb"
        if subdir.exists():
            for file in subdir.iterdir():
                file.unlink()
            subdir.rmdir()


if __name__ == "__main__":
    # for one job/class
    path = SKILL_DIR / "Adele"
    vm = VMatrixImage(path)
    vm.create()

    # for all jobs/classes
    for dir in SKILL_DIR.iterdir():
        if not dir.is_dir():
            continue

        vm = VMatrixImage(dir)
        vm.create()
