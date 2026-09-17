from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "mactrix.ico"


def build(size: int = 512) -> Image.Image:
    image = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    scale = size / 512

    def box(values):
        return tuple(int(value * scale) for value in values)

    draw.rounded_rectangle(box((20, 20, 492, 492)), radius=int(108 * scale), fill=(7, 17, 31, 255), outline=(20, 121, 214, 255), width=max(2, int(6 * scale)))

    for pos in (120, 196, 272, 348):
        draw.line((int(76 * scale), int(pos * scale), int(436 * scale), int(pos * scale)), fill=(16, 57, 93, 170), width=max(1, int(4 * scale)))
        draw.line((int(pos * scale), int(76 * scale), int(pos * scale), int(436 * scale)), fill=(16, 57, 93, 170), width=max(1, int(4 * scale)))

    for x, y, radius in ((120, 120, 9), (196, 196, 7), (348, 120, 7), (120, 348, 7), (348, 348, 9)):
        r = int(radius * scale)
        cx, cy = int(x * scale), int(y * scale)
        draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(66, 197, 255, 235))

    m = [
        (122, 352), (122, 160), (146, 135), (165, 142), (256, 230),
        (347, 142), (366, 135), (390, 160), (390, 352), (338, 352),
        (338, 224), (256, 302), (174, 224), (174, 352),
    ]
    draw.polygon([(int(x * scale), int(y * scale)) for x, y in m], fill=(42, 165, 255, 255))
    draw.rounded_rectangle(box((103, 389, 409, 409)), radius=int(10 * scale), fill=(102, 214, 255, 245))
    return image


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image = build()
    image.save(OUTPUT, format="ICO", sizes=[(16, 16), (24, 24), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
    print(f"Wrote {OUTPUT}")


if __name__ == "__main__":
    main()
