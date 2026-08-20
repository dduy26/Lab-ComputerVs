import matplotlib.pyplot as plt
from skimage import io, color, feature
from pathlib import Path

# Đường dẫn tương đối (giả định chạy từ thư mục gốc của canny_skimage)
BASE = Path(__file__).parent.parent
INPUT_DIR = BASE / "data" / "input"
OUTPUT_DIR = BASE / "data" / "output"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Các bộ tham số cần thử (bao gồm mặc định)
params_list = [
    {"sigma": 1, "low": None, "high": None},   # default
    {"sigma": 1.5, "low": 10, "high": 50},
    {"sigma": 2, "low": 30, "high": 100},
    {"sigma": 1, "low": 50, "high": 150},
]

def process_one_image(img_path):
    img = io.imread(img_path)
    gray = color.rgb2gray(img) if img.ndim == 3 else img
    name = img_path.stem

    # Vẽ bảng so sánh
    fig, axes = plt.subplots(1, len(params_list)+1, figsize=(18, 4))
    axes[0].imshow(gray, cmap='gray')
    axes[0].set_title("Original")
    axes[0].axis('off')

    for i, p in enumerate(params_list):
        edges = feature.canny(gray, sigma=p["sigma"],
                              low_threshold=p["low"],
                              high_threshold=p["high"])
        # Tên file lưu
        if p["low"] is None:
            label = "default"
            suffix = "default"
        else:
            label = f"σ={p['sigma']}, L={p['low']}, H={p['high']}"
            suffix = f"sigma{p['sigma']}_low{p['low']}_high{p['high']}"
        # Lưu ảnh cạnh riêng
        save_path = OUTPUT_DIR / f"{name}_{suffix}.png"
        plt.imsave(save_path, edges, cmap='gray')
        print(f"Saved: {save_path}")
        # Hiển thị
        axes[i+1].imshow(edges, cmap='gray')
        axes[i+1].set_title(label)
        axes[i+1].axis('off')

    # Lưu bảng so sánh
    compare_path = OUTPUT_DIR / f"{name}_comparison.png"
    plt.tight_layout()
    plt.savefig(compare_path, dpi=150)
    print(f"Saved comparison: {compare_path}")
    plt.close()

# Chạy cho tất cả ảnh trong input
for f in INPUT_DIR.glob("*.jpg"):
    print(f"Processing: {f.name}")
    process_one_image(f)
print("Done! Check data/output/")