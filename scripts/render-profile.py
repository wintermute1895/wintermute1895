"""Generate the self-hosted profile animation and light-mode university mark."""
from pathlib import Path
import math
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
mark = Image.open(ASSETS / "tianjin-university.png").convert("RGBA")
blue = Image.new("RGBA", mark.size, (26, 74, 119, 255))
blue.putalpha(mark.getchannel("A"))
blue.save(ASSETS / "tianjin-university-blue.png")

def font(size, bold=False):
    return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans" + ("-Bold" if bold else "") + ".ttf", size)

frames = []
labels = ["TELEOPERATION + SHARED CONTROL", "INVERSE KINEMATICS + RETARGETING", "REAL2SIM + POLICY EVALUATION"]
for i in range(90):
    t = i / 90 * 2 * math.pi
    im = Image.new("RGB", (1000, 260), "#101c30")
    d = ImageDraw.Draw(im)
    for x in range(0, 1000, 40):
        d.line((x, 0, x, 260), fill="#192a40")
    for y in range(0, 260, 40):
        d.line((0, y, 1000, y), fill="#192a40")
    d.text((40, 25), "HUMAN INTENT / ROBOT ACTION", font=font(13), fill="#7dd3c7")
    d.text((36, 60), "wintermute", font=font(56, True), fill="#f1f5f9")
    d.text((40, 142), labels[i // 30], font=font(17), fill="#d2e0ed")
    d.text((40, 211), "Tianjin University  /  Class of 2027", font=font(15), fill="#9eb5ca")
    base = (785, 217)
    a = -2.05 + .22 * math.sin(t)
    b = -.45 + .45 * math.cos(t)
    elbow = (base[0] + 92 * math.cos(a), base[1] + 92 * math.sin(a))
    tip = (elbow[0] + 95 * math.cos(b), elbow[1] + 95 * math.sin(b))
    d.line((base, elbow, tip), fill="#7dd3c7", width=8)
    d.line((749, 229, 821, 229), fill="#9eb5ca", width=5)
    for x, y in (base, elbow, tip):
        d.ellipse((x-8, y-8, x+8, y+8), fill="#101c30", outline="#7dd3c7", width=3)
    x, y = tip
    d.line((x+8, y-8, x+23, y-8, x+27, y-2), fill="#7dd3c7", width=3)
    d.line((x+8, y+8, x+23, y+8, x+27, y+2), fill="#7dd3c7", width=3)
    for j in range(3):
        d.ellipse((40+j*18, 183, 46+j*18, 189), fill="#7dd3c7" if j == i//30 else "#40536a")
    frames.append(im.quantize(colors=64))
frames[0].save(ASSETS / "robotics-loop.gif", save_all=True, append_images=frames[1:], duration=100, loop=0, optimize=True)
frames[15].save(ASSETS / "robotics-preview.png")
