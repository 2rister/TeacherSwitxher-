# -*- coding: utf-8 -*-
"""Portrait plates for the reading sheets:  python3 build/make_portraits.py

Downloads each source from Wikimedia Commons (cached under build/.cache), turns
it into a sepia "engraved plate" matching the poster style, and writes it to
materials/img. Sizing is set by the print: the frame is 40x50 mm, so 640x840 is
about 400 dpi there - past what any office printer resolves, and less than half
the weight of the 900x1180 plates used before.

Every source is free to use; the licence beside each entry was checked against
the Commons API and is reproduced on the answer key.
"""
import os, subprocess, sys, time
import numpy as np
from PIL import Image, ImageEnhance, ImageFilter, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(os.path.dirname(HERE), "materials", "img")
CACHE = os.path.join(HERE, ".cache")
UA = "TeacherSwitxher-EduMaterials/1.0 (classroom handouts)"
SIZE = (640, 840)
INK, PAPER = (38, 30, 24), (244, 234, 212)
# The plate sits inside a drawn frame on the sheet, so the soft edge is barely
# visible; flattening it onto the frame's own tone lets these ship as JPEG
# instead of RGBA PNG - about a tenth of the weight for the same printed result.
FRAME = (250, 243, 225)

#            file        source URL                                  crop (l,t,r,b as 0..1)      contrast bright
SOURCES = {
    "newton": ("https://upload.wikimedia.org/wikipedia/commons/f/f7/Portrait_of_Sir_Isaac_Newton%2C_1689_%28brightened%29.jpg",
               (0.06, 0.02, 0.94, 0.78), 1.28, 1.04, "Godfrey Kneller, 1689 - public domain"),
    "lennon": ("https://upload.wikimedia.org/wikipedia/commons/8/85/John_Lennon_1969_%28cropped%29.jpg",
               (0.02, 0.00, 0.98, 0.95), 1.30, 1.04, "Joost Evers / Anefo, 1969 - CC0 1.0"),
    "diana":  ("https://upload.wikimedia.org/wikipedia/commons/5/5e/Diana%2C_Princess_of_Wales_1997_%282%29.jpg",
               (0.04, 0.00, 0.96, 0.86), 1.32, 1.04, "John Mathew Smith, 1997 - CC BY-SA 2.0"),
    "darwin": ("https://upload.wikimedia.org/wikipedia/commons/2/2e/Charles_Darwin_seated_crop.jpg",
               (0.32, 0.02, 0.82, 0.52), 1.24, 1.04, "Maull & Fox, c. 1854 - public domain"),
    "nelson": ("https://upload.wikimedia.org/wikipedia/commons/7/72/HoratioNelson1.jpg",
               (0.02, 0.00, 0.98, 0.90), 1.22, 1.10, "Lemuel Francis Abbott, 1799 - public domain"),
}


def fetch(name, url):
    """Commons rate-limits full-size originals; back off, then fall back to the
    thumbnail service, which serves from a different host."""
    dst = os.path.join(CACHE, name + ".jpg")
    if os.path.exists(dst) and os.path.getsize(dst) > 50_000:
        return dst
    os.makedirs(CACHE, exist_ok=True)
    thumb = url.replace("/commons/", "/commons/thumb/", 1)
    thumb = f"{thumb}/1280px-{url.rsplit('/', 1)[1]}".replace("upload.wikimedia.org",
                                                              "thumb.wikimedia.org")
    for attempt, target in enumerate([url, url, thumb, thumb]):
        if attempt:
            time.sleep(15 * attempt)
        subprocess.run(["curl", "-sS", "--max-time", "180", "-A", UA, "-o", dst, target],
                       capture_output=True)
        if os.path.exists(dst) and open(dst, "rb").read(3) == b"\xff\xd8\xff":
            return dst
    raise SystemExit(f"could not download {name}: {url}")


def duotone(gray):
    a = np.asarray(gray, dtype=np.float32) / 255.0
    ramp = np.stack([INK[i] + (PAPER[i] - INK[i]) * a for i in range(3)], axis=-1)
    return Image.fromarray(np.clip(ramp, 0, 255).astype(np.uint8), "RGB")


def soft_edges(img, feather=0.16):
    """Fade the plate into the parchment at the bottom and sides."""
    w, h = img.size
    m = np.ones((h, w), dtype=np.float32)
    fb = int(h * 0.30)
    m[h - fb:, :] *= np.linspace(1, 0, fb)[:, None] ** 1.3
    fs = int(w * feather)
    m[:, :fs] *= np.linspace(0, 1, fs)[None, :]
    m[:, w - fs:] *= np.linspace(1, 0, fs)[None, :]
    ft = int(h * 0.06)
    m[:ft, :] *= np.linspace(0, 1, ft)[:, None]
    out = img.convert("RGBA")
    out.putalpha(Image.fromarray((m * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(4)))
    return out


def main():
    os.makedirs(IMG, exist_ok=True)
    for name, (url, crop, contrast, bright, credit) in SOURCES.items():
        src = fetch(name, url)
        im = Image.open(src).convert("RGB")
        w, h = im.size
        im = im.crop((int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h)))
        im = ImageOps.fit(im, SIZE, method=Image.LANCZOS, centering=(0.5, 0.35))
        g = ImageOps.grayscale(im)
        g = ImageOps.autocontrast(g, cutoff=1)
        g = ImageEnhance.Contrast(g).enhance(contrast)
        g = ImageEnhance.Brightness(g).enhance(bright)
        g = g.filter(ImageFilter.UnsharpMask(radius=2.0, percent=110, threshold=3))
        plate = soft_edges(duotone(g))
        flat = Image.new("RGB", plate.size, FRAME)
        flat.paste(plate, mask=plate.split()[3])
        dst = os.path.join(IMG, name + ".jpg")
        flat.save(dst, "JPEG", quality=88, optimize=True, progressive=True)
        print(f"  {name + '.jpg':<14} {SIZE[0]}x{SIZE[1]}  {os.path.getsize(dst) // 1024:>4} KB   {credit}")


if __name__ == "__main__":
    main()
