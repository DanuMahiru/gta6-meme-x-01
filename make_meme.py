#!/usr/bin/env python3
"""Build the GTA 6 meme: a Leonida Police Department WANTED poster.

The make.fun ghost (real press-kit mark, mark-1024.png) is the suspect's
mugshot. Drawn entirely with PIL so every line is crisp at 480x480.
Original design: screened the top 12 entries first (invoice, library
overdue, parking citation, boarding pass, bank statement, receipt,
certificate, DMV test, lock screen, hurricane) and chose a document no
winner uses: a wanted poster.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
CREAM = (245, 238, 218)
BLACK = (20, 18, 20)
MAGENTA = (196, 28, 131)   # make.fun brand magenta
RED = (176, 0, 32)
GOLD = (232, 168, 0)

FONT_BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FONT_BOOK = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(size, bold=True):
    return ImageFont.truetype(FONT_BOLD if bold else FONT_BOOK, size)


def text_w(draw, s, f):
    return draw.textlength(s, font=f)


def center(draw, y, s, f, fill=BLACK):
    draw.text(((W - text_w(draw, s, f)) / 2, y), s, font=f, fill=fill)


def tracked(draw, y, s, f, fill=BLACK, tracking=0):
    """Draw text centered with extra letter spacing (tracking px)."""
    widths = [draw.textlength(ch, font=f) for ch in s]
    total = sum(widths) + tracking * (len(s) - 1)
    x = (W - total) / 2
    for ch, w in zip(s, widths):
        draw.text((x, y), ch, font=f, fill=fill)
        x += w + tracking


def star(draw, cx, cy, r_outer, r_inner, fill, outline=None, width=4):
    pts = []
    for i in range(10):
        r = r_outer if i % 2 == 0 else r_inner
        ang = math.pi / 2 + i * math.pi / 5
        pts.append((cx + r * math.cos(ang), cy - r * math.sin(ang)))
    draw.polygon(pts, fill=fill, outline=outline)
    if outline:
        draw.line(pts + [pts[0]], fill=outline, width=width, joint="curve")


img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

# --- frame ---
d.rectangle([18, 18, W - 19, H - 19], outline=BLACK, width=10)
d.rectangle([36, 36, W - 37, H - 37], outline=BLACK, width=3)

# --- authority line ---
tracked(d, 58, "LEONIDA POLICE DEPARTMENT", font(30), fill=BLACK, tracking=6)
center(d, 92, "VICE CITY DISTRICT  •  STATE OF LEONIDA", font(24, bold=False), fill=BLACK)

# --- WANTED ---
tracked(d, 128, "WANTED", font(150), fill=BLACK, tracking=18)

# --- 5 wanted stars (GTA wanted level) ---
star_y, star_r = 316, 34
gap = 86
x0 = (W - 4 * gap) / 2
for i in range(5):
    star(d, x0 + i * gap, star_y, star_r, star_r * 0.42, GOLD, outline=BLACK, width=4)

# --- mugshot: the real make.fun ghost mark ---
ghost = Image.open("assets/mark-1024.png").convert("RGBA").resize((300, 300), Image.LANCZOS)
gx = (W - 300) // 2
gy = 362
d.rectangle([gx - 10, gy - 10, gx + 310, gy + 310], outline=BLACK, width=6)
img.paste(ghost, (gx, gy), ghost)
d = ImageDraw.Draw(img)

# --- suspect name ---
center(d, 690, "GTA VI", font(88), fill=BLACK)

# --- details ---
center(d, 786, "LAST SEEN: 17 SEPT 2013", font(36), fill=BLACK)
center(d, 830, "CHARGE: 4,811 DAYS OF WAITING", font(36), fill=RED)

# --- divider ---
d.line([(90, 878), (W - 90, 878)], fill=BLACK, width=3)

# --- reward: the make.fun pitch ---
center(d, 892, "REWARD: $250 — PAID BY MY AI AGENT", font(36), fill=BLACK)
center(d, 932, "ON MAKE.FUN", font(40), fill=MAGENTA)

img.save("meme.png")
print("saved meme.png", img.size)
