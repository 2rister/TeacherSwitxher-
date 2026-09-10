"""Widen the 3:2 reference to the deck's 16:9 without cropping anything.

The left and right edges are dark painted border, so they can be continued by
mirroring a slice outwards and softening it - nothing of the artwork is lost,
which cropping to 16:9 would not manage (it would eat Shakespeare and the
Thames panorama).
"""
import numpy as np
from PIL import Image, ImageFilter

SRC, DST = "reference.png", "board_bg.png"
im = Image.open(SRC).convert("RGB")
# Nothing is cropped: taking 50 px off the bottom to shrink the side bands ate
# into the "Knowledge - History - Inspiration" scroll, which sits lower than it
# looks. Wider bands are the cheaper price.
W, H = im.size
TARGET_W = int(round(H * 16 / 9))          # 1820
pad = (TARGET_W - W) // 2
print(f"{W}x{H} -> {TARGET_W}x{H}   поля по {pad} px")

# Stretch a THIN edge strip rather than mirroring a wide slice: a 90 px mirror
# duplicated recognisable content - Diana's face reappeared on the right, a torn
# note on the left. A few pixels smeared out reads as the frame falling into
# shadow and carries no shapes to recognise.
SLICE = 5
left = im.crop((0, 0, SLICE, H)).resize((pad, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(22))
right = im.crop((W - SLICE, 0, W, H)).resize((pad, H), Image.LANCZOS).filter(ImageFilter.GaussianBlur(22))

out = Image.new("RGB", (TARGET_W, H))
out.paste(left, (0, 0)); out.paste(im, (pad, 0)); out.paste(right, (pad + W, 0))

# darken the added strips slightly so they read as the frame receding, not a seam
a = np.asarray(out, np.float32)
for x0, x1, flip in ((0, pad, True), (pad + W, TARGET_W, False)):
    t = np.linspace(0, 1, x1 - x0)
    if flip: t = t[::-1]
    a[:, x0:x1] *= (0.40 + 0.60 * (1 - t))[None, :, None]
out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))

out = out.resize((2000, int(2000 * H / TARGET_W)), Image.LANCZOS)
out.save(DST, "PNG", optimize=True)
print(f"{DST}: {out.size}, {__import__('os').path.getsize(DST)//1024} KB")

# geometry of the painted plaques, in slide inches
SLIDE_W, SLIDE_H = 13.3333, 7.5
COLS = [(305, 471), (501, 666), (694, 855), (884, 1039), (1075, 1234)]
ROW_TOP0, ROW_STEP, ROW_H = 399.0, 55.43, 48.0   # measured on the uncropped art
kx, ky = SLIDE_W / TARGET_W, SLIDE_H / H
grid = []
for ci, (x0, x1) in enumerate(COLS):
    for ri in range(8):
        y0 = ROW_TOP0 + ROW_STEP * ri
        grid.append(dict(col=ci, row=ri,
                         left=(x0 + pad) * kx, top=y0 * ky,
                         width=(x1 - x0) * kx, height=ROW_H * ky))
import json
with open("board_grid.json", "w") as fh:
    json.dump(grid, fh)
print(f"сетка: {len(grid)} плиток")
g = grid[0]; print(f"  первая: {g['left']:.3f}, {g['top']:.3f}  {g['width']:.3f}x{g['height']:.3f} in")
g = grid[-1]; print(f"  последняя: {g['left']:.3f}, {g['top']:.3f}  {g['width']:.3f}x{g['height']:.3f} in")
