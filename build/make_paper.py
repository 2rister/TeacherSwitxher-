# -*- coding: utf-8 -*-
"""Bake the parchment ground into one JPEG:  python3 build/make_paper.py

The look used to be built live in CSS — two radial gradients, a linear wash, a
feTurbulence noise layer in multiply blend, and an inset vignette. Chromium
cannot keep any of that as vector, so it rasterised the full page at print
resolution and embedded the result once per page: ~1 MB a page, 12 MB for the
pack. One shared JPEG is embedded once for the whole document instead.
"""
import os
import numpy as np
from PIL import Image, ImageFilter

DPI = 150                                   # ample for a smooth ground with fine tooth
W, H = int(8.27 * DPI), int(11.69 * DPI)    # A4
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   "materials", "img", "paper.jpg")

y, x = np.mgrid[0:H, 0:W].astype(np.float32)
u, v = x / W, y / H


def ellipse(cx, cy, r):
    """Normalised distance from a centre, matching a CSS radial-gradient ramp."""
    d = np.sqrt(((u - cx) * (W / H)) ** 2 + (v - cy) ** 2) / r
    return np.clip(1.0 - d, 0.0, 1.0)


# linear-gradient(155deg, #f3e8d0, #e7d8b6 55%, #d9c69c)
# CSS measures 155deg clockwise from "to top", and normalises progress over the
# projected gradient-line length — not over the raw diagonal, which is longer and
# would flatten most of the page onto the darkest stop.
A = np.deg2rad(155.0)
dx, dy = np.sin(A), -np.cos(A)
Lg = abs(W * dx) + abs(H * dy)
t = np.clip(((x - W / 2) * dx + (y - H / 2) * dy) / Lg + 0.5, 0, 1)
stops = [(0.00, (0xF3, 0xE8, 0xD0)), (0.55, (0xE7, 0xD8, 0xB6)), (1.00, (0xD9, 0xC6, 0x9C))]
base = np.zeros((H, W, 3), np.float32)
for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
    m = (t >= t0) & (t <= t1)
    k = ((t - t0) / (t1 - t0))[m][:, None]
    base[m] = np.array(c0, np.float32) + (np.array(c1, np.float32) - np.array(c0, np.float32)) * k

# highlight top-left, warm shade bottom-right
base += (np.array([255, 252, 240], np.float32) - base) * (ellipse(0.18, 0.12, 0.62) * 0.85)[..., None]
base += (np.array([160, 132, 86], np.float32) - base) * (ellipse(0.82, 0.88, 0.65) * 0.20)[..., None]

# Paper tooth. Centred on 1.0 so the grain does not also darken the sheet, and
# kept fine — at 150 dpi an unblurred field reads as sandpaper, not laid paper.
rng = np.random.default_rng(20260909)
tooth = rng.normal(0.0, 1.0, (H, W)).astype(np.float32)
tooth = np.asarray(Image.fromarray(((tooth * 0.5 + 0.5) * 255).clip(0, 255).astype(np.uint8))
                   .filter(ImageFilter.GaussianBlur(0.9)), np.float32) / 255.0
base *= (1.0 + 0.085 * (tooth - 0.5) * 2.0)[..., None]

# inset plate vignette, previously an inset box-shadow
edge = np.minimum.reduce([u, 1 - u, v * (H / W), (1 - v) * (H / W)])
base *= (1.0 - 0.17 * np.clip(1.0 - edge / 0.115, 0, 1) ** 1.9)[..., None]

Image.fromarray(base.clip(0, 255).astype(np.uint8), "RGB").save(
    OUT, "JPEG", quality=84, optimize=True, progressive=True, dpi=(DPI, DPI))
print(f"{OUT}  {W}x{H}  {os.path.getsize(OUT)//1024} KB")
