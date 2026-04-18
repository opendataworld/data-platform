#!/usr/bin/env python3
"""Generate og-image.png for site.open-data.world (1200x630)."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

W, H = 1200, 630
BG = (11, 12, 16)          # #0b0c10
FG = (230, 230, 230)
MUTED = (138, 143, 152)
ACCENT = (74, 222, 128)     # #4ade80

FONT_CANDIDATES = [
    "/System/Library/Fonts/Helvetica.ttc",
    "/System/Library/Fonts/HelveticaNeue.ttc",
    "/Library/Fonts/Arial.ttf",
    "/System/Library/Fonts/Supplemental/Arial.ttf",
]

def load_font(size):
    for p in FONT_CANDIDATES:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                continue
    return ImageFont.load_default()

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)

# Accent circle (brand mark)
d.ellipse((80, 80, 180, 180), fill=ACCENT)

# Small label
d.text((80, 220), "OPENDATAWORLD", fill=MUTED, font=load_font(20))

# Headline
d.text((80, 260), "Open-source data platform,", fill=FG, font=load_font(62))
d.text((80, 335), "assembled.", fill=FG, font=load_font(62))

# Tagline
d.text((80, 430), "Catalog · Ingest · Resolve · Model · Visualize", fill=MUTED, font=load_font(26))
d.text((80, 470), "OpenMetadata · Airbyte · Zingg · Cube · Superset · SurrealDB", fill=MUTED, font=load_font(18))

# URL footer
d.text((80, 560), "site.open-data.world", fill=ACCENT, font=load_font(22))

# Accent stripe on the right
d.rectangle((W - 8, 0, W, H), fill=ACCENT)

out = Path(__file__).parent / "og-image.png"
img.save(out, "PNG", optimize=True)
print(f"wrote {out} ({out.stat().st_size} bytes)")
