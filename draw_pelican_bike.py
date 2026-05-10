#!/usr/bin/env python3
"""Render a storybook pelican riding a bicycle with Pillow."""

from __future__ import annotations

import math
import os
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 960
SS = 2
SW, SH = W * SS, H * SS
OUT = Path(__file__).resolve().parent / "output" / "pelican_bike_claude.png"
FONT_DIR = Path("/usr/share/fonts/truetype/dejavu")


def P(x: float) -> int:
    return int(round(x * SS))


def box(cx: float, cy: float, rx: float, ry: float) -> tuple[int, int, int, int]:
    return (P(cx - rx), P(cy - ry), P(cx + rx), P(cy + ry))


def pts(points):
    return [(P(x), P(y)) for x, y in points]


def line(draw, points, fill, width=1, joint="curve"):
    draw.line(pts(points), fill=fill, width=P(width), joint=joint)


def ellipse(draw, cx, cy, rx, ry, fill, outline=None, width=1):
    draw.ellipse(box(cx, cy, rx, ry), fill=fill, outline=outline, width=P(width) if outline else 1)


def polygon(draw, points, fill, outline=None):
    draw.polygon(pts(points), fill=fill)
    if outline:
        line(draw, [*points, points[0]], outline, 2)


def load_font(name: str, size: int):
    try:
        return ImageFont.truetype(str(FONT_DIR / name), P(size))
    except OSError:
        return ImageFont.load_default()


def draw_sky(draw):
    top, bottom = (108, 181, 242), (212, 236, 255)
    for y in range(SH):
        t = y / max(1, SH - 1)
        col = tuple(int(top[i] * (1 - t) + bottom[i] * t) for i in range(3))
        draw.line([(0, y), (SW, y)], fill=col)


def draw_sun(draw):
    cx, cy = 1050, 145
    for r, a in [(120, 22), (86, 34), (60, 48)]:
        ellipse(draw, cx, cy, r, r, (255, 224, 115, a))
    for a in range(0, 360, 18):
        rad = math.radians(a)
        line(draw, [(cx + math.cos(rad) * 74, cy + math.sin(rad) * 74),
                    (cx + math.cos(rad) * 105, cy + math.sin(rad) * 105)], (255, 220, 95, 95), 3)
    ellipse(draw, cx, cy, 46, 46, (255, 219, 101, 230))


def draw_cloud(draw, cx, cy, s):
    color = (255, 255, 255, 205)
    shadow = (190, 214, 235, 60)
    for ox, oy, rx, ry in [(-48, 5, 45, 25), (0, -10, 58, 34), (50, 7, 42, 24), (15, 9, 70, 26)]:
        ellipse(draw, cx + ox*s, cy + oy*s + 7*s, rx*s, ry*s, shadow)
    for ox, oy, rx, ry in [(-48, 5, 45, 25), (0, -10, 58, 34), (50, 7, 42, 24), (15, 9, 70, 26)]:
        ellipse(draw, cx + ox*s, cy + oy*s, rx*s, ry*s, color)


def draw_hills(draw):
    back = [(0, 610)] + [(x, 555 + 38 * math.sin(x / 110)) for x in range(0, W + 70, 70)] + [(W, H), (0, H)]
    front = [(0, 690)] + [(x, 640 + 28 * math.sin(x / 95 + 1.3)) for x in range(0, W + 55, 55)] + [(W, H), (0, H)]
    polygon(draw, back, (104, 166, 126))
    polygon(draw, front, (128, 187, 113))


def draw_path(draw):
    polygon(draw, [(0, 805), (420, 675), (830, 680), (1280, 825), (1280, 960), (0, 960)], (223, 195, 145))
    polygon(draw, [(160, 960), (495, 706), (765, 708), (1110, 960)], (238, 213, 164))
    for i in range(110):
        x = (i * 137) % W
        y = 730 + ((i * 53) % 220)
        r = 1.5 + (i % 4)
        ellipse(draw, x, y, r, r * .65, (178, 147, 104, 80))


def draw_trees_flowers_birds(draw):
    for tx, ty, s in [(92, 625, .9), (1135, 610, .82), (1025, 650, .58)]:
        polygon(draw, [(tx-8*s, ty), (tx+8*s, ty), (tx+5*s, ty-70*s), (tx-5*s, ty-70*s)], (122, 78, 46))
        for ox, oy, c in [(-24, -75, (66, 139, 74)), (16, -88, (76, 158, 78)), (0, -112, (60, 130, 68))]:
            ellipse(draw, tx+ox*s, ty+oy*s, 38*s, 31*s, c)
    for bx, by, s in [(210, 205, 1), (260, 180, .8), (910, 245, .75), (970, 230, .62)]:
        line(draw, [(bx-14*s, by), (bx, by-8*s), (bx+14*s, by)], (58, 78, 110, 150), 2)
    for i in range(42):
        x = 65 + (i * 83) % 1140
        y = 704 + (i * 37) % 115
        stem = (62, 138, 62)
        line(draw, [(x, y+12), (x, y+26)], stem, 2)
        petal = [(245, 112, 150), (255, 213, 80), (143, 118, 210), (250, 151, 93)][i % 4]
        for a in range(0, 360, 60):
            ellipse(draw, x + math.cos(math.radians(a))*6, y + math.sin(math.radians(a))*6, 4, 3, petal)
        ellipse(draw, x, y, 2.4, 2.4, (91, 69, 36))


def draw_wheel(draw, cx, cy, r):
    ellipse(draw, cx, cy, r+7, r+7, None, (37, 45, 48), 13)
    ellipse(draw, cx, cy, r-3, r-3, None, (210, 222, 225), 4)
    for i in range(16):
        a = math.tau * i / 16
        line(draw, [(cx, cy), (cx + math.cos(a)*(r-10), cy + math.sin(a)*(r-10))], (117, 132, 138, 185), 1.5)
    ellipse(draw, cx, cy, 12, 12, (72, 81, 85), (232, 238, 236), 2)


def draw_bike(draw):
    rear, front, crank = (420, 710), (860, 710), (620, 710)
    seat_top, head, handle = (590, 545), (810, 560), (885, 515)
    red, dark = (202, 45, 50), (129, 34, 41)
    draw_wheel(draw, *rear, 112)
    draw_wheel(draw, *front, 112)
    tubes = [(rear, crank), (crank, front), (front, head), (head, seat_top), (seat_top, rear), (seat_top, crank), (rear, head)]
    for a, b in tubes:
        line(draw, [a, b], dark, 13)
        line(draw, [a, b], red, 8)
    line(draw, [head, (850, 532), handle], (52, 60, 62), 8)
    line(draw, [(872, 515), (917, 504), (930, 516)], (52, 60, 62), 7)
    line(draw, [(894, 502), (925, 492)], (44, 48, 50), 8)
    line(draw, [seat_top, (582, 515)], (58, 64, 64), 8)
    polygon(draw, [(535, 518), (630, 520), (646, 535), (548, 542)], (92, 63, 45), (54, 40, 32))
    ellipse(draw, *crank, 30, 30, None, (72, 76, 70), 5)
    for a in range(0, 360, 30):
        rad = math.radians(a)
        line(draw, [(crank[0] + math.cos(rad)*23, crank[1] + math.sin(rad)*23),
                    (crank[0] + math.cos(rad)*30, crank[1] + math.sin(rad)*30)], (85, 88, 81), 2)
    pedal1 = (crank[0] + math.cos(math.radians(32))*58, crank[1] + math.sin(math.radians(32))*58)
    pedal2 = (crank[0] + math.cos(math.radians(212))*58, crank[1] + math.sin(math.radians(212))*58)
    line(draw, [crank, pedal1], (60, 63, 61), 5)
    line(draw, [crank, pedal2], (60, 63, 61), 5)
    for px, py in [pedal1, pedal2]:
        line(draw, [(px-17, py), (px+17, py)], (48, 51, 50), 5)
    line(draw, [(crank[0]-26, crank[1]-7), (rear[0], rear[1]-8), (crank[0]-24, crank[1]+8), (rear[0], rear[1]+8)], (45, 44, 38, 190), 3)
    return {"seat": (590, 518), "handle": (925, 492), "crank": crank, "pedal1": pedal1, "pedal2": pedal2}


def bezier(p0, p1, p2, p3, n=28):
    out = []
    for i in range(n + 1):
        t = i / n
        x = (1-t)**3*p0[0] + 3*(1-t)**2*t*p1[0] + 3*(1-t)*t*t*p2[0] + t**3*p3[0]
        y = (1-t)**3*p0[1] + 3*(1-t)**2*t*p1[1] + 3*(1-t)*t*t*p2[1] + t**3*p3[1]
        out.append((x, y))
    return out


def ribbon_from_curve(curve, widths):
    left, right = [], []
    for i, (x, y) in enumerate(curve):
        j0, j1 = max(0, i-1), min(len(curve)-1, i+1)
        dx = curve[j1][0] - curve[j0][0]
        dy = curve[j1][1] - curve[j0][1]
        ln = math.hypot(dx, dy) or 1
        nx, ny = -dy / ln, dx / ln
        w = widths[i] / 2
        left.append((x + nx*w, y + ny*w))
        right.append((x - nx*w, y - ny*w))
    return left + right[::-1]


def draw_pelican(draw, anchors):
    seat_x, seat_y = anchors["seat"]
    handle_x, handle_y = anchors["handle"]
    p1, p2 = anchors["pedal1"], anchors["pedal2"]
    cream, outline = (245, 243, 232), (176, 168, 150)
    orange, orange2 = (244, 173, 72), (246, 198, 137)
    ellipse(draw, seat_x-6, seat_y+84, 116, 92, (211, 205, 185, 55))
    for a in [-18, 0, 18]:
        line(draw, [(seat_x-100, seat_y+35), (seat_x-135, seat_y+22+a)], outline, 3)
    ellipse(draw, seat_x-28, seat_y+36, 150, 116, cream, outline, 4)
    ellipse(draw, seat_x-58, seat_y+38, 78, 88, (232, 229, 216), outline, 2)
    for i in range(4):
        line(draw, [(seat_x-96+i*18, seat_y+2+i*4), (seat_x-40+i*12, seat_y+73)], (202, 198, 183), 2)
    neck_curve = bezier((seat_x+55, seat_y-15), (seat_x+70, seat_y-120), (seat_x+160, seat_y-130), (seat_x+207, seat_y-84), 34)
    widths = [44 - i * .45 for i in range(len(neck_curve))]
    polygon(draw, ribbon_from_curve(neck_curve, widths), cream, outline)
    ellipse(draw, seat_x+220, seat_y-80, 58, 42, cream, outline, 3)
    beak = [(seat_x+248, seat_y-92), (seat_x+392, seat_y-103), (seat_x+430, seat_y-86), (seat_x+388, seat_y-76), (seat_x+260, seat_y-68)]
    polygon(draw, beak, orange, (171, 109, 46))
    pouch = [(seat_x+263, seat_y-66), (seat_x+383, seat_y-75), (seat_x+362, seat_y-29), (seat_x+275, seat_y-38)]
    polygon(draw, pouch, orange2, (180, 120, 70))
    line(draw, [(seat_x+257, seat_y-82), (seat_x+404, seat_y-88)], (155, 93, 43), 2)
    ellipse(draw, seat_x+226, seat_y-94, 9, 9, (255, 255, 255), (70, 62, 50), 1.5)
    ellipse(draw, seat_x+228, seat_y-94, 4, 4, (35, 35, 35))
    ellipse(draw, seat_x+230, seat_y-96, 1.5, 1.5, (255, 255, 255))
    for dx in [-24, -13, -3, 8, 18]:
        line(draw, [(seat_x+194, seat_y-111), (seat_x+194+dx, seat_y-137-abs(dx)*.25)], outline, 2)
    wing = [(seat_x+62, seat_y+0), (seat_x+170, seat_y-20), (handle_x-14, handle_y+12), (handle_x-6, handle_y+36), (seat_x+86, seat_y+75), (seat_x+30, seat_y+54)]
    polygon(draw, wing, (237, 234, 222), outline)
    for i in range(4):
        line(draw, [(seat_x+105+i*16, seat_y+23+i*3), (handle_x-35+i*7, handle_y+27+i*7)], (198, 194, 179), 2)
    for knee, foot in [((seat_x-7, seat_y+142), p1), ((seat_x+64, seat_y+132), p2)]:
        line(draw, [(seat_x+22, seat_y+102), knee, foot], (224, 145, 44), 9)
        ellipse(draw, foot[0], foot[1], 23, 10, orange, (158, 91, 35), 2)
        for off in [-12, 0, 12]:
            line(draw, [(foot[0]+off*.4, foot[1]), (foot[0]+off, foot[1]+11)], (158, 91, 35), 1.3)


def draw_motion(draw):
    for i in range(7):
        y = 650 + i * 18
        line(draw, [(245 - i*10, y), (335 - i*6, y-7)], (80, 100, 130, 80), 2)


def draw_title(draw):
    title_font = load_font("DejaVuSans-Bold.ttf", 44)
    sub_font = load_font("DejaVuSans.ttf", 20)
    for text, y, font, fill in [("Pelican on a Bike", 42, title_font, (32, 50, 96, 245)), ("~ a whimsical ride ~", 96, sub_font, (90, 86, 140, 230))]:
        bbox = draw.textbbox((0, 0), text, font=font)
        x = P((W - (bbox[2]-bbox[0]) / SS) / 2)
        draw.text((x + P(2), P(y+2)), text, font=font, fill=(255, 255, 255, 165))
        draw.text((x, P(y)), text, font=font, fill=fill)


def main():
    img = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img, "RGBA")
    draw_sky(draw)
    draw_sun(draw)
    for c in [(220, 160, 1.0), (460, 120, .68), (760, 205, .82), (1060, 285, .62)]:
        draw_cloud(draw, *c)
    draw_hills(draw)
    draw_path(draw)
    draw_trees_flowers_birds(draw)
    draw_motion(draw)
    anchors = draw_bike(draw)
    draw_pelican(draw, anchors)
    draw_title(draw)
    final = img.convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    final.save(OUT)
    print(f"Saved {OUT} ({W}x{H})")


if __name__ == "__main__":
    main()
