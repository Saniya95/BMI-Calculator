from PIL import Image, ImageDraw, ImageFont

SIZE = 1024
BG = (84, 145, 230, 255)

img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# Rounded square blue base like the reference icon.
draw.rounded_rectangle((0, 0, SIZE, SIZE), radius=95, fill=BG)

# Gauge geometry
cx = SIZE // 2
cy = 560
outer_r = 505
ring = 28

# White gauge ring
draw.pieslice(
    (cx - outer_r, cy - outer_r, cx + outer_r, cy + outer_r),
    180,
    360,
    fill=(245, 245, 245, 255),
)
inner_r = outer_r - ring
draw.pieslice(
    (cx - inner_r, cy - inner_r, cx + inner_r, cy + inner_r),
    180,
    360,
    fill=BG,
)

# Colored gauge segments
segments = [
    (180, 230, (111, 93, 220, 255)),
    (230, 270, (13, 239, 57, 255)),
    (270, 320, (245, 208, 0, 255)),
    (320, 360, (252, 0, 119, 255)),
]
for start, end, color in segments:
    draw.pieslice(
        (cx - inner_r + 2, cy - inner_r + 2, cx + inner_r - 2, cy + inner_r - 2),
        start,
        end,
        fill=color,
    )

# Cut lower half to keep a semicircle only.
draw.rectangle((0, cy, SIZE, SIZE), fill=BG)

# Hub base and cap
draw.ellipse((cx - 150, cy - 150, cx + 150, cy + 150), fill=(238, 238, 243, 255))
draw.ellipse((cx - 110, cy - 110, cx + 110, cy + 110), fill=(52, 50, 76, 255))

# Needle (towards upper-left)
needle = [(cx - 18, cy + 20), (cx + 24, cy - 2), (cx - 172, cy - 250)]
draw.polygon(needle, fill=(52, 50, 76, 255))

# Center dot
draw.ellipse((cx - 24, cy - 24, cx + 24, cy + 24), fill=(241, 241, 246, 255))

# BMI text block
font = None
for path in [
    "C:/Windows/Fonts/arialbd.ttf",
    "C:/Windows/Fonts/segoeuib.ttf",
    "C:/Windows/Fonts/calibrib.ttf",
]:
    try:
        font = ImageFont.truetype(path, 285)
        break
    except OSError:
        continue
if font is None:
    font = ImageFont.load_default()

text = "BMI"
bbox = draw.textbbox((0, 0), text, font=font)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]
tx = (SIZE - tw) // 2
ty = 690 - (th // 2)
draw.text((tx, ty), text, font=font, fill=(242, 242, 242, 255))

img.save("assets/icon.png", "PNG")
print("Generated replica-style assets/icon.png")
