#!/usr/bin/env python3
"""poidh #1552 'split the G your way' — original visual pun.

Concept: split a capital G down the middle and the left half IS a C.
Caption: "split the G, get a C." — music's favourite key change, taken literally.
All drawn with PIL; no stock imagery, no copied art.
"""
import math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1200, 675
BG = (13, 16, 38)          # deep ink navy
CREAM = (245, 233, 200)    # warm cream for the G
GOLD = (232, 184, 84)      # gold accents
MUTED = (168, 175, 205)    # soft grey-blue for small text

SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

random.seed(20261115)
img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# starfield
for _ in range(140):
    x, y = random.randint(0, W - 1), random.randint(0, H - 1)
    r = random.choice([1, 1, 1, 2])
    a = random.randint(40, 130)
    d.ellipse([x - r, y - r, x + r, y + r], fill=(a, a, min(255, a + 40)))

# faint staff lines across the middle band (music hint)
for i, y in enumerate(range(300, 420, 24)):
    d.line([(70, y), (W - 70, y)], fill=(28, 33, 66), width=2)

# --- render the G on its own layer, then split it ---
G_SIZE = 470
g_font = ImageFont.truetype(SERIF_BOLD, G_SIZE)
layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
ld = ImageDraw.Draw(layer)
bbox = ld.textbbox((0, 0), "G", font=g_font)
gw, gh = bbox[2] - bbox[0], bbox[3] - bbox[1]
gx = (W - gw) // 2 - bbox[0]
gy = 96 - bbox[1]
ld.text((gx, gy), "G", font=g_font, fill=CREAM + (255,))
# split point: vertical middle of the glyph
cut_x = gx + bbox[0] + gw // 2
top, bot = 96, 96 + gh

left = layer.crop((0, top, cut_x, bot))
right = layer.crop((cut_x, top, W, bot))
SHIFT = 58

# rebuild cleanly: paste halves with gap onto fresh composite
# (crop origins are layer coords: left crop origin x=0, right crop origin x=cut_x,
#  so the right half must be pasted at cut_x+SHIFT, not SHIFT)
comp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
comp.alpha_composite(left, (-SHIFT, 0))
comp.alpha_composite(right, (cut_x + SHIFT, 10))
# gold glow on the cut faces
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.line([(cut_x - SHIFT, top + 8), (cut_x - SHIFT, bot - 8)], fill=GOLD + (255,), width=5)
gd.line([(cut_x + SHIFT, top + 18), (cut_x + SHIFT, bot + 2)], fill=GOLD + (255,), width=5)
glow = glow.filter(ImageFilter.GaussianBlur(3))
comp.alpha_composite(glow)
img = Image.alpha_composite(img.convert("RGBA"), comp)
d = ImageDraw.Draw(img)

# a few gold sparks in the gap
for (sx, sy, sr) in [(cut_x - 6, 190, 5), (cut_x + 14, 330, 4), (cut_x - 16, 430, 3),
                     (cut_x + 4, 260, 3), (cut_x + 22, 470, 4)]:
    d.ellipse([sx - sr, sy - sr, sx + sr, sy + sr], fill=GOLD + (255,))

# floating music notes
note_font = ImageFont.truetype(SANS, 54)
for (nx, ny, ch) in [(150, 150, "\u266a"), (1010, 170, "\u266b"),
                      (180, 470, "\u266b"), (990, 460, "\u266a")]:
    d.text((nx, ny), ch, font=note_font, fill=(110, 118, 160, 255))

# labels under the halves (left half ink 382-541 centre ~461; right half 658-827 centre ~742)
lab_font = ImageFont.truetype(SERIF_BOLD, 64)
d.text((441, bot + 18), "C", font=lab_font, fill=GOLD + (255,))
small = ImageFont.truetype(SANS, 26)
rtxt = "…the rest"
rb = d.textbbox((0, 0), rtxt, font=small)
d.text((742 - (rb[2] - rb[0]) // 2, bot + 34), rtxt, font=small, fill=MUTED + (255,))

# caption
cap_font = ImageFont.truetype(SERIF_BOLD, 58)
cap = "split the G, get a C."
cb = d.textbbox((0, 0), cap, font=cap_font)
d.text(((W - (cb[2] - cb[0])) // 2, 556), cap, font=cap_font, fill=CREAM + (255,))
sub_font = ImageFont.truetype(SANS, 24)
sub = "music's favourite key change, taken literally"
sb = d.textbbox((0, 0), sub, font=sub_font)
d.text(((W - (sb[2] - sb[0])) // 2, 628), sub, font=sub_font, fill=MUTED + (255,))

img.convert("RGB").save("/home/hatch/workspace/taskmarket/poidh-1552/split-the-g.png")
print("saved split-the-g.png")
