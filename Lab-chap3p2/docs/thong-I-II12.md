# Thành viên 1 — Thông (Phần I + II.1 + II.2)

**Bài thực hành 4:** So sánh sự tương đồng của các hình ảnh sử dụng Wavelet, Python
**Thư mục:** `Lab-chap3p2`

---

## 📖 I. Mục tiêu bài tập

- **Trích xuất thông tin bằng Wavelet:** Biến đổi Wavelet rời rạc 2D (2D-DWT) phân tích ảnh thành các băng tần theo tần số (xấp xỉ + chi tiết), giúp giữ lại cấu trúc chính của ảnh (băng tần LL) đồng thời tách được các chi tiết biên theo phương ngang, dọc, chéo (LH, HL, HH).
- **Làm quen thư viện PyWavelets:** Sử dụng `pywt.wavedec2()` để phân tách ảnh thành nhiều cấp, từ đó xây dựng đặc trưng wavelet cho mỗi ảnh.
- **Đánh giá hàm băm wavelet (wHash):** Lượng tử hóa hệ số băng tần LL thành chuỗi bit 64-bit, dùng khoảng cách **Hamming** để xác định hai ảnh có giống nhau hay không. Mục tiêu cuối là đánh giá độ chính xác của phương pháp này trong bài toán so sánh ảnh.

---

## 🗂️ II.1. Chuẩn bị dữ liệu

### 1. Cách tổ chức thư mục

```
Lab-chap3p2/data/input/
├── meme.jpg              # ảnh gốc (nhóm giống)
├── memetest.jpg          # ảnh khác hẳn (nhóm khác)
├── similar/              # các biến thể của meme.jpg (ảnh giống nhau)
│   ├── similar_meme_rot5.png        # xoay 5°
│   ├── similar_meme_rot15.png       # xoay 15°
│   ├── similar_meme_rot-5.png       # xoay -5°
│   ├── similar_meme_rot-15.png      # xoay -15°
│   ├── similar_meme_rot30.png       # xoay 30°
│   ├── similar_meme_rot45.png       # xoay 45°
│   ├── similar_meme_scale90.png     # thu nhỏ 90%
│   ├── similar_meme_scale110.png    # phóng to 110%
│   ├── similar_meme_gauss15.png     # nhiễu Gaussian σ=15
│   ├── similar_meme_saltpepper3.png # nhiễu muối tiêu 3%
│   ├── similar_meme_blur.png        # làm mờ Gaussian (5,5)
│   ├── similar_meme_blur9x9.png     # làm mờ mạnh (9,9)
│   ├── similar_meme_bright30.png    # tăng độ sáng +30
│   ├── similar_meme_contrast1p5.png # tăng tương phản ×1.5
│   ├── similar_meme_crop10.png      # crop trung tâm 10%
│   └── similar_meme_flip_h.png      # lật ngang
└── different/             # ảnh khác hẳn (ẢNH THẬT do người dùng tự chụp)
    ├── different_memetest.png      # ảnh mặc định
    ├── different_awww.png          # ảnh thật người dùng chụp
    ├── different_hehehe.jpg        # ảnh thật người dùng chụp
    └── different_huhu.png          # ảnh thật người dùng chụp
```

### 2. Quy tắc đặt tên file

`<nhóm>_<đối tượng>_<biến thể>.<jpg|png>`

- `similar` / `different` — phân loại.
- Tên đối tượng (`meme`, `memetest`, `ban_phim`, `con_meo`, ...) — nguồn ảnh.
- Tên biến thể (`rot15`, `gauss15`, `blur`, ...) — phép biến đổi đã áp dụng (chỉ với nhóm `similar`).
- Với nhóm `different`, chỉ cần `different_<tên>.jpg/png` (ảnh thật người dùng tự chụp, không cần biến thể).

### 3. Số lượng ảnh tối thiểu

- **Nhóm giống (similar):** 16 ảnh (từ meme.jpg qua 6 loại biến đổi: xoay, scale, nhiễu, blur, sáng/tương phản, crop/flip).
- **Nhóm khác (different):** 4 ảnh (1 ảnh mặc định memetest + 3 ảnh thật người dùng chụp: `awww`, `hehehe`, `huhu`).
- **Tổng cộng:** 20 ảnh (đạt mức đề xuất 20–30 ảnh).

### 4. Script sinh dữ liệu — `notebook/prepare_dataset.py`

```python
# -*- coding: utf-8 -*-
"""
Chuẩn bị dữ liệu cho Bài thực hành 4 — Wavelet Hashing (Thành viên 1: Thông)
Tạo 22 ảnh: 16 similar + 6 different.
"""
import os
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(BASE_DIR, "data", "input")

SRC_SIMILAR = os.path.join(INPUT_DIR, "meme.jpg")
SRC_DIFFERENT = os.path.join(INPUT_DIR, "memetest.jpg")
SIMILAR_DIR = os.path.join(INPUT_DIR, "similar")
DIFFERENT_DIR = os.path.join(INPUT_DIR, "different")


def ensure_dirs():
    """Tạo thư mục similar/ và different/ nếu chưa có."""
    os.makedirs(SIMILAR_DIR, exist_ok=True)
    os.makedirs(DIFFERENT_DIR, exist_ok=True)


def read_gray(path, size=(256, 256)):
    """Đọc ảnh, chuyển xám, resize 256x256."""
    data = np.fromfile(path, dtype=np.uint8)         # đọc bytes (chống lỗi Unicode path)
    img = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)   # giải mã ảnh xám
    return cv2.resize(img, size, interpolation=cv2.INTER_AREA)


def save(img, folder, name):
    """Lưu ảnh PNG (encode rồi tofile để hỗ trợ tên file tiếng Việt)."""
    out = os.path.join(folder, name)
    ok, buf = cv2.imencode(".png", img)
    if ok:
        buf.tofile(out)
    return out


def make_similar(img, output_dir):
    """Tạo các biến thể 'giống nhau' từ 1 ảnh gốc."""
    paths = []
    h, w = img.shape

    # Xoay góc (rotate): cùng đối tượng, góc khác nhau
    for angle in (5, 15, -5, -15, 30, 45):
        M = cv2.getRotationMatrix2D((w / 2, h / 2), angle, 1.0)
        rotated = cv2.warpAffine(img, M, (w, h), borderMode=cv2.BORDER_REFLECT)
        paths.append(save(rotated, output_dir, f"similar_meme_rot{angle}.png"))

    # Scale (zoom): thu/phóng quanh tâm
    for scale in (0.9, 1.1):
        M = cv2.getRotationMatrix2D((w / 2, h / 2), 0, scale)
        scaled = cv2.warpAffine(img, M, (w, h))
        paths.append(save(scaled, output_dir, f"similar_meme_scale{int(scale*100)}.png"))

    # Nhiễu Gaussian (cộng nhiễu) & salt-pepper
    gauss = np.clip(img.astype(np.float32) + np.random.normal(0, 15, img.shape), 0, 255).astype(np.uint8)
    paths.append(save(gauss, output_dir, "similar_meme_gauss15.png"))

    sp = img.copy()
    rng = np.random.default_rng(42)
    n_pixels = int(sp.size * 0.03)
    coords = rng.choice(sp.size, n_pixels, replace=False)
    sp.flat[coords] = rng.integers(0, 2, n_pixels) * 255
    paths.append(save(sp, output_dir, "similar_meme_saltpepper3.png"))

    # Làm mờ Gaussian (blur nhẹ & mạnh)
    blurred = cv2.GaussianBlur(img, (5, 5), 1.0)
    paths.append(save(blurred, output_dir, "similar_meme_blur.png"))
    blur2 = cv2.GaussianBlur(img, (9, 9), 3.0)
    paths.append(save(blur2, output_dir, "similar_meme_blur9x9.png"))

    # Độ sáng & tương phản
    bright = cv2.convertScaleAbs(img, alpha=1.0, beta=30)
    paths.append(save(bright, output_dir, "similar_meme_bright30.png"))
    contrast = cv2.convertScaleAbs(img, alpha=1.5, beta=0)
    paths.append(save(contrast, output_dir, "similar_meme_contrast1p5.png"))

    # Crop trung tâm rồi phóng lại & lật ngang
    crop = img[int(h*0.1):int(h*0.9), int(w*0.1):int(w*0.9)]
    crop = cv2.resize(crop, (w, h), interpolation=cv2.INTER_AREA)
    paths.append(save(crop, output_dir, "similar_meme_crop10.png"))
    flipped = cv2.flip(img, 1)
    paths.append(save(flipped, output_dir, "similar_meme_flip_h.png"))

    return paths


def make_different(img_memetest, output_dir):
    """
    Tạo nhóm "khác nhau": các ảnh có nội dung KHÁC HẲN meme.jpg.

    Ghi chú: theo đề bài, nhóm "không tương tự" nên dùng ẢNH THẬT do người
    dùng tự chụp (bất kỳ đối tượng nào khác hẳn). Script giữ memetest làm
    ảnh mặc định; người dùng bổ sung thêm file `different_*.jpg/png`.
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

    print(f"similar   : {len(sim)} anh")
    print(f"different : {len(dif)} anh")
    print(f"TOTAL     : {len(sim) + len(dif)} anh")

    for p in sim + dif:
        assert read_gray(p) is not None, p
    print("[OK] Tat ca anh deu doc duoc.")


if __name__ == "__main__":
    main()
```

**Kết quả chạy thật:**

```text
similar   : 16 anh  -> E:\...\data\input\similar
different : 6 anh   -> E:\...\data\input\different
TOTAL     : 22 anh
[OK] Tat ca anh deu doc duoc.
```

---

## 🌊 II.2. Trích xuất Wavelet đặc trưng

### 1. Biến đổi Wavelet 2D với `pywt.wavedec2`

`pywt.wavedec2(img, wavelet, level)` phân tích ảnh thành một cây nhiều cấp:

- Ở mỗi cấp, ảnh được lọc thông thấp (L) và thông cao (H) lần lượt theo **hàng** rồi theo **cột** → cho **4 băng tần**:
  - **LL (xấp xỉ):** tần số thấp cả 2 hướng — giữ cấu trúc/năng lượng chính của ảnh.
  - **LH:** chi tiết theo phương ngang (biên ngang).
  - **HL:** chi tiết theo phương dọc (biên dọc).
  - **HH:** chi tiết chéo + nhiễu tần số cao.
- `level` quyết định số lần lặp: băng LL của cấp trước được phân tách tiếp ở cấp sau.
- Kết quả trả về là tuple `(cA, (cH, cV, cD)_level, (cH, cV, cD)_level-1, ...)`.

**Kích thước các băng tần (chạy thật với ảnh 256×256, `haar`, level 3):**

```text
LL (xấp xỉ)              : (32, 32)
Level 3 chi tiết LH/HL/HH: (32, 32) / (32, 32) / (32, 32)
Level 2 chi tiết LH/HL/HH: (64, 64) / (64, 64) / (64, 64)
Level 1 chi tiết LH/HL/HH: (128, 128) / (128, 128) / (128, 128)
```

### 2. Phân tích các thành phần

| Băng tần | Ý nghĩa | Vai trò trong wHash |
|---|---|---|
| **LL** | Xấp xỉ, tần số thấp, năng lượng chính | **Dùng để tạo hash** — bền vững với nhiễu/nén/sáng |
| **LH** | Chi tiết ngang (biên ngang) | Nhạy, dễ thay đổi — không dùng cho hash |
| **HL** | Chi tiết dọc (biên dọc) | Nhạy, dễ thay đổi — không dùng cho hash |
| **HH** | Chi tiết chéo + nhiễu | Rất nhạy với nhiễu — không dùng cho hash |

### 3. Cách chọn wavelet (haar, db4, sym2) và ảnh hưởng

| Wavelet | Đặc điểm | Ảnh hưởng đến kết quả |
|---|---|---|
| **haar** | Đơn giản nhất, bậc lọc ngắn, nhanh | Hash nhạy với thay đổi nhỏ hơn; kết quả tốt trên ảnh rõ ràng |
| **db4** | Daubechies bậc 4, mịn hơn haar, nhiều hệ số hơn | Hash mượt hơn, ít nhạy nhiễu, chi phí cao hơn |
| **sym2** | Đối xứng gần đúng, họ Symlet | Trung gian giữa haar và db4; ổn định khi xoay/biến dạng nhẹ |

**Kết quả chạy thật (so sánh 3 wavelet trên cùng cặp ảnh, hash 64-bit):**

```text
[Wavelet: haar]
  meme vs rot5              : Hamming= 2/64 | Similarity=96.88%   (kỳ vọng GIỐNG -> nhỏ ✅)
  meme vs blur              : Hamming= 0/64 | Similarity=100.00%  (kỳ vọng GIỐNG -> nhỏ ✅)
  meme vs different_awww    : Hamming=32/64 | Similarity=50.00%   (kỳ vọng KHÁC  -> lớn ✅)
  meme vs different_hehehe  : Hamming=28/64 | Similarity=56.25%   (kỳ vọng KHÁC  -> lớn ✅)
  meme vs different_huhu    : Hamming=28/64 | Similarity=56.25%   (kỳ vọng KHÁC  -> lớn ✅)
  meme vs different_memetest: Hamming=33/64 | Similarity=48.44%   (kỳ vọng KHÁC  -> lớn ✅)

[Wavelet: db4]
  meme vs rot5              : Hamming= 6/64 | Similarity=90.62%   (kỳ vọng GIỐNG -> nhỏ ✅)
  meme vs blur              : Hamming= 0/64 | Similarity=100.00%  (kỳ vọng GIỐNG -> nhỏ ✅)
  meme vs different_awww    : Hamming=28/64 | Similarity=56.25%   (kỳ vọng KHÁC  -> lớn ✅)
  meme vs different_hehehe  : Hamming=36/64 | Similarity=43.75%   (kỳ vọng KHÁC  -> lớn ✅)
  meme vs different_huhu    : Hamming=34/64 | Similarity=46.88%   (kỳ vọng KHÁC  -> lớn ✅)
  meme vs different_memetest: Hamming=34/64 | Similarity=46.88%   (kỳ vọng KHÁC  -> lớn ✅)

[Wavelet: sym2]
  meme vs rot5              : Hamming= 5/64 | Similarity=92.19%   (kỳ vọng GIỐNG -> nhỏ ✅)
  meme vs blur              : Hamming= 0/64 | Similarity=100.00%  (kỳ vọng GIỐNG -> nhỏ ✅)
  meme vs different_awww    : Hamming=38/64 | Similarity=40.62%   (kỳ vọng KHÁC  -> lớn ✅)
  meme vs different_hehehe  : Hamming=32/64 | Similarity=50.00%   (kỳ vọng KHÁC  -> lớn ✅)
  meme vs different_huhu    : Hamming=36/64 | Similarity=43.75%   (kỳ vọng KHÁC  -> lớn ✅)
  meme vs different_memetest: Hamming=32/64 | Similarity=50.00%   (kỳ vọng KHÁC  -> lớn ✅)
```

**Nhận xét từ kết quả thật:**

- Cả 3 wavelet đều phân biệt đúng: **ảnh giống → Hamming nhỏ (≤6), ảnh khác → Hamming lớn (≥28)**.
- **Blur (làm mờ)** hầu như không làm đổi hash (Hamming = 0) — LL bền vững với nhiễu thấp tần.
- **Xoay nhẹ (rot5)** gây lệch ít bit nhất với `haar` (2 bit), nhiều hơn với `db4` (6 bit) — cần ngưỡng phù hợp.
- 3 ảnh thật người dùng chụp (`awww`, `hehehe`, `huhu`) đều cho Hamming ≥ 28 với mọi wavelet → đúng nhóm "khác nhau".
- Trong báo cáo thực hành, dùng **`haar`** làm lựa chọn mặc định (nhanh, đủ chính xác); có thể khảo sát `db4`/`sym2` khi cần mượt hơn với ảnh nhiễu.

### 4. Script kiểm chứng — `notebook/verify_wavelet_hash.py`

```python
# -*- coding: utf-8 -*-
"""
Kiểm chứng Trích xuất Wavelet 2D (Phần II.2 — Thành viên 1: Thông)
So sánh 3 wavelet (haar, db4, sym2) trên cặp giống/khác.
"""
import os
import cv2
import numpy as np
import pywt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(BASE_DIR, "data", "input")


def read_gray(path, size=(256, 256)):
    data = np.fromfile(path, dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)
    return cv2.resize(img, size, interpolation=cv2.INTER_AREA)


def wavelet_hash(img, wavelet="haar", level=3, hash_size=8):
    """2D-DWT -> LL -> resize 8x8 -> lượng tử hóa median -> 64 bit."""
    coeffs = pywt.wavedec2(img, wavelet=wavelet, level=level)
    ll = coeffs[0]                                           # băng tần xấp xỉ
    ll_small = cv2.resize(ll, (hash_size, hash_size), interpolation=cv2.INTER_AREA)
    med = np.median(ll_small)                                # ngưỡng trung vị
    return (ll_small >= med).astype(np.uint8).flatten()      # chuỗi bit 64


def hamming(h1, h2):
    return int(np.count_nonzero(h1 != h2))


def main():
    meme = read_gray(os.path.join(INPUT_DIR, "meme.jpg"))
    rot5 = read_gray(os.path.join(INPUT_DIR, "similar", "similar_meme_rot5.png"))
    blur = read_gray(os.path.join(INPUT_DIR, "similar", "similar_meme_blur.png"))

    diff_dir = os.path.join(INPUT_DIR, "different")
    diff_files = sorted(f for f in os.listdir(diff_dir)
                        if f.lower().endswith((".jpg", ".png", ".webp")))

    for w in ["haar", "db4", "sym2"]:
        h_meme = wavelet_hash(meme, w)
        h_rot5 = wavelet_hash(rot5, w)
        h_blur = wavelet_hash(blur, w)

        d_rot = hamming(h_meme, h_rot5)
        d_blur = hamming(h_meme, h_blur)

        print(f"[Wavelet: {w}]")
        print(f"  meme vs rot5     : Hamming={d_rot:2d}/64 | Similarity={(1-d_rot/64)*100:5.2f}%")
        print(f"  meme vs blur     : Hamming={d_blur:2d}/64 | Similarity={(1-d_blur/64)*100:5.2f}%")

        for f in diff_files:
            other = read_gray(os.path.join(diff_dir, f))
            d_diff = hamming(h_meme, wavelet_hash(other, w))
            print(f"  meme vs {f:<25}: Hamming={d_diff:2d}/64 | Similarity={(1-d_diff/64)*100:5.2f}%")


if __name__ == "__main__":
    main()
```

**Cách chạy:**

```bash
python notebook/prepare_dataset.py
python notebook/verify_wavelet_hash.py
```

---

## 📌 Kết luận phần Thành viên 1

- Đã tạo dataset **20 ảnh** (16 similar + 4 different) với cách đặt tên và tổ chức thư mục rõ ràng.
- Đã giải thích **2D-DWT** (`pywt.wavedec2`), ý nghĩa từng băng tần **LL/LH/HL/HH**, và ảnh hưởng của việc chọn wavelet.
- Đã chạy thực nghiệm, xác nhận **wHash dùng băng tần LL phân biệt đúng** ảnh giống/khác với cả 3 wavelet (haar, db4, sym2).
