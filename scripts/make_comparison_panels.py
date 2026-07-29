from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

ids = ["00000008", "00000210", "00000211", "00000265", "00000279"]

root = Path("data/RGBD_GSD/test")
rgb_pred_dir = Path("results/qualitative_analysis/rgb")
rgbd_pred_dir = Path("results/qualitative_analysis/rgbd")
out_dir = Path("results/comparison_panels")
out_dir.mkdir(parents=True, exist_ok=True)

def load_resize(path, size=(512, 512), grayscale=False):
    img = Image.open(path)
    img = img.convert("L" if grayscale else "RGB")
    img = img.resize(size)
    return img

for image_id in ids:
    original = load_resize(root / "images" / f"{image_id}.jpg")
    gt = load_resize(root / "masks" / f"{image_id}.png", grayscale=True)
    rgb = load_resize(rgb_pred_dir / f"{image_id}_rgb_overlay.png")
    rgbd = load_resize(rgbd_pred_dir / f"{image_id}_rgbd_overlay.png")

    gt = ImageOps.colorize(gt, black="black", white="white")

    titles = ["Original", "Ground Truth", "RGB Prediction", "RGB-D Prediction"]
    images = [original, gt, rgb, rgbd]

    panel_w = 512 * 4
    panel_h = 512 + 50
    panel = Image.new("RGB", (panel_w, panel_h), "white")
    draw = ImageDraw.Draw(panel)

    for i, (title, img) in enumerate(zip(titles, images)):
        x = i * 512
        panel.paste(img, (x, 50))
        draw.text((x + 160, 15), title, fill="black")

    out_path = out_dir / f"{image_id}_comparison.png"
    panel.save(out_path)
    print(f"Saved: {out_path}")