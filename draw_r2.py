#!/usr/bin/env python3
"""Draw the front page for THE WORLD - Saturday 21 November 2026.

Fresh design: masthead + 6-stat strip + 3 illustrated hero cards +
10-card story grid + dense ALSO ON list (25) + world-map strip and a
DATA CHECK box. 38 dated stories across 7 regions, 1024x1024 PNG.
"""
import math
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (246, 241, 227)
PAPER = (255, 253, 246)
NAVY = (22, 35, 63)
NAVY_LT = (52, 68, 104)
RED = (176, 39, 24)
GREY = (107, 107, 107)
LINE = (201, 194, 174)
GOLD = (184, 138, 44)

FD = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    try:
        return ImageFont.truetype(os.path.join(FD, name), size)
    except OSError:
        return ImageFont.load_default()


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines fitting max_w."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, x, y, fnt, fill, lh):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += lh
    return y


img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)
M = 28  # margin

# ---- top red bar ------------------------------------------------------
d.rectangle([0, 0, W, 6], fill=RED)

# ---- masthead ---------------------------------------------------------
d.text((W // 2, 14), "THE WORLD", font=SERIF_B(92), fill=NAVY, anchor="ma")
d.text((W // 2, 112), "S A T U R D A Y   2 1   N O V E M B E R   2 0 2 6",
       font=SANS_B(19), fill=RED, anchor="ma")
d.line([M, 140, W - M, 140], fill=NAVY, width=2)
d.line([M, 144, W - M, 144], fill=NAVY, width=1)
d.text((W // 2, 150), "38 DATED STORIES  •  7 REGIONS  •  ALL TIMES UTC",
       font=SANS_B(13), fill=GREY, anchor="ma")

# ---- stat strip -------------------------------------------------------
y0 = 176
stats = [
    ("M6.7", "PERU QUAKE"),
    ("3", "MISSILES DOWN"),
    ("200", "NATIONS AT COP31"),
    ("$7.25BN", "BAYER DEAL"),
    ("71", "STRIKES IN YEMEN"),
    ("2", "US BASES HIT"),
]
cw = (W - 2 * M) // 6
for i, (num, lab) in enumerate(stats):
    x = M + i * cw
    d.rectangle([x, y0, x + cw - 6, y0 + 52], outline=LINE, width=1)
    d.text((x + cw // 2 - 3, y0 + 5), num, font=SERIF_B(26), fill=RED,
           anchor="ma")
    for j, ln in enumerate(wrap(d, lab, SANS_B(10), cw - 16)):
        d.text((x + cw // 2 - 3, y0 + 34 + j * 11), ln, font=SANS_B(10),
               fill=NAVY, anchor="ma")

# ---- hero cards -------------------------------------------------------
heroes = [
    {
        "tag": "CLIMATE",
        "time": "23:41 UTC",
        "head": "COP31 RUNS INTO OVERTIME",
        "stand": "Antalya deadlocked over fossil fuels as the draft deal drops the words",
        "scene": "cop",
    },
    {
        "tag": "MIDDLE EAST",
        "time": "22:58 UTC",
        "head": "MISSILES OVER RIYADH",
        "stand": "Saudi defences down three Houthi ballistic missiles on a third night of alerts",
        "scene": "riyadh",
    },
    {
        "tag": "AMERICAS",
        "time": "00:09 UTC",
        "head": "QUAKE SHAKES THE ANDES",
        "stand": "Magnitude 6.7 strikes central Peru; Lima residents flee their homes",
        "scene": "peru",
    },
]
hy, hh = 240, 232
hw = (W - 2 * M - 16) // 3


def hero_scene(x, y, w, h, kind):
    d.rectangle([x, y, x + w, y + h], fill=(233, 228, 210))
    if kind == "cop":
        # globe with rays + conference hall silhouette
        cx, cy, r = x + w // 2, y + h // 2 - 14, 42
        for k in range(12):
            a = math.radians(k * 30)
            d.line([cx + int(r * 0.9 * math.cos(a)), cy + int(r * 0.9 * math.sin(a)),
                    cx + int((r + 12) * math.cos(a)), cy + int((r + 12) * math.sin(a))],
                   fill=GOLD, width=3)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=NAVY_LT)
        d.ellipse([cx - r + 10, cy - r + 8, cx - r + 28, cy - r + 24], fill=CREAM)
        d.arc([cx - r, cy - r, cx + r, cy + r], 200, 340, fill=CREAM, width=3)
        d.arc([cx - r, cy - r, cx + r, cy + r], 20, 160, fill=CREAM, width=3)
        for i, bh in enumerate([20, 30, 38, 30, 20]):
            bx = x + 18 + i * 52
            d.rectangle([bx, y + h - bh - 4, bx + 44, y + h - 4], fill=NAVY)
    elif kind == "riyadh":
        # skyline + interceptor trails
        for bx, bw, bh in [(0, 34, 62), (40, 26, 84), (72, 30, 56),
                           (108, 24, 96), (138, 30, 70), (174, 26, 88),
                           (206, 30, 60), (242, 28, 78), (274, 26, 52)]:
            d.rectangle([x + bx, y + h - bh - 6, x + bx + bw, y + h - 6], fill=NAVY)
        # tallest tower with arch top
        d.rectangle([x + 138, y + 18, x + 162, y + h - 6], fill=NAVY)
        d.pieslice([x + 138, y + 2, x + 162, y + 34], 180, 360, fill=NAVY)
        d.ellipse([x + 146, y + 14, x + 154, y + 26], fill=CREAM)
        for sx, sy, ex, ey in [(x + 30, y + 20, x + 90, y + 70),
                               (x + 280, y + 12, x + 210, y + 60),
                               (x + 150, y + 6, x + 150, y + 52)]:
            d.line([sx, sy, ex, ey], fill=RED, width=2)
            d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=RED)
        for sx, sy in [(x + 40, y + 30), (x + 250, y + 40), (x + 120, y + 24)]:
            d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=GOLD)
    else:  # peru
        # Andes triangles + seismograph zigzag
        d.polygon([(x, y + h - 6), (x + 70, y + 30), (x + 140, y + h - 6)], fill=NAVY_LT)
        d.polygon([(x + 100, y + h - 6), (x + 190, y + 12), (x + 280, y + h - 6)], fill=NAVY)
        d.polygon([(x + 60, y + 40), (x + 70, y + 30), (x + 80, y + 40)], fill=CREAM)
        d.polygon([(x + 178, y + 24), (x + 190, y + 12), (x + 202, y + 24)], fill=CREAM)
        pts = []
        for i in range(41):
            px = x + 8 + i * 7
            py = y + h - 46 + (14 if i % 4 == 0 else (-10 if i % 4 == 2 else 0))
            pts.append((px, py))
        d.line(pts, fill=RED, width=3)
        d.ellipse([x + w - 26, y + 12, x + w - 14, y + 24], fill=GOLD)


for i, hero in enumerate(heroes):
    x = M + i * (hw + 8)
    d.rectangle([x, hy, x + hw, hy + hh], fill=PAPER, outline=NAVY, width=1)
    hero_scene(x + 1, hy + 1, hw - 2, 120, hero["scene"])
    ty = hy + 128
    d.text((x + 10, ty), hero["tag"], font=SANS_B(10), fill=RED)
    d.text((x + hw - 10, ty), hero["time"], font=SANS(10), fill=GREY, anchor="ra")
    ty += 16
    ty = draw_lines(d, wrap(d, hero["head"], SERIF_B(19), hw - 20),
                    x + 10, ty, SERIF_B(19), NAVY, 21)
    ty += 2
    draw_lines(d, wrap(d, hero["stand"], SANS(12), hw - 20),
               x + 10, ty, SANS(12), (60, 60, 60), 15)

# ---- grid of 10 -------------------------------------------------------
grid = [
    ("MIDDLE EAST", "21:17", "Iran says it struck US bases in Bahrain"),
    ("EUROPE", "20:44", "Russian missiles fall in Poland; Warsaw calls it deliberate"),
    ("AMERICAS", "19:32", "FBI and US agriculture department hacked"),
    ("MARKETS", "18:05", "Bayer pays $7.25bn to settle Roundup cases"),
    ("ASIA-PACIFIC", "17:20", "Myanmar genocide ruling published by world court"),
    ("ASIA-PACIFIC", "16:48", "Banda Sea quake M6.6; no tsunami threat"),
    ("EUROPE", "15:12", "Zelensky agrees trilateral peace talks before Christmas"),
    ("WORLD", "14:37", "UN agrees talks to govern killer robots by 2028"),
    ("AFRICA", "13:58", "Hodeidah strikes put Sudan aid route at risk"),
    ("MARKETS", "12:26", "Stocks slide after Iran hits Bahrain bases"),
]
gy, gh = 480, 92
gw = (W - 2 * M - 32) // 5
for i, (tag, t, head) in enumerate(grid):
    r, c = divmod(i, 5)
    x = M + c * (gw + 8)
    y = gy + r * (gh + 6)
    d.rectangle([x, y, x + gw, y + gh], fill=PAPER, outline=LINE, width=1)
    d.text((x + 8, y + 7), tag, font=SANS_B(9), fill=RED)
    d.text((x + gw - 8, y + 7), t, font=SANS(9), fill=GREY, anchor="ra")
    draw_lines(d, wrap(d, head, SERIF_B(13), gw - 16), x + 8, y + 24,
               SERIF_B(13), NAVY, 16)

# ---- ALSO ON list -----------------------------------------------------
also = [
    ("Timor-Leste M6.8; no tsunami threat", "ASIA-PACIFIC", "11:54"),
    ("Houthi strike hits Riyadh's tallest tower", "MIDDLE EAST", "11:31"),
    ("Coalition orders civilians out of Hodeidah", "MIDDLE EAST", "11:08"),
    ("71 Saudi airstrikes across eight Yemeni provinces", "MIDDLE EAST", "10:47"),
    ("41 killed in Yemen strikes, Houthis say", "MIDDLE EAST", "10:22"),
    ("Two oil tankers struck near Oman", "MIDDLE EAST", "10:05"),
    ("King Charles thanks Turkey for hosting COP31", "CLIMATE", "09:41"),
    ("COP31 draft drops fossil-fuel language", "CLIMATE", "09:18"),
    ("US sent no official delegation to COP31", "CLIMATE", "08:56"),
    ("African leaders press for finance reform", "AFRICA", "08:33"),
    ("EU chair proposes budget cuts, digital tax", "EUROPE", "08:12"),
    ("Russian missile hits Kryvyi Rih; two killed", "EUROPE", "07:49"),
    ("US-Canada defence tensions grow", "AMERICAS", "07:26"),
    ("Major arrest in Mexico after cartel raid", "AMERICAS", "07:03"),
    ("AI-assisted maths breakthrough claimed", "MARKETS & TECH", "06:41"),
    ("Killer-robot talks agreed at the UN", "WORLD", "06:19"),
    ("Houthis claim hit on Saudi power plant", "MIDDLE EAST", "05:58"),
    ("Saudi shoots down five Houthi drones", "MIDDLE EAST", "05:37"),
    ("Peru quake 108 km deep; no deaths reported", "AMERICAS", "05:15"),
    ("Lima residents flee homes after tremor", "AMERICAS", "04:52"),
    ("Bayer deal ends years of Roundup litigation", "MARKETS", "04:31"),
    ("Roundup settlement lifts Bayer shares", "MARKETS", "04:09"),
    ("UN warns Hodeidah strikes endanger aid", "AFRICA", "03:48"),
    ("Myanmar case returns to the world court", "ASIA-PACIFIC", "03:26"),
    ("Climate finance splits nearly 200 nations", "CLIMATE", "03:04"),
]
ay = 678
d.text((M, ay), "ALSO ON", font=SERIF_B(16), fill=NAVY)
d.text((W - M, ay + 2), "25 MORE STORIES", font=SANS_B(10), fill=GREY, anchor="ra")
d.line([M, ay + 22, W - M, ay + 22], fill=NAVY, width=1)
col_w = (W - 2 * M - 24) // 2
row_h = 17
for i, (head, tag, t) in enumerate(also):
    col, row = divmod(i, 13)
    x = M + col * (col_w + 24)
    y = ay + 30 + row * row_h
    d.ellipse([x, y + 4, x + 5, y + 9], fill=RED)
    txt = head
    while d.textlength(txt, font=SANS(11)) > col_w - 92:
        txt = txt[:-1].rstrip()
    d.text((x + 10, y), txt, font=SANS(11), fill=(40, 40, 40))
    d.text((x + col_w - 4, y), tag + " " + t, font=SANS_B(9), fill=GREY, anchor="ra")

# ---- bottom band: map + data check ------------------------------------
by = 936
# stylised world map strip (left)
mx, mw, mh = M, 620, 70
d.rectangle([mx, by, mx + mw, by + mh], fill=(233, 228, 210), outline=LINE, width=1)
d.text((mx + 8, by + 4), "WHERE THE DAY HAPPENED", font=SANS_B(9), fill=GREY)
# rough continent blobs in a 0..100 x 0..62 grid, scaled into the strip
blobs = [
    [(4, 18), (10, 8), (18, 10), (22, 22), (16, 34), (8, 32)],          # N America
    [(20, 44), (26, 38), (30, 48), (26, 58), (20, 54)],                 # S America
    [(46, 14), (52, 8), (58, 12), (56, 20), (48, 22)],                  # Europe
    [(46, 26), (54, 24), (60, 30), (58, 44), (50, 46), (46, 36)],       # Africa
    [(60, 10), (72, 6), (86, 10), (92, 18), (84, 26), (70, 24)],        # Asia
    [(84, 52), (92, 50), (94, 58), (86, 60)],                           # Australia
]
for blob in blobs:
    pts = [(mx + 6 + px * 6.0, by + 14 + py * 0.8) for px, py in blob]
    d.polygon(pts, fill=NAVY_LT)
pins = [(14, 26), (24, 50), (52, 16), (56, 32), (50, 40), (66, 16),
        (80, 20), (88, 56), (70, 26), (30, 30), (58, 12), (20, 20)]
for px, py in pins:
    d.ellipse([mx + 6 + px * 6.0 - 3, by + 14 + py * 0.8 - 3,
               mx + 6 + px * 6.0 + 3, by + 14 + py * 0.8 + 3], fill=RED)
# data check (right)
dx = M + mw + 12
dw = W - M - dx
d.rectangle([dx, by, dx + dw, by + mh], outline=RED, width=2)
d.text((dx + 10, by + 6), "DATA CHECK", font=SANS_B(11), fill=RED)
facts = [
    "M6.7 — USGS, Carhuamayo, Peru, 00:09 UTC",
    "3 — missiles intercepted over Riyadh",
    "200 — nations at COP31, Antalya",
]
for i, f in enumerate(facts):
    d.text((dx + 10, by + 22 + i * 17), f, font=SANS(11), fill=(40, 40, 40))

# ---- footer -----------------------------------------------------------
d.text((W // 2, H - 12), "THE WORLD  •  SATURDAY 21 NOVEMBER 2026  •  38 STORIES  •  7 REGIONS",
       font=SANS_B(9), fill=GREY, anchor="ma")

out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out, "PNG")
print("saved", out, os.path.getsize(out), "bytes")
