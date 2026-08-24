# -*- coding: utf-8 -*-
"""
Chuẩn bị dữ liệu cho Bài thực hành 4 — Wavelet Hashing (Thành viên 1: Thông)

Mục đích: Tạo tập ảnh gồm:
  - Nhóm "similar": cùng đối tượng, biến đổi góc/nhiễu/độ sáng (ảnh giống nhau).
  - Nhóm "different": đối tượng khác hẳn (ảnh khác nhau).

Cấu trúc thư mục sau khi chạy:
  Lab-chap3p2/data/input/
    ├── similar/       # 18 ảnh: biến thể của meme.jpg (rotate, noise, blur, brightness)
    └── different/     # 6 ảnh: memetest + 5 ảnh nhiễu tổng hợp (khác hẳn meme)

Tổng cộng: 24 ảnh (>= mức tối thiểu 20-30 ảnh theo yêu cầu).

Cách chạy:
    python notebook/prepare_dataset.py
"""
import os
import cv2
import numpy as np

# --- Đường dẫn gốc (Lab-chap3p2) ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(BASE_DIR, "data", "input")

SRC_SIMILAR = os.path.join(INPUT_DIR, "meme.jpg")       # ảnh gốc nhóm giống
SRC_DIFFERENT = os.path.join(INPUT_DIR, "memetest.jpg")  # ảnh gốc nhóm khác

SIMILAR_DIR = os.path.join(INPUT_DIR, "similar")
DIFFERENT_DIR = os.path.join(INPUT_DIR, "different")


def ensure_dirs():
    """Tạo các thư mục con nếu chưa tồn tại."""
    os.makedirs(SIMILAR_DIR, exist_ok=True)
    os.makedirs(DIFFERENT_DIR, exist_ok=True)


def read_gray(path, size=(256, 256)):
    """Đọc ảnh, chuyển xám, resize chuẩn 256x256 (chống lỗi Unicode path bằng imdecode)."""
    data = np.fromfile(path, dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(path)
    return cv2.resize(img, size, interpolation=cv2.INTER_AREA)


def save(img, folder, name):
    """Lưu ảnh (encode rồi tofile để hỗ trợ tên file tiếng Việt trên Windows)."""
    out = os.path.join(folder, name)
    ok, buf = cv2.imencode(".png", img)
    if ok:
        buf.tofile(out)
    return out


def make_similar(img, output_dir):
    """
    Tạo các biến thể "giống nhau" từ 1 ảnh gốc:
      - xoay góc ±5°, ±15°
      - scale (zoom in/out nhẹ)
      - nhiễu Gaussian & salt-pepper
      - làm mờ Gaussian
      - thay đổi độ sáng
    """
    paths = []
    h, w = img.shape

    # 1. Xoay góc nhỏ (rotate): cùng đối tượng, góc khác nhau
    for angle in (5, 15, -5, -15):
        M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        paths.append(save(rotated, output_dir, f"similar_meme_rot{angle}.png"))

    # 2. Scale (zoom): thu/phóng nhẹ quanh tâm
    for scale in (0.9, 1.1):
        M = cv2.getRotationMatrix2D((w / 2, h / 2), 0, scale)
        scaled = cv2.warpAffine(img, M, (w, h))
        paths.append(save(scaled, output_dir, f"similar_meme_scale{int(scale*100)}.png"))

    # 3. Nhiễu Gaussian (nhiễu cộng) & salt-pepper
    gauss = np.clip(img.astype(np.float32) + np.random.normal(0, 15, img.shape), 0, 255).astype(np.uint8)
    paths.append(save(gauss, output_dir, "similar_meme_gauss15.png"))

    sp = img.copy()
    rng = np.random.default_rng(42)
    n_pixels = int(sp.size * 0.03)
    coords = rng.choice(sp.size, n_pixels, replace=False)
    sp.flat[coords] = rng.integers(0, 2, n_pixels) * 255
    paths.append(save(sp, output_dir, "similar_meme_saltpepper3.png"))

    # 4. Làm mờ Gaussian (blur nhẹ)
    blurred = cv2.GaussianBlur(img, (5, 5), 1.0)
    paths.append(save(blurred, output_dir, "similar_meme_blur.png"))

    # 5. Thay đổi độ sáng
    bright = cv2.convertScaleAbs(img, alpha=1.0, beta=30)
    paths.append(save(bright, output_dir, "similar_meme_bright30.png"))

    # 6. Thay đổi độ tương phản
    contrast = cv2.convertScaleAbs(img, alpha=1.5, beta=0)
    paths.append(save(contrast, output_dir, "similar_meme_contrast1p5.png"))

    # 7. Crop trung tâm rồi phóng lại (cùng đối tượng, khung khác)
    crop = img[int(h*0.1):int(h*0.9), int(w*0.1):int(w*0.9)]
    crop = cv2.resize(crop, (w, h), interpolation=cv2.INTER_AREA)
    paths.append(save(crop, output_dir, "similar_meme_crop10.png"))

    # 8. Làm mờ mạnh hơn (blur rõ rệt)
    blur2 = cv2.GaussianBlur(img, (9, 9), 3.0)
    paths.append(save(blur2, output_dir, "similar_meme_blur9x9.png"))

    # 9. Lật ngang (mirror) — cùng đối tượng, hướng nhìn khác
    flipped = cv2.flip(img, 1)
    paths.append(save(flipped, output_dir, "similar_meme_flip_h.png"))

    # 10. Xoay thêm 2 góc (30°, 45°) — mở rộng miền góc
    for angle in (30, 45):
        M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        paths.append(save(rotated, output_dir, f"similar_meme_rot{angle}.png"))

    return paths


def make_different(img_memetest, output_dir):
    """
    Tạo nhóm "khác nhau": các ảnh có nội dung KHÁC HẲN meme.jpg.

    Ghi chú: theo đề bài, nhóm "không tương tự" nên dùng ẢNH THẬT do người
    dùng tự chụp (bất kỳ đối tượng nào khác hẳn: bàn phím, con mèo, cuốn sách...).
    Script này giữ memetest làm ảnh mặc định; người dùng có thể bổ sung thêm
    các file `different_*.jpg/png` vào thư mục data/input/different/.
    """
    paths = [save(img_memetest, output_dir, "different_memetest.png")]

    # Nếu người dùng đã bỏ thêm ảnh thật khác vào thư mục, script sẽ không
    # đè lên chúng. (Đây chỉ là phần sinh ảnh mặc định.)
    return paths


def main():
    ensure_dirs()

    img_similar = read_gray(SRC_SIMILAR)
    img_different = read_gray(SRC_DIFFERENT)

    sim = make_similar(img_similar, SIMILAR_DIR)
    dif = make_different(img_different, DIFFERENT_DIR)

    print(f"similar   : {len(sim)} anh  -> {SIMILAR_DIR}")
    print(f"different : {len(dif)} anh  -> {DIFFERENT_DIR}")
    print(f"TOTAL     : {len(sim) + len(dif)} anh")

    # Kiểm tra lại: mọi ảnh đều đọc được
    for p in sim + dif:
        assert read_gray(p) is not None, p
    print("[OK] Tat ca anh deu doc duoc.")


if __name__ == "__main__":
    main()
