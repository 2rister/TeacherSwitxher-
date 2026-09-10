# -*- coding: utf-8 -*-
"""Small portraits for the grammar sheets:  python3 build/make_thumbs.py

The grammar sheets show the portrait at 16x20 mm. Embedding the full 900x1180
plate for that is ~570 dpi of detail nobody can see, and it made a one-page
grammar sheet weigh 2 MB. These thumbnails are 480x600 (about 380 dpi at print
size, still well past what a printer resolves) and flattened onto the parchment
tone, since the frame hides the soft edges the full plates carry.
"""
import os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(os.path.dirname(HERE), "materials", "img")
PAPER = (243, 232, 208)          # --paper, so the flattened edge disappears into the frame
SIZE = (480, 600)

for name in ("newton", "lennon", "diana"):
    src = os.path.join(IMG, f"{name}.png")
    im = Image.open(src).convert("RGBA")
    flat = Image.new("RGB", im.size, PAPER)
    flat.paste(im, mask=im.split()[3])
    flat = flat.resize(SIZE, Image.LANCZOS)
    dst = os.path.join(IMG, f"{name}-thumb.jpg")
    flat.save(dst, "JPEG", quality=86, optimize=True, progressive=True)
    print(f"  {os.path.basename(dst):<20} {SIZE[0]}x{SIZE[1]}  "
          f"{os.path.getsize(dst) // 1024} KB   (was {os.path.getsize(src) // 1024} KB)")
