#!/usr/bin/env python3
"""Draw the news-image-20261121 front page: THE WORLD, Saturday 21 November 2026.

One 1024x1024 PNG, 38 dated stories, 7 regions. All headlines and summaries are
written here from facts verified against live reporting on 21 Nov 2026 (Reuters,
AP, AFP, Al Jazeera, USGS, IGP). Layout follows the front-page genre the
competition's top entries use; every word, number and drawing is our own.
Run: python3 draw.py  ->  writes entry.png next to this file.
"""
import math
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
M = 24                      # outer margin
CW = W - 2 * M              # content width = 976
CREAM = (246, 241, 227)
PAPER = (250, 246, 234)
INK = (20, 20, 20)
RED = (178, 34, 34)
DARKRED = (140, 20, 20)
GREY = (90, 86, 78)
LIGHT = (232, 224, 205)
NAVY = (16, 28, 58)

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIFB = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANSB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANSI = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"
SERI = "/usr/share/fonts/truetype/liberation/LiberationSerif-Italic.ttf"

_font_cache = {}
def font(path, size):
    key = (path, size)
    if key not in _font_cache:
        _font_cache[key] = ImageFont.truetype(path, size)
    return _font_cache[key]

def wrap(d, text, fnt, maxw):
    """Greedy word wrap; returns list of lines that fit maxw."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=fnt) <= maxw or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines

def para(d, x, y, text, fnt, maxw, fill=INK, leading=None, max_lines=None):
    """Draw wrapped paragraph; return y just below last line."""
    if leading is None:
        leading = int(fnt.size * 1.25)
    lines = wrap(d, text, fnt, maxw)
    if max_lines:
        lines = lines[:max_lines]
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y

def centre(d, cx, y, text, fnt, fill=INK):
    d.text((cx, y), text, font=fnt, fill=fill, anchor="ma")

# region colours
REGIONS = [
    ("EUROPE", 6, (31, 95, 168)),
    ("ASIA", 10, (201, 106, 30)),
    ("MIDDLE EAST", 4, (178, 34, 34)),
    ("AFRICA", 1, (46, 125, 79)),
    ("AMERICAS", 12, (106, 79, 163)),
    ("OCEANIA", 4, (14, 124, 123)),
    ("GLOBAL", 1, (102, 102, 102)),
]

NUMBERS = [
    ("13", "DAY OF COP31, MEANT TO CLOSE ON DAY 12"),
    ("3", "MISSILES SHOT DOWN OVER RIYADH"),
    ("6.7", "MAGNITUDE OF THE PERU QUAKE"),
    ("146", "PEOPLE SAFE AFTER THE DAVAO LANDING"),
    ("$58,983", "BITCOIN EARLY SATURDAY, DOWN 3.9% IN A DAY"),
    ("124*", "K L RAHUL'S SCORE AT TEA IN WELLINGTON"),
]

HEROES = [
    dict(num=1, place="ANTALYA, TÜRKIYE", beat="CLIMATE",
         kicker="COP31: OVERTIME",
         head="Climate summit runs into Saturday with no deal",
         body="Nearly 200 countries miss the Friday close; a draft with no fossil-fuel mention splits the room.",
         src="AP, Al Jazeera"),
    dict(num=2, place="RIYADH, SAUDI ARABIA", beat="WAR",
         kicker="SAUDI: MISSILES",
         head="Three Houthi missiles shot down over Riyadh",
         body="The Saudi-led coalition says it destroyed three ballistic missiles aimed at the capital early on Saturday.",
         src="Reuters, AFP"),
    dict(num=3, place="JUNÍN, PERU", beat="EARTHQUAKE",
         kicker="PERU: QUAKE 6.7",
         head="Magnitude 6.7 earthquake shakes central Peru",
         body="The deep quake near Junín was felt in Lima and along the coast; no deaths, no damage, no tsunami risk.",
         src="USGS, IGP"),
]

SECONDARY = [
    dict(num=4, place="KYIV", beat="WAR", color=(31, 95, 168),
         head="Zelensky: Crimea bridge \u201cwill not stay\u201d",
         body="He warns of double-tap strikes in an NBC interview.",
         src="NBC"),
    dict(num=5, place="STRAIT OF HORMUZ", beat="WAR", color=(178, 34, 34),
         head="Iran says it downed a US drone",
         body="Tehran claims the shootdown; Washington has not confirmed it.",
         src="IRIB"),
    dict(num=6, place="TEHRAN", beat="DIPLOMACY", color=(106, 79, 163),
         head="Iran: uranium stock stays in the country",
         body="Minister still seeks a \u201cfair solution\u201d.",
         src="Tasnim"),
    dict(num=7, place="WASHINGTON", beat="TECHNOLOGY", color=(201, 106, 30),
         head="Trump vows tax on data centres abroad",
         body="\u201cTremendous\u201d penalty promised; no details yet.",
         src="ABC"),
    dict(num=8, place="BEIJING", beat="DIPLOMACY", color=(178, 34, 34),
         head="China tells Japan to \u201ccorrect\u201d Taiwan words",
         body="Tokyo says its stance is unchanged.",
         src="AFP"),
    dict(num=9, place="DAVAO", beat="AVIATION", color=(14, 124, 123),
         head="Jet lands safely after engine fire alert",
         body="Air Niugini 767 diverts after midnight; all 146 safe.",
         src="AP"),
    dict(num=10, place="CANBERRA", beat="DIPLOMACY", color=(31, 95, 168),
         head="Australia and China agree to AI talks",
         body="Albanese wraps up an 11-day trip.",
         src="ABC"),
    dict(num=11, place="WORLD", beat="MARKETS", color=(102, 102, 102),
         head="Bitcoin trades below $59,000 on Saturday",
         body="Down 3.9% in 24 hours; ether $1,625.",
         src="CoinGecko"),
    dict(num=12, place="LAS VEGAS", beat="FORMULA ONE", color=(20, 20, 20),
         head="Russell fastest in final Las Vegas practice",
         body="1:34.041 in a damp, messy session.",
         src="Formula 1"),
    dict(num=13, place="WELLINGTON", beat="CRICKET", color=(46, 125, 79),
         head="Rahul hits a century against New Zealand",
         body="India 344 for 2 at tea, replying to 368.",
         src="AFP"),
]

ALSO = [
    (14, "Kryvyi Rih: double strike kills 2, injures 42 (Kyiv Ind.)"),
    (15, "Copenhagen: Russian attach\u00e9 expelled over plot (AJ)"),
    (16, "Antalya: EU warns COP31 risks a \u2018fossil summit\u2019 (AFP)"),
    (17, "Antalya: Panama threatens to block climate text (AJ)"),
    (18, "Jakarta: PLN signs clean-power deals (Antara)"),
    (19, "Yemen: Houthis threaten Jeddah, Red Sea ports (AJ)"),
    (20, "Washington: Vance: Iran strikes were Trump\u2019s call (Reuters)"),
    (21, "Washington: lawmaker threatens SpaceX funding (CNN)"),
    (22, "Texas: execution of man of 70 takes 63 minutes (ABC)"),
    (23, "Los Angeles: jury convicts Palisades fire starter (ABC)"),
    (24, "Missouri: judge approves $7.25bn Roundup deal (AFP)"),
    (25, "Vancouver: Canada rests defence in climate trial (AFP)"),
    (26, "Pyongyang: Kim tours factories, no Trump talks (AFP)"),
    (27, "Sejong: freight train derails, no one hurt (KH)"),
    (28, "Taipei: budget and cash payout passed (TT)"),
    (29, "Bangkok: six-point plan on arsenic in rivers (Nation)"),
    (30, "New Delhi: Pakistan minister joins SCO forum (Dawn)"),
    (31, "Eastern India: rain alerts as Akvan remnants move in (ETV)"),
    (32, "Myanmar: rights groups urge sanctions after ruling (AP)"),
    (33, "Port Louis: African rating agency talks to 15 states (AJ)"),
    (34, "Melbourne: Cummins keeps Australian captaincy (ABC)"),
    (35, "Las Vegas: Verstappen sent to stewards (Autosport)"),
    (36, "Paris: Diallo backed in FIFA vote (Reuters)"),
    (37, "Santiago: quake in north Chile (Reports)"),
    (38, "Sydney: AI camera row deepens (ABC)"),
]

# (lon, lat) of stories 1-13 for the map pins (nudged apart where the region crowds)
PINS = {
    1: (26.0, 38.0), 2: (42.0, 20.0), 3: (-75.9, -11.0), 4: (30.0, 54.0),
    5: (64.0, 24.0), 6: (55.0, 36.0), 7: (-77.0, 38.9), 8: (116.4, 39.9),
    9: (125.6, 7.1), 10: (146.0, -33.0), 11: (-0.1, 51.5), 12: (-115.1, 36.2),
    13: (170.0, -41.0),
}

# ---------- illustration helpers ----------

def draw_globe_thermo(d, x, y, w, h):
    """COP31: a globe, a red thermometer and a clock on pale blue."""
    d.rectangle([x, y, x + w, y + h], fill=(205, 228, 238))
    cx, cy, r = x + 62, y + 58, 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(70, 130, 200),
              outline=(20, 60, 120), width=2)
    d.ellipse([cx - 22, cy - 26, cx + 2, cy - 4], fill=(90, 180, 110))
    d.ellipse([cx - 4, cy + 8, cx + 24, cy + 28], fill=(90, 180, 110))
    d.ellipse([cx + 8, cy - 30, cx + 26, cy - 12], fill=(90, 180, 110))
    # thermometer
    tx = x + 150
    d.rounded_rectangle([tx, y + 14, tx + 16, y + 78], radius=8, fill=(250, 250, 250),
                        outline=(120, 40, 40), width=2)
    d.rectangle([tx + 3, y + 44, tx + 13, y + 76], fill=(200, 40, 40))
    d.ellipse([tx - 3, y + 72, tx + 19, y + 94], fill=(200, 40, 40))
    d.text((tx + 24, y + 16), "+1.5\u00b0C", font=font(SANSB, 15), fill=DARKRED)
    d.text((tx + 24, y + 38), "LIMIT", font=font(SANSB, 11), fill=DARKRED)
    d.text((tx + 24, y + 54), "AT RISK", font=font(SANSB, 11), fill=DARKRED)
    # clock
    kx, ky, kr = x + 262, y + 56, 30
    d.ellipse([kx - kr, ky - kr, kx + kr, ky + kr], fill=(250, 250, 250),
              outline=INK, width=2)
    d.line([kx, ky, kx, ky - 20], fill=INK, width=3)
    d.line([kx, ky, kx + 15, ky + 6], fill=INK, width=3)
    d.text((kx - 16, ky + 34), "DAY 13", font=font(SANSB, 11), fill=INK)

def draw_riyadh(d, x, y, w, h):
    """Riyadh: night skyline, moon, three missile trails with bursts."""
    d.rectangle([x, y, x + w, y + h], fill=NAVY)
    d.ellipse([x + w - 52, y + 10, x + w - 24, y + 38], fill=(240, 230, 180))
    import random
    rnd = random.Random(7)
    for _ in range(26):
        sx = x + rnd.randint(4, w - 8)
        sy = y + rnd.randint(4, 40)
        d.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 220))
    # skyline
    base = y + h
    for bx, bw, bh in [(6, 42, 52), (52, 30, 74), (86, 46, 44), (136, 34, 66),
                       (174, 50, 38), (228, 36, 60), (268, 44, 46)]:
        d.rectangle([x + bx, base - bh, x + bx + bw, base], fill=(8, 14, 34))
        for wy in range(base - bh + 8, base - 6, 12):
            for wx in range(x + bx + 6, x + bx + bw - 6, 11):
                if rnd.random() < 0.55:
                    d.rectangle([wx, wy, wx + 5, wy + 6], fill=(255, 210, 90))
    # missile trails: dotted arcs rising to bursts
    for tx0, tx1, ty in [(20, 120, 26), (150, 210, 18), (240, 300, 30)]:
        steps = 26
        for i in range(steps):
            t = i / steps
            px = x + tx0 + (tx1 - tx0) * t
            py = y + h - 8 - (y + h - 8 - (y + ty)) * t * t - 26 * math.sin(math.pi * t)
            d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=(255, 210, 90))
        bx, by = x + tx1, y + ty
        for ang in range(0, 360, 45):
            ex = bx + 11 * math.cos(math.radians(ang))
            ey = by + 11 * math.sin(math.radians(ang))
            d.line([bx, by, ex, ey], fill=(255, 200, 60), width=2)
        d.ellipse([bx - 4, by - 4, bx + 4, by + 4], fill=(255, 240, 160))
    d.rectangle([x, y + h - 20, x + w, y + h], fill=(8, 14, 34))

def draw_quake(d, x, y, w, h):
    """Peru: red seismograph trace over hills and small houses."""
    d.rectangle([x, y, x + w, y + h], fill=(238, 226, 198))
    # hills
    d.polygon([(x, y + h), (x, y + 84), (x + 90, y + 58), (x + 180, y + 88),
               (x + 260, y + 62), (x + w, y + 86), (x + w, y + h)], fill=(196, 178, 138))
    # houses
    for hx, hw in [(28, 52), (108, 46), (196, 56), (268, 44)]:
        hy = y + h - 46
        d.rectangle([x + hx, hy, x + hx + hw, y + h - 10], fill=(250, 244, 228),
                    outline=(120, 90, 60), width=1)
        d.polygon([(x + hx - 4, hy), (x + hx + hw // 2, hy - 20), (x + hx + hw + 4, hy)],
                  fill=(178, 60, 40))
        d.rectangle([x + hx + hw // 2 - 6, y + h - 26, x + hx + hw // 2 + 6, y + h - 10],
                    fill=(90, 60, 40))
    # seismograph trace
    pts = []
    n = 46
    for i in range(n + 1):
        px = x + 8 + (w - 16) * i / n
        if 10 <= i <= 15 or 30 <= i <= 34:
            amp = 26 if i % 2 == 0 else -26
        elif i in (16, 17, 35):
            amp = 12 if i % 2 == 0 else -12
        else:
            amp = 3 if i % 2 == 0 else -3
        pts.append((px, y + 34 + amp))
    d.line(pts, fill=(200, 30, 30), width=3, joint="curve")
    d.text((x + 8, y + 6), "00:09 UTC", font=font(SANSB, 11), fill=DARKRED)
    d.text((x + w - 8, y + 6), "6.7", font=font(SERIFB, 22), fill=DARKRED, anchor="ra")
    d.rectangle([x + 6, y + 21, x + 96, y + 36], fill=(238, 226, 198))
    d.text((x + 8, y + 23), "108 KM DEEP", font=font(SANSB, 10), fill=DARKRED)

HERO_DRAW = [draw_globe_thermo, draw_riyadh, draw_quake]

# ---------- simplified world map ----------

CONTINENTS = [
    # North America
    [(-168, 66), (-150, 70), (-130, 71), (-115, 68), (-100, 69), (-88, 66),
     (-82, 70), (-76, 62), (-70, 58), (-65, 49), (-70, 42), (-75, 35),
     (-81, 26), (-84, 30), (-90, 21), (-94, 17), (-100, 20), (-105, 22),
     (-112, 29), (-120, 34), (-124, 42), (-125, 49), (-135, 58), (-152, 60),
     (-162, 58), (-168, 66)],
    # South America
    [(-79, 9), (-76, 4), (-72, 0), (-68, -4), (-62, -8), (-57, -13),
     (-52, -18), (-47, -23), (-41, -28), (-48, -32), (-57, -36), (-62, -41),
     (-66, -47), (-70, -52), (-72, -42), (-73, -32), (-74, -22), (-77, -12),
     (-80, -4), (-81, 2), (-79, 9)],
    # Europe
    [(-10, 36), (-8, 43), (-2, 48), (0, 50), (4, 53), (8, 57), (12, 55),
     (18, 56), (21, 60), (25, 65), (30, 70), (35, 68), (40, 63), (38, 56),
     (33, 52), (28, 46), (24, 40), (19, 38), (14, 38), (9, 37), (4, 36),
     (-2, 36), (-10, 36)],
    # Africa
    [(-6, 35), (0, 36), (10, 37), (16, 32), (22, 32), (28, 31), (33, 28),
     (38, 22), (43, 12), (48, 11), (51, 10), (46, 4), (41, -1), (38, -6),
     (35, -12), (32, -18), (29, -25), (25, -30), (20, -35), (18, -30),
     (15, -20), (12, -10), (10, 0), (6, 4), (0, 5), (-6, 5), (-10, 11),
     (-15, 17), (-17, 22), (-15, 28), (-10, 31), (-6, 35)],
    # Asia
    [(35, 68), (45, 68), (55, 70), (65, 72), (75, 73), (90, 75), (110, 76),
     (130, 72), (150, 70), (160, 65), (162, 60), (158, 52), (150, 45),
     (142, 40), (135, 35), (130, 33), (127, 38), (122, 32), (118, 25),
     (110, 20), (105, 10), (100, 8), (95, 15), (90, 22), (85, 20),
     (80, 15), (75, 8), (72, 20), (68, 25), (60, 25), (55, 28), (50, 30),
     (48, 35), (45, 38), (40, 36), (38, 40), (35, 45), (35, 55), (30, 60),
     (35, 68)],
    # Australia
    [(113, -22), (115, -32), (120, -35), (130, -32), (140, -38), (146, -38),
     (150, -37), (153, -32), (150, -27), (146, -20), (142, -15), (137, -12),
     (132, -12), (126, -14), (120, -18), (115, -20), (113, -22)],
]

def draw_map(d, x, y, w, h):
    d.rectangle([x, y, x + w, y + h], fill=(214, 230, 240))
    def mx(lon):
        return x + (lon + 180) / 360.0 * w
    def my(lat):
        return y + (85 - lat) / 145.0 * h
    for poly in CONTINENTS:
        pts = [(mx(lon), my(lat)) for lon, lat in poly]
        d.polygon(pts, fill=(232, 220, 192), outline=(150, 130, 95))
    for num, (lon, lat) in PINS.items():
        px, py = mx(lon), my(lat)
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED, outline=(255, 255, 255), width=1)
        d.text((px, py - 1), str(num), font=font(SANSB, 9), fill=(255, 255, 255), anchor="mm")

# ---------- page build ----------

def build():
    img = Image.new("RGB", (W, H), CREAM)
    d = ImageDraw.Draw(img)

    # kicker line
    d.text((M, 10), "THE WORLD IN ONE DAY", font=font(SANSB, 14), fill=RED)
    right = "38 STORIES  \u00b7  7 REGIONS  \u00b7  EVERY ONE DATED SATURDAY 21 NOVEMBER 2026"
    d.text((W - M, 11), right, font=font(SANSB, 12), fill=INK, anchor="ra")
    d.line([M, 30, W - M, 30], fill=RED, width=2)

    # masthead
    centre(d, W // 2, 38, "Saturday 21 November 2026", font(SERIFB, 56), INK)
    centre(d, W // 2, 102,
           "Climate summit runs past its deadline  \u00b7  Three missiles shot down over Riyadh  \u00b7  Strong quake shakes Peru",
           font(SERIF, 16), GREY)
    d.line([M, 126, W - M, 126], fill=INK, width=2)

    # number strip: six figures of the day
    strip_y, strip_h = 134, 62
    cell_w = CW // 6
    for i, (num, cap) in enumerate(NUMBERS):
        cx = M + i * cell_w
        if i:
            d.line([cx, strip_y + 6, cx, strip_y + strip_h - 6], fill=(190, 180, 160), width=1)
        centre(d, cx + cell_w // 2, strip_y + 2, num, font(SERIFB, 30), RED)
        para(d, cx + 8, strip_y + 36, cap, font(SANSB, 9), cell_w - 16,
             fill=INK, leading=11, max_lines=2)
    d.line([M, strip_y + strip_h + 4, W - M, strip_y + strip_h + 4], fill=INK, width=1)

    # region bar
    bar_y, bar_h = 206, 22
    seg_w = CW // 7
    for i, (name, count, color) in enumerate(REGIONS):
        x0 = M + i * seg_w
        wseg = seg_w if i < 6 else CW - 6 * seg_w
        d.rectangle([x0, bar_y, x0 + wseg - 1, bar_y + bar_h], fill=color)
        centre(d, x0 + wseg // 2, bar_y + 4, f"{name} {count}", font(SANSB, 11),
               (255, 255, 255))

    # heroes: three big stories
    hero_y, hero_h, hero_w, gap = 236, 232, 322, 8
    for i, h in enumerate(HEROES):
        x0 = M + i * (hero_w + gap)
        d.rectangle([x0, hero_y, x0 + hero_w, hero_y + hero_h], fill=PAPER,
                    outline=(180, 168, 140), width=1)
        HERO_DRAW[i](d, x0 + 1, hero_y + 1, hero_w - 2, 112)
        d.rectangle([x0, hero_y + 113, x0 + hero_w, hero_y + 135], fill=RED)
        d.text((x0 + 8, hero_y + 117), h["kicker"], font=font(SANSB, 12), fill=(255, 255, 255))
        short_place = {"ANTALYA, TÜRKIYE": "ANTALYA", "RIYADH, SAUDI ARABIA": "RIYADH",
                       "JUNÍN, PERU": "JUNÍN"}[h["place"]]
        d.text((x0 + hero_w - 8, hero_y + 117), f"{h['num']} {short_place} \u00b7 {h['beat']}",
               font=font(SANSB, 10), fill=(255, 255, 255), anchor="ra")
        y = para(d, x0 + 8, hero_y + 141, h["head"], font(SERIFB, 19), hero_w - 16,
                 leading=22, max_lines=2)
        y = para(d, x0 + 8, y + 3, h["body"], font(SANS, 11), hero_w - 16,
                 fill=(50, 48, 44), leading=14, max_lines=3)
        d.text((x0 + 8, hero_y + hero_h - 16), f"({h['src']})", font=font(SANSI, 9), fill=GREY)

    # secondary grid: stories 4-13, five columns, two rows
    grid_y, card_w, card_h, cg = 476, 188, 108, 9
    for i, s in enumerate(SECONDARY):
        col, row = i % 5, i // 5
        x0 = M + col * (card_w + cg)
        y0 = grid_y + row * (card_h + cg)
        d.rectangle([x0, y0, x0 + card_w, y0 + card_h], fill=PAPER,
                    outline=(180, 168, 140), width=1)
        d.rectangle([x0, y0, x0 + card_w, y0 + 20], fill=s["color"])
        d.text((x0 + 6, y0 + 4), f"{s['num']}  {s['place']}  \u00b7  {s['beat']}",
               font=font(SANSB, 10), fill=(255, 255, 255))
        y = para(d, x0 + 6, y0 + 25, s["head"], font(SERIFB, 13), card_w - 12,
                 leading=15, max_lines=2)
        para(d, x0 + 6, y + 2, s["body"], font(SANS, 10), card_w - 12,
             fill=(50, 48, 44), leading=12, max_lines=2)
        d.text((x0 + 6, y0 + card_h - 14), f"({s['src']})", font=font(SANSI, 8), fill=GREY)

    # map + also list
    bot_y = 710
    d.text((M, bot_y), "WHERE IT HAPPENED", font=font(SANSB, 12), fill=RED)
    d.text((M, bot_y + 16), "Stories 1\u201313, numbered as above", font=font(SANS, 9), fill=GREY)
    draw_map(d, M, bot_y + 32, 300, 168)
    d.text((M, bot_y + 204), "Each number is the story with that number on this page.",
           font=font(SANS, 9), fill=GREY)

    ax = M + 312
    aw = W - M - ax
    d.text((ax, bot_y), "ALSO ON SATURDAY 21 NOVEMBER  \u2014  25 MORE STORIES",
           font=font(SANSB, 12), fill=RED)
    col_w = aw // 2
    f_also = font(SANS, 10)
    for i, (num, text) in enumerate(ALSO):
        col = 0 if i < 13 else 1
        row = i if i < 13 else i - 13
        tx = ax + col * col_w
        ty = bot_y + 20 + row * 15
        d.text((tx, ty), f"{num}", font=font(SANSB, 10), fill=RED)
        d.text((tx + 20, ty), text, font=f_also, fill=INK)

    # date check box
    dc_y = 936
    d.rectangle([M, dc_y, W - M, dc_y + 52], outline=RED, width=2)
    d.text((M + 8, dc_y + 5), "DATE CHECK", font=font(SANSB, 11), fill=RED)
    para(d, M + 8, dc_y + 20,
         "Left out as Friday 20 November\u2019s news: Wall Street\u2019s fall into correction, the Russian barrage that hit Kyiv\u2019s bridges, the missile that landed in Poland, the UK\u2013EU deal, Cyclone Akvan\u2019s landfall. Older still: Voyager 1\u2019s light-day (18 Nov). Not confirmed when drawn, so not shown: BepiColombo in Mercury orbit, a final COP31 text.",
         font(SANS, 10), CW - 16, fill=INK, leading=13, max_lines=2)

    # footer
    centre(d, W // 2, 996,
           "Every story here happened, or was first reported, on Saturday 21 November 2026. Sources named beside each story. Original drawings.",
           font(SANS, 10), GREY)

    img.save("entry.png", optimize=True)
    import os
    print("saved entry.png", os.path.getsize("entry.png"), "bytes")

if __name__ == "__main__":
    build()
