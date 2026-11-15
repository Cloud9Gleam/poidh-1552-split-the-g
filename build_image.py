#!/usr/bin/env python3
"""poidh #1552 'split the G your way' — original artwork.

Concept: the letter G, unzipped — not cut. A heavy green G is split down
the middle by a zipper seam; the two halves are pulled apart and the
zipper teeth + pull tab show the mechanism. Rendered procedurally with
PIL (no stock imagery, no copied assets).
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1200, 1200
BG = (247, 242, 231)          # warm cream
GREEN = (30, 86, 49)          # deep green
GREEN_DARK = (18, 58, 32)
SILVER = (192, 196, 200)
SILVER_DARK = (120, 126, 132)
BRASS = (176, 141, 46)
BRASS_DARK = (120, 94, 28)
CAPTION = (90, 100, 92)

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img, "RGBA")

# --- render the G on its own layer -------------------------------------
g_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(g_layer)
font = ImageFont.truetype(FONT, 760)
# centre the G in the upper 2/3 (leave room for caption)
bbox = gd.textbbox((0, 0), "G", font=font)
gw, gh = bbox[2] - bbox[0], bbox[3] - bbox[1]
gx, gy = (W - gw) // 2 - bbox[0], 150 - bbox[1]
gd.text((gx, gy), "G", font=font, fill=GREEN + (255,))

# --- zigzag split line through the middle of the G ----------------------
# use the G's real rendered extent so teeth/slider hug the letter
gb = g_layer.getbbox()
cx = W // 2
AMP, WL = 16, 74
top, bottom = gb[1] + 6, gb[3] - 6


def split_x(y):
    """x of the zigzag seam at height y (triangle wave)."""
    ph = ((y - top) % WL) / WL
    tri = 1 - abs(2 * ph - 1)          # 0..1..0
    return cx + (tri * 2 - 1) * AMP


# left mask: polygon covering everything left of the seam, traced in order
# around the region: top-left -> down the zigzag -> bottom-left -> close
pts = [(0, 0)]
for y in range(top, bottom + 1, 6):
    pts.append((split_x(y), y))
pts += [(0, H), (0, 0)]
left_mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(left_mask).polygon(pts, fill=255)
right_mask = Image.new("L", (W, H), 255)
right_mask.paste(Image.new("L", (W, H), 0), (0, 0), left_mask)

SHIFT = 42
left = Image.new("RGBA", (W, H), (0, 0, 0, 0))
left.paste(g_layer, (-SHIFT, 0), left_mask)
right = Image.new("RGBA", (W, H), (0, 0, 0, 0))
right.paste(g_layer, (SHIFT, 0), right_mask)
img.paste(Image.alpha_composite(left, right), (0, 0), Image.alpha_composite(left, right))

d = ImageDraw.Draw(img, "RGBA")

# --- zipper teeth along both cut edges ----------------------------------
TOOTH_W, TOOTH_H, STEP = 22, 15, 30
y = top + 8
i = 0
while y < bottom - 10:
    sx = split_x(y)
    # left-half teeth (pointing right, into the gap)
    d.rounded_rectangle([sx - SHIFT - TOOTH_W, y, sx - SHIFT + 2, y + TOOTH_H],
                        radius=3, fill=SILVER, outline=SILVER_DARK, width=1)
    # right-half teeth, half-step offset (pointing left)
    y2 = y + STEP // 2
    if y2 < bottom - 10:
        sx2 = split_x(y2)
        d.rounded_rectangle([sx2 + SHIFT - 2, y2, sx2 + SHIFT + TOOTH_W, y2 + TOOTH_H],
                            radius=3, fill=SILVER, outline=SILVER_DARK, width=1)
    y += STEP
    i += 1

# --- zipper slider + pull tab at the bottom of the seam ------------------
sx_b = split_x(bottom - 6)
slider_y = bottom - 34
# slider body (small trapezoid)
d.polygon([(sx_b - 26, slider_y), (sx_b + 26, slider_y),
           (sx_b + 18, slider_y + 46), (sx_b - 18, slider_y + 46)],
          fill=BRASS, outline=BRASS_DARK)
# pull tab hanging below the slider
tab_y0 = slider_y + 46
d.rounded_rectangle([sx_b - 16, tab_y0, sx_b + 16, tab_y0 + 92],
                    radius=14, fill=BRASS, outline=BRASS_DARK, width=2)
d.ellipse([sx_b - 8, tab_y0 + 62, sx_b + 8, tab_y0 + 78],
          outline=BRASS_DARK, width=3)
# connector ring between slider and tab
d.ellipse([sx_b - 10, tab_y0 - 8, sx_b + 10, tab_y0 + 10],
          outline=BRASS_DARK, width=3)

# --- caption -------------------------------------------------------------
cap_font = ImageFont.truetype(FONT, 44)
cap = "split the G \u2014 unzipped, not cut."
cb = d.textbbox((0, 0), cap, font=cap_font)
d.text(((W - (cb[2] - cb[0])) // 2, 1105), cap, font=cap_font, fill=CAPTION)

img.save("split-the-g.png")
print("saved split-the-g.png", img.size)
