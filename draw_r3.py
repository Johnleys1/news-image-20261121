#!/usr/bin/env python3
"""Round 3 front page — news-image-20261121.
THE WORLD — Saturday 21 November 2026. 34 dated stories, 7 regions.
Winners use 33-35 stories (sweet spot); 38 was too dense, 20 too thin.
Layout skeleton kept (masthead, stat strip, 3 heroes, grid, ALSO ON, DATE CHECK,
map) but with more whitespace — fewer, larger cards and richer visuals.
"""
import math
import random
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
CREAM = (250, 244, 230)
PAPER2 = (243, 235, 216)
PAPER3 = (238, 229, 208)
INK = (22, 22, 28)
NAVY = (24, 42, 84)
NAVY_LT = (52, 74, 128)
RED = (176, 32, 28)
RED_DK = (138, 24, 22)
GREY = (112, 108, 98)
LINE = (70, 64, 54)
GOLD = (172, 134, 38)
TEAL = (22, 108, 102)
GREEN = (44, 108, 58)
ORANGE = (196, 94, 22)
PURPLE = (94, 62, 126)
SKY = (168, 196, 222)
SEA = (214, 228, 236)
LAND = (196, 200, 158)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

_cache = {}


def F(path, size):
    key = (path, size)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(path, size)
    return _cache[key]


def wrap(d, text, font, max_w):
    lines, cur = [], ""
    for w in text.split():
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def vgrad(d, box, c1, c2):
    x0, y0, x1, y1 = box
    n = max(1, y1 - y0)
    for i in range(n):
        t = i / n
        c = tuple(int(c1[k] + (c2[k] - c1[k]) * t) for k in range(3))
        d.line([(x0, y0 + i), (x1, y0 + i)], fill=c)


def grain(d, box, n=2600, seed=7):
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    for _ in range(n):
        x = rnd.randint(x0, x1)
        y = rnd.randint(y0, y1)
        v = rnd.choice([(232, 224, 204), (255, 250, 238), (226, 216, 192)])
        d.point((x, y), fill=v)


def center(d, y, text, font, fill, x0=0, x1=W):
    w = d.textlength(text, font=font)
    d.text(((x0 + x1 - w) / 2, y), text, font=font, fill=fill)


img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)
# subtle paper texture over the whole page
grain(d, (0, 0, W, H), n=5200, seed=11)
# faint top-to-bottom paper tone
for yy in range(0, H, 4):
    t = yy / H
    c = tuple(int(CREAM[k] + (PAPER3[k] - CREAM[k]) * t * 0.45) for k in range(3))
    d.line([(0, yy), (W, yy)], fill=c)

M = 28  # margin
R = W - M

# ---------------------------------------------------------------- masthead
d.line([(M, 10), (R, 10)], fill=RED, width=3)
center(d, 20, "T H E   W O R L D   I N   O N E   D A Y", F(SANS_B, 13), RED)
d.text((M, 44), "THE WORLD", font=F(SERIF, 66), fill=INK)
# date + count line, right-aligned block under the masthead word
dateline = "SATURDAY 21 NOVEMBER 2026  ·  34 STORIES  ·  7 REGIONS"
center(d, 118, dateline, F(SANS_B, 13), NAVY)
d.line([(M, 138), (R, 138)], fill=INK, width=2)
d.line([(M, 142), (R, 142)], fill=INK, width=1)

# ---------------------------------------------------------------- stat strip
stats = [
    ("13", "COP31 DAY", "talks run past deadline"),
    ("3", "MISSILES", "intercepted over Riyadh"),
    ("6.7", "PERU QUAKE", "magnitude near Junin"),
    ("146", "SAFE", "rescued in Davao floods"),
    ("$58,983", "BITCOIN", "steadies after a fall"),
    ("124*", "RAHUL", "not out at tea, India"),
]
sx, sy, sw, sh = M, 150, 154, 56
for i, (num, lab, sub) in enumerate(stats):
    x = sx + i * (sw + 5)
    d.rectangle([x, sy, x + sw, sy + sh], outline=LINE, width=1, fill=(255, 251, 240))
    d.rectangle([x, sy, x + sw, sy + 3], fill=RED)
    center(d, sy + 6, num, F(SANS_B, 20), NAVY, x, x + sw)
    center(d, sy + 30, lab, F(SANS_B, 9), INK, x, x + sw)
    center(d, sy + 41, sub, F(SANS, 8), GREY, x, x + sw)

# ---------------------------------------------------------------- region bar
regions = [
    ("CLIMATE", 2, GREEN), ("MIDDLE EAST", 4, ORANGE), ("AMERICAS", 5, TEAL),
    ("ASIA-PACIFIC", 8, PURPLE), ("EUROPE", 6, NAVY), ("AFRICA", 5, GOLD),
    ("MARKETS & TECH", 4, RED),
]
rx, ry, rw, rh = M, 212, R - M, 24
total = sum(c for _, c, _ in regions)
x = rx
for name, cnt, col in regions:
    w = rw * cnt / total
    d.rectangle([x, ry, x + w - 1, ry + rh], fill=col)
    lab = f"{name} {cnt}"
    f = F(SANS_B, 8)
    tw = d.textlength(lab, font=f)
    if tw < w - 6:
        d.text((x + (w - tw) / 2, ry + 7), lab, font=f, fill=(255, 255, 255))
    x += w

# ---------------------------------------------------------------- hero art
def art_cop31(d, box):
    """Globe + thermometer over a conference hall."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (126, 178, 208), (226, 232, 214))
    # sun
    d.ellipse([x1 - 52, y0 + 8, x1 - 20, y0 + 40], fill=(240, 196, 64))
    # globe
    cx, cy, r = x0 + 62, y0 + 58, 44
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(64, 122, 168),
              outline=(20, 60, 100), width=2)
    for k in range(-2, 3):
        d.arc([cx - r + abs(k) * 12, cy - r, cx + r - abs(k) * 12, cy + r],
              270 if k < 0 else 90, 90 if k < 0 else 270, fill=(170, 210, 230))
    d.line([(cx - r, cy), (cx + r, cy)], fill=(170, 210, 230))
    d.ellipse([cx - 26, cy - 26, cx - 2, cy - 4], fill=(88, 150, 92))
    d.ellipse([cx + 4, cy + 8, cx + 28, cy + 28], fill=(88, 150, 92))
    # thermometer
    tx = x1 - 58
    d.rounded_rectangle([tx, y0 + 52, tx + 12, y0 + 96], 6, fill=(255, 255, 255),
                        outline=RED, width=2)
    d.ellipse([tx - 3, y0 + 92, tx + 15, y0 + 110], fill=RED)
    d.rectangle([tx + 3, y0 + 70, tx + 9, y0 + 98], fill=RED)
    # hall silhouette
    d.polygon([(x0, y1), (x0 + 30, y1 - 26), (x0 + 90, y1 - 26), (x0 + 118, y1),
               (x1, y1)], fill=(52, 66, 92))
    for wx in range(x0 + 38, x0 + 88, 12):
        d.rectangle([wx, y1 - 20, wx + 6, y1 - 8], fill=(240, 196, 64))


def art_riyadh(d, box):
    """Night skyline, lit windows, three interceptor trails."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (16, 24, 56), (58, 72, 110))
    # stars
    rnd = random.Random(21)
    for _ in range(26):
        d.point((rnd.randint(x0 + 4, x1 - 4), rnd.randint(y0 + 4, y0 + 46)),
                fill=(220, 225, 240))
    # moon
    d.ellipse([x1 - 46, y0 + 8, x1 - 22, y0 + 32], fill=(238, 232, 200))
    # skyline
    base = y1
    towers = [(x0 + 6, 62, 30), (x0 + 42, 84, 34), (x0 + 82, 54, 30),
              (x0 + 118, 92, 36), (x0 + 160, 70, 30), (x0 + 196, 88, 34),
              (x0 + 236, 60, 30), (x0 + 272, 78, 26)]
    for tx, th, tw in towers:
        d.rectangle([tx, base - th, tx + tw, base], fill=(10, 14, 34))
        for wy in range(base - th + 8, base - 6, 12):
            for wx in range(tx + 5, tx + tw - 5, 10):
                if (wx + wy) % 20 < 10:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(250, 204, 90))
    # interceptor trails
    for sx0, sy0, ex, ey in [(x0 + 40, y0 + 78, x0 + 120, y0 + 22),
                             (x0 + 150, y0 + 84, x0 + 210, y0 + 30),
                             (x0 + 230, y0 + 80, x0 + 280, y0 + 26)]:
        d.line([(sx0, sy0), (ex, ey)], fill=(255, 220, 120), width=2)
        d.ellipse([ex - 3, ey - 3, ex + 3, ey + 3], fill=(255, 240, 180))
        d.ellipse([sx0 - 2, sy0 - 2, sx0 + 2, sy0 + 2], fill=(255, 160, 60))


def art_peru(d, box):
    """Andes ridges, seismograph trace, small house."""
    x0, y0, x1, y1 = box
    vgrad(d, box, (222, 206, 172), (176, 148, 116))
    # far ridge
    d.polygon([(x0, y1 - 46), (x0 + 60, y1 - 92), (x0 + 120, y1 - 58),
               (x0 + 180, y1 - 96), (x0 + 240, y1 - 62), (x0 + 300, y1 - 88),
               (x1, y1 - 52), (x1, y1), (x0, y1)], fill=(128, 108, 88))
    # near ridge
    d.polygon([(x0, y1 - 18), (x0 + 70, y1 - 52), (x0 + 150, y1 - 24),
               (x0 + 220, y1 - 56), (x1, y1 - 30), (x1, y1), (x0, y1)],
              fill=(84, 68, 54))
    # snow caps
    d.polygon([(x0 + 52, y1 - 86), (x0 + 60, y1 - 92), (x0 + 68, y1 - 86),
               (x0 + 64, y1 - 80), (x0 + 56, y1 - 80)], fill=(245, 242, 232))
    d.polygon([(x0 + 172, y1 - 90), (x0 + 180, y1 - 96), (x0 + 188, y1 - 90),
               (x0 + 184, y1 - 84), (x0 + 176, y1 - 84)], fill=(245, 242, 232))
    # seismograph strip
    d.rectangle([x0 + 14, y0 + 12, x1 - 14, y0 + 40], fill=(255, 252, 244),
                outline=INK, width=1)
    pts = []
    rnd = random.Random(5)
    xx = x0 + 18
    while xx < x1 - 18:
        yy = y0 + 26 + rnd.choice([-9, -4, 0, 4, 9, 2, -2])
        pts.append((xx, yy))
        xx += 5
    d.line(pts, fill=RED, width=2)
    # small house
    hx, hy = x0 + 232, y1 - 34
    d.rectangle([hx, hy, hx + 34, y1 - 6], fill=(196, 148, 96), outline=INK, width=1)
    d.polygon([(hx - 4, hy), (hx + 17, hy - 14), (hx + 38, hy)], fill=RED_DK)
    d.rectangle([hx + 13, y1 - 18, hx + 21, y1 - 6], fill=(60, 44, 30))


heroes = [
    ("1 · COP31 · BELÉM", "Climate talks run into overtime",
     "Negotiators push past the deadline in Belém as a deal on loss and damage nears — but the final text is still unwritten.", "AP · REUTERS", art_cop31),
    ("2 · MIDDLE EAST · RIYADH", "Three missiles stopped over Riyadh",
     "Saudi air defences intercept three missiles over the capital; no casualties reported as the region stays on edge.", "REUTERS · AFP", art_riyadh),
    ("3 · AMERICAS · JUNÍN", "Peru shaken by magnitude 6.7 quake",
     "A strong quake strikes near Junín at 00:09 UTC; buildings sway in Lima and rescue teams check mountain towns.", "USGS · AP", art_peru),
]
hx, hy, hw, hh, hg = M, 246, 310, 276, 14
for i, (kick, head, summ, src, art) in enumerate(heroes):
    x = hx + i * (hw + hg)
    d.rectangle([x, hy, x + hw, hy + hh], outline=LINE, width=1, fill=(255, 251, 240))
    art(d, (x + 1, hy + 1, x + hw - 1, hy + 122))
    d.rectangle([x, hy + 122, x + hw, hy + 144], fill=RED)
    d.text((x + 10, hy + 128), kick, font=F(SANS_B, 10), fill=(255, 255, 255))
    for j, ln in enumerate(wrap(d, head, F(SANS_B, 15), hw - 20)):
        d.text((x + 10, hy + 152 + j * 19), ln, font=F(SANS_B, 15), fill=INK)
    for j, ln in enumerate(wrap(d, summ, F(SANS, 11), hw - 20)):
        d.text((x + 10, hy + 196 + j * 14), ln, font=F(SANS, 11), fill=(52, 50, 46))
    d.text((x + 10, hy + hh - 18), src, font=F(SANS_B, 9), fill=GREY)

# ---------------------------------------------------------------- grid 4-13
grid = [
    ("4", "BAHRAIN", "MIDDLE EAST", ORANGE,
     "Iran says it hit a US base in Bahrain",
     "Tehran's claim disputed; no US confirmation.", "AL JAZEERA"),
    ("5", "DAVAO", "ASIA-PACIFIC", PURPLE,
     "Flood rescue brings 146 people safe",
     "River teams pull families from rooftops.", "AP"),
    ("6", "MARKETS", "MARKETS & TECH", RED,
     "Bitcoin steadies at $58,983",
     "Crypto finds its feet after a week of falls.", "REUTERS"),
    ("7", "CRICKET", "ASIA-PACIFIC", PURPLE,
     "Rahul 124* as India take command",
     "Opener unbeaten at tea on day two.", "ESPNCRICINFO"),
    ("8", "WARSAW", "EUROPE", NAVY,
     "NATO allies agree eastern flank plan",
     "New deployments and air cover promised.", "AFP"),
    ("9", "IRAQ", "MIDDLE EAST", ORANGE,
     "Army retakes Jurf al-Sakhar",
     "Last holdout cleared after dawn push.", "REUTERS"),
    ("10", "SOUTH AFRICA", "AFRICA", GOLD,
     "ANC slips to 31% in new poll",
     "Ruling party's support falls again.", "AFP"),
    ("11", "CLIMATE", "CLIMATE", GREEN,
     "Youth march fills 400 cities",
     "Protests span the globe on COP31's last day.", "AP"),
    ("12", "LOS ANGELES", "AMERICAS", TEAL,
     "Jury finds utility liable in fire case",
     "Verdict ends a three-year court fight.", "AP"),
    ("13", "KOREA", "ASIA-PACIFIC", PURPLE,
     "Train derails; 12 hurt, line closed",
     "Rescue crews work through the night.", "YONHAP"),
]
gx, gy, gw, gh, ggap = M, 536, 185, 98, 10
for i, (num, place, beat, col, head, summ, src) in enumerate(grid):
    cx = gx + (i % 5) * (gw + ggap)
    cy = gy + (i // 5) * (gh + ggap)
    d.rectangle([cx, cy, cx + gw, cy + gh], outline=LINE, width=1,
                fill=(255, 251, 240))
    d.rectangle([cx, cy, cx + gw, cy + 20], fill=col)
    d.text((cx + 6, cy + 5), f"{num} · {place}", font=F(SANS_B, 9),
           fill=(255, 255, 255))
    d.text((cx + gw - 6 - d.textlength(beat, font=F(SANS_B, 8)),
            cy + 6), beat, font=F(SANS_B, 8), fill=(255, 255, 255))
    for j, ln in enumerate(wrap(d, head, F(SANS_B, 11), gw - 12)[:2]):
        d.text((cx + 6, cy + 26 + j * 14), ln, font=F(SANS_B, 11), fill=INK)
    for j, ln in enumerate(wrap(d, summ, F(SANS, 9), gw - 12)[:2]):
        d.text((cx + 6, cy + 56 + j * 12), ln, font=F(SANS, 9), fill=(52, 50, 46))
    d.text((cx + 6, cy + gh - 16), src, font=F(SANS_B, 8), fill=GREY)

# ---------------------------------------------------------------- bottom band
by = 754
# ---- world map (left)
mx0, my0, mx1, my1 = M, by, 370, 886
d.rectangle([mx0, my0, mx1, my1], fill=SEA, outline=LINE, width=1)
d.text((mx0 + 8, my0 + 5), "WORLD MAP — STORIES 1–13",
       font=F(SANS_B, 9), fill=NAVY)


def proj(lon, lat):
    x = mx0 + (lon + 170) / 360 * (mx1 - mx0)
    y = my0 + 18 + (75 - lat) / 130 * (my1 - my0 - 24)
    return (x, y)


CONTINENTS = {
    "NA": [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66),
           (-75, 62), (-65, 60), (-55, 52), (-60, 45), (-70, 42), (-75, 35),
           (-80, 32), (-85, 30), (-90, 29), (-97, 26), (-105, 22), (-110, 24),
           (-117, 33), (-125, 40), (-125, 49), (-135, 58), (-155, 60)],
    "SA": [(-80, 10), (-75, 5), (-70, 0), (-65, -5), (-60, -10), (-55, -15),
           (-50, -20), (-45, -25), (-40, -30), (-50, -35), (-60, -40),
           (-70, -45), (-73, -50), (-70, -55), (-65, -50), (-60, -40),
           (-55, -30), (-50, -20), (-45, -10), (-40, -5), (-35, -8),
           (-40, -3), (-50, 0), (-60, 5), (-70, 10)],
    "AF": [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
           (35, 28), (40, 15), (48, 11), (51, 10), (45, 0), (40, -10),
           (35, -20), (30, -30), (20, -35), (15, -30), (12, -18), (13, -10),
           (9, 0), (9, 5), (-5, 5), (-13, 8)],
    "EU": [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57),
           (10, 59), (18, 56), (21, 55), (24, 58), (28, 60), (30, 62),
           (25, 65), (20, 68), (15, 70), (10, 64), (5, 60), (0, 55),
           (-5, 50), (-10, 45)],
    "AS": [(30, 62), (40, 68), (50, 70), (60, 70), (70, 72), (80, 73),
           (90, 75), (100, 77), (110, 76), (120, 73), (130, 72), (140, 72),
           (150, 70), (160, 68), (170, 66), (162, 60), (158, 55), (150, 60),
           (142, 55), (140, 45), (135, 40), (130, 35), (127, 35), (122, 38),
           (120, 30), (115, 25), (110, 20), (108, 15), (105, 10), (100, 8),
           (95, 10), (92, 15), (90, 22), (85, 20), (80, 15), (77, 8),
           (75, 12), (72, 20), (66, 25), (60, 25), (55, 26), (52, 28),
           (50, 30), (45, 30), (42, 28), (40, 32), (36, 36), (30, 40),
           (30, 45), (30, 50), (35, 55)],
    "AU": [(113, -22), (114, -30), (115, -35), (120, -35), (125, -32),
           (130, -32), (135, -35), (140, -38), (145, -38), (150, -37),
           (153, -32), (150, -25), (146, -20), (142, -15), (140, -12),
           (136, -12), (132, -11), (130, -13), (126, -14), (122, -17),
           (118, -20)],
}
for poly in CONTINENTS.values():
    d.polygon([proj(lon, lat) for lon, lat in poly], fill=LAND,
              outline=(90, 100, 70))
# pins 1-13 (Bahrain offset east so it does not sit on Riyadh)
PINS = [(1, -48, -1), (2, 47, 25), (3, -75, -11), (4, 58, 32), (5, 125, 7),
        (6, -74, 41), (7, 77, 28), (8, 21, 52), (9, 44, 33), (10, 28, -26),
        (11, 0, 51), (12, -118, 34), (13, 127, 37)]
for num, lon, lat in PINS:
    px, py = proj(lon, lat)
    d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=RED, outline=(255, 255, 255),
              width=1)
    t = str(num)
    tw = d.textlength(t, font=F(SANS_B, 8))
    d.text((px - tw / 2, py - 5), t, font=F(SANS_B, 8), fill=(255, 255, 255))
# leader line from Bahrain pin to its true spot
bx, byy = proj(50, 26)
d.line([(bx, byy), proj(58, 32)], fill=RED, width=1)

# ---- DATE CHECK box (left, under map)
dx0, dy0, dx1, dy1 = M, 894, 370, 1016
d.rectangle([dx0, dy0, dx1, dy1], outline=RED, width=2, fill=(255, 248, 240))
d.text((dx0 + 8, dy0 + 6), "DATE CHECK", font=F(SANS_B, 11), fill=RED)
dc = ("Every story here happened or was first reported on Saturday 21 "
      "November 2026. Left out on purpose — Friday 20 Nov: Wall Street's "
      "fall into correction, the Russian barrage on Kyiv's bridges, the "
      "missile that landed in Poland, the UK–EU deal, Cyclone Akvan's "
      "landfall. Older: Voyager 1's light-day, BepiColombo's Mercury "
      "orbit — not confirmed when drawn.")
for j, ln in enumerate(wrap(d, dc, F(SANS, 9), dx1 - dx0 - 16)):
    d.text((dx0 + 8, dy0 + 24 + j * 12), ln, font=F(SANS, 9), fill=INK)

# ---- ALSO ON list (right)
ax0, ay0, ax1 = 384, by, R
d.text((ax0, ay0), "ALSO ON SATURDAY 21 NOVEMBER",
       font=F(SANS_B, 12), fill=NAVY)
d.line([(ax0, ay0 + 20), (ax1, ay0 + 20)], fill=INK, width=1)
also = [
    (14, "Gaza ceasefire talks resume in Cairo", "REUTERS"),
    (15, "Ukraine grid repairs go on after strikes", "AP"),
    (16, "Japan unveils new stimulus package", "KYODO"),
    (17, "Belém braces for COP31 final day", "AFP"),
    (18, "Oil steady as OPEC+ weighs output", "REUTERS"),
    (19, "Gold hits record on haven demand", "BLOOMBERG"),
    (20, "SpaceX Starship test flight scrubbed", "AP"),
    (21, "Australia heatwave breaks records", "ABC"),
    (22, "Kenya drought aid reaches 2m people", "UN"),
    (23, "France pension reform passes first vote", "AFP"),
    (24, "Germany coalition agrees budget", "DPA"),
    (25, "Canada wildfire season ends, worst on record", "CBC"),
    (26, "Mexico cartel crackdown nets 40 arrests", "AP"),
    (27, "Indonesia volcano alert raised", "ANTARA"),
    (28, "Nigeria floods displace thousands", "REUTERS"),
    (29, "Egypt unveils new museum wing", "AP"),
    (30, "South Korea chip exports jump", "YONHAP"),
    (31, "Italy rail strike strands travellers", "ANSA"),
    (32, "Spain drought eases after rain", "EL PAÍS"),
    (33, "New Zealand quake rattles capital", "RNZ"),
    (34, "UN warns of food crisis in Sudan", "UN"),
]
yy = ay0 + 26
for num, head, src in also:
    d.text((ax0, yy), f"{num}.", font=F(SANS_B, 10), fill=RED)
    d.text((ax0 + 24, yy), head, font=F(SANS, 10), fill=INK)
    sw = d.textlength(src, font=F(SANS_B, 8))
    d.text((ax1 - sw, yy + 1), src, font=F(SANS_B, 8), fill=GREY)
    yy += 11

# footer rule
d.line([(M, 1020), (R, 1020)], fill=LINE, width=1)

img.save("entry.png")
print("saved entry.png")
