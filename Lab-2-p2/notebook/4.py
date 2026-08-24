"""
BÀI THỰC HÀNH 3: CANNY EDGE DETECTOR - MÃ NGUỒN TỔNG HỢP (LAB-2-P2)
Tập hợp mã thực thi của cả 7 thành viên theo thứ tự:
- TV 3 (Thông): So sánh 3 thuật toán phát hiện cạnh (Sobel vs Laplacian vs Canny).
- TV 4 (Duy): Baseline OpenCV, Khảo sát Sigma (1.0 -> 5.0), Khảo sát Ngưỡng (Low/High), Đếm pixel.
- TV 5 (Phước): Thực hành Canny bằng Scikit-image (skimage.feature.canny).
- TV 6 (Vinh): Canny trên 3 loại ảnh (Nhiễu Gaussian, Tương phản thấp, Nhiều chi tiết).
- TV 7 (Huy): Kết hợp Canny với Phân đoạn Contour (Bounding Box) & Nhận dạng Hough (Lines/Circles).
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
import sys
import io
from pathlib import Path

# Cấu hình UTF-8 cho Terminal Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Cấu hình Matplotlib
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.unicode_minus'] = False

def imread_unicode(path, flags=cv2.IMREAD_COLOR):
    """Đọc ảnh hỗ trợ đường dẫn tiếng Việt có dấu trên Windows OS"""
    path_str = str(path)
    if not os.path.exists(path_str):
        return None
    try:
        data = np.fromfile(path_str, dtype=np.uint8)
        return cv2.imdecode(data, flags)
    except Exception:
        return cv2.imread(path_str, flags)

# ==============================================================================
# BƯỚC 0: NẠP DỮ LIỆU ẢNH VÀ TIỀN XỬ LÝ
# ==============================================================================
BASE_DIR = Path(__file__).parent.parent
img_path = BASE_DIR / "data" / "input" / "meme.jpg"

if not img_path.exists():
    img_path = Path("data/input/meme.jpg")

img = imread_unicode(img_path)

if img is None:
    # Tạo ảnh tổng hợp nếu không tìm thấy tệp ảnh
    img = np.zeros((400, 400, 3), dtype=np.uint8)
    cv2.rectangle(img, (50, 50), (200, 200), (255, 255, 255), -1)
    cv2.circle(img, (300, 300), 60, (255, 255, 255), -1)
    cv2.line(img, (50, 350), (350, 50), (255, 255, 255), 5)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

print("=" * 70)
print("TAI ANH THANH CONG!")
print(f"Kich thuoc anh goc: {img.shape}")
print("=" * 70)

# ==============================================================================
# MODULE 1: THÀNH VIÊN 3 (THÔNG) - SO SÁNH SOBEL VS LAPLACIAN VS CANNY
# ==============================================================================
print("\n--- THÀNH VIÊN 3 (THÔNG): SO SÁNH SOBEL, LAPLACIAN VA CANNY ---")

# 1. Sobel Magnitude
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
sobel_mag = cv2.magnitude(sobelx, sobely)
sobel_res = cv2.convertScaleAbs(sobel_mag)

# 2. Laplacian
lap_res = cv2.convertScaleAbs(cv2.Laplacian(gray, cv2.CV_64F))

# 3. Canny
canny_res = cv2.Canny(gray, 100, 200)

fig1 = plt.figure(figsize=(12, 10))
plt.subplot(2, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("1. Anh Goc (Original)")
plt.axis("off")

plt.subplot(2, 2, 2)
plt.imshow(sobel_res, cmap="gray")
plt.title("2. Sobel Detector (First Derivative)")
plt.axis("off")

plt.subplot(2, 2, 3)
plt.imshow(lap_res, cmap="gray")
plt.title("3. Laplacian Detector (Second Derivative)")
plt.axis("off")

plt.subplot(2, 2, 4)
plt.imshow(canny_res, cmap="gray")
plt.title("4. Canny Detector (Multi-stage Optimal)")
plt.axis("off")

plt.suptitle("SO SANH CAC THUAT TOAN PHAT HIEN CANH (THONG)", fontsize=14, fontweight="bold")
plt.tight_layout()

# ==============================================================================
# MODULE 2: THÀNH VIÊN 4 (DUY) - II.1 (OPENCV BASELINE) & II.2 (KHẢO SÁT THAM SỐ)
# ==============================================================================
print("\n--- THÀNH VIÊN 4 (DUY): BASELINE & KHẢO SÁT THAM SỐ CANNY OPENCV ---")

# 1. Canny Mặc định OpenCV (100, 200) - Baseline
edge_default = cv2.Canny(gray, 100, 200)
count_default = np.count_nonzero(edge_default)
print(f"[II.1 Baseline OpenCV] (100, 200): {count_default} pixels canh")

# 2. Khảo sát Sigma (1.0 -> 5.0, bước 0.5)
sigmas = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
edge_sigmas = []
count_sigmas = []

print("\n[II.2.a Khao sat Sigma lam mo Gaussian]:")
for s in sigmas:
    blur = cv2.GaussianBlur(gray, (5, 5), s)
    edge = cv2.Canny(blur, 100, 200)
    cnt = np.count_nonzero(edge)
    edge_sigmas.append(edge)
    count_sigmas.append(cnt)
    print(f"  - Sigma = {s:3.1f} : {cnt} pixels")

# 3. Khảo sát Ngưỡng Thấp & Ngưỡng Cao
blur_std = cv2.GaussianBlur(gray, (5, 5), 2.0)
threshold_pairs = [
    (30, 90),     # Ngưỡng thấp (Nhiều chi tiết & nhiễu)
    (50, 150),    # Ngưỡng trung bình thấp
    (100, 200),   # Ngưỡng mặc định OpenCV
    (150, 250),   # Ngưỡng cao
    (200, 300)    # Ngưỡng rất cao (Mất chi tiết)
]
edge_thresholds = []
count_thresholds = []

print("\n[II.2.b Khao sat Bo Nguong Low/High Threshold]:")
for low, high in threshold_pairs:
    edge = cv2.Canny(blur_std, low, high)
    cnt = np.count_nonzero(edge)
    edge_thresholds.append(edge)
    count_thresholds.append(cnt)
    print(f"  - Threshold ({low:3d}, {high:3d}) : {cnt} pixels")

# Trực quan hóa Khảo sát Duy (Subplot 2x5 cho Sigma & 2x3 cho Threshold)
fig2 = plt.figure(figsize=(16, 7))
plt.subplot(2, 5, 1)
plt.imshow(edge_default, cmap="gray")
plt.title(f"Baseline (No Blur)\n({count_default} px)")
plt.axis("off")

for idx, s in enumerate(sigmas):
    plt.subplot(2, 5, idx + 2)
    plt.imshow(edge_sigmas[idx], cmap="gray")
    plt.title(f"Sigma = {s}\n({count_sigmas[idx]} px)")
    plt.axis("off")

plt.suptitle("KHAO SAT SIGMA GAUSSIAN (1.0 -> 5.0, BUOC 0.5) - OPENCV", fontsize=14, fontweight="bold")
plt.tight_layout()

fig3 = plt.figure(figsize=(15, 6))
plt.subplot(2, 3, 1)
plt.imshow(edge_default, cmap="gray")
plt.title(f"Baseline (100, 200)\n({count_default} px)")
plt.axis("off")

for idx, (low, high) in enumerate(threshold_pairs):
    plt.subplot(2, 3, idx + 2)
    plt.imshow(edge_thresholds[idx], cmap="gray")
    plt.title(f"Threshold ({low}, {high})\n({count_thresholds[idx]} px)")
    plt.axis("off")

plt.suptitle("KHAO SAT BO NGUONG THAP VA NGUONG CAO - OPENCV", fontsize=14, fontweight="bold")
plt.tight_layout()

# ==============================================================================
# MODULE 3: THÀNH VIÊN 5 (PHƯỚC) - SCIKIT-IMAGE CANNY IMPLEMENTATION
# ==============================================================================
print("\n--- THÀNH VIÊN 5 (PHƯỚC): CANNY BẰNG SCIKIT-IMAGE ---")

try:
    from skimage import feature, color
    # skimage canny nhận giá trị pixel dải [0, 1] hoặc uint8
    gray_sk = gray.astype(np.float64) / 255.0
    
    edge_sk_def = feature.canny(gray_sk, sigma=1.0)
    edge_sk_s2 = feature.canny(gray_sk, sigma=2.0)
    edge_sk_low = feature.canny(gray_sk, sigma=1.0, low_threshold=0.05, high_threshold=0.2)
    edge_sk_high = feature.canny(gray_sk, sigma=1.0, low_threshold=0.2, high_threshold=0.5)

    fig4 = plt.figure(figsize=(14, 7))
    plt.subplot(2, 2, 1)
    plt.imshow(edge_sk_def, cmap="gray")
    plt.title("1. skimage Default (sigma=1.0)")
    plt.axis("off")

    plt.subplot(2, 2, 2)
    plt.imshow(edge_sk_s2, cmap="gray")
    plt.title("2. skimage Sigma=2.0 (Smoother)")
    plt.axis("off")

    plt.subplot(2, 2, 3)
    plt.imshow(edge_sk_low, cmap="gray")
    plt.title("3. skimage Low Threshold (0.05, 0.2)")
    plt.axis("off")

    plt.subplot(2, 2, 4)
    plt.imshow(edge_sk_high, cmap="gray")
    plt.title("4. skimage High Threshold (0.2, 0.5)")
    plt.axis("off")

    plt.suptitle("CANNY EDGE DETECTOR - SCIKIT-IMAGE (PHUOC)", fontsize=14, fontweight="bold")
    plt.tight_layout()
    print("  - Da thuc thi thanh cong skimage.feature.canny!")
except ImportError:
    print("  - Thu vien scikit-image chua duoc cai dat trong moi truong!")

# ==============================================================================
# MODULE 4: THÀNH VIÊN 6 (VINH) - II.3 CANNY TREN ĐA DẠNG ẢNH
# ==============================================================================
print("\n--- THÀNH VIÊN 6 (VINH): CANNY TREN CAC LOAI ANH KHAC NHAU ---")

# a) Ảnh nhiều nhiễu (Gaussian Noise)
noise = np.random.normal(0, 50, gray.shape).astype(np.float32)
img_noisy = np.clip(gray.astype(np.float32) + noise, 0, 255).astype(np.uint8)
blur_noisy = cv2.GaussianBlur(img_noisy, (7, 7), 2.5)
edges_noisy = cv2.Canny(blur_noisy, 50, 150)

# b) Ảnh tương phản thấp (Low Contrast)
img_low_contrast = np.clip((gray.astype(np.float32) - 128) * 0.2 + 128, 0, 255).astype(np.uint8)
blur_lc = cv2.GaussianBlur(img_low_contrast, (5, 5), 1.0)
edges_low_contrast = cv2.Canny(blur_lc, 15, 40)

# c) Ảnh nhiều chi tiết (Sharpened)
kernel_sharpen = np.array([[-1,-1,-1], [-1, 9,-1], [-1,-1,-1]])
img_detailed = cv2.filter2D(gray, -1, kernel_sharpen)
blur_det = cv2.GaussianBlur(img_detailed, (3, 3), 1.0)
edges_detailed = cv2.Canny(blur_det, 150, 250)

fig5 = plt.figure(figsize=(15, 10))
plt.subplot(3, 2, 1)
plt.imshow(img_noisy, cmap="gray")
plt.title("1a. Anh Nhieu (Gaussian Noise)")
plt.axis("off")

plt.subplot(3, 2, 2)
plt.imshow(edges_noisy, cmap="gray")
plt.title("1b. Canny (Blur 7x7, Sigma=2.5, Low=50, High=150)")
plt.axis("off")

plt.subplot(3, 2, 3)
plt.imshow(img_low_contrast, cmap="gray", vmin=0, vmax=255)
plt.title("2a. Anh Tuong Phan Thap (Low Contrast)")
plt.axis("off")

plt.subplot(3, 2, 4)
plt.imshow(edges_low_contrast, cmap="gray")
plt.title("2b. Canny (Low Threshold Rat Thap: 15, 40)")
plt.axis("off")

plt.subplot(3, 2, 5)
plt.imshow(img_detailed, cmap="gray")
plt.title("3a. Anh Nhieu Chi Tiet (Sharpened)")
plt.axis("off")

plt.subplot(3, 2, 6)
plt.imshow(edges_detailed, cmap="gray")
plt.title("3b. Canny (High Threshold Cao: 150, 250)")
plt.axis("off")

plt.suptitle("THUC HANH II.3: CANNY TREN CAC LOAI ANH THACH THUC (VINH)", fontsize=14, fontweight="bold")
plt.tight_layout()

# ==============================================================================
# MODULE 5: THÀNH VIÊN 7 (HUY) - II.4 KẾT HỢP CONTOUR & HOUGH TRANSFORM
# ==============================================================================
print("\n--- THÀNH VIÊN 7 (HUY): KẾT HỢP CONTOUR VA HOUGH TRANSFORM ---")

canny_base = cv2.Canny(blur_std, 50, 150)

# 1. Phân đoạn Contour & Bounding Box
contours, _ = cv2.findContours(canny_base, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
img_contour = img.copy()

for cnt in contours:
    if cv2.contourArea(cnt) > 50:
        cv2.drawContours(img_contour, [cnt], -1, (0, 255, 0), 2)
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img_contour, (x, y), (x + w, y + h), (255, 0, 0), 2)

# 2. Nhận dạng Hough Transform
img_hough = img.copy()
lines = cv2.HoughLinesP(canny_base, 1, np.pi/180, threshold=50, minLineLength=40, maxLineGap=10)
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = map(int, line.flatten()[:4])
        cv2.line(img_hough, (x1, y1), (x2, y2), (0, 255, 0), 2)

circles = cv2.HoughCircles(blur_std, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=150, param2=30, minRadius=20, maxRadius=100)
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        cv2.circle(img_hough, (i[0], i[1]), i[2], (0, 0, 255), 2)

fig6 = plt.figure(figsize=(12, 9))
plt.subplot(2, 2, 1)
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.title("1. Anh Goc")
plt.axis("off")

plt.subplot(2, 2, 2)
plt.imshow(canny_base, cmap="gray")
plt.title("2. Canny Edge Map (50, 150)")
plt.axis("off")

plt.subplot(2, 2, 3)
plt.imshow(cv2.cvtColor(img_contour, cv2.COLOR_BGR2RGB))
plt.title("3. Phan doan Contour & Bounding Box")
plt.axis("off")

plt.subplot(2, 2, 4)
plt.imshow(cv2.cvtColor(img_hough, cv2.COLOR_BGR2RGB))
plt.title("4. Nhan dang Hough Lines & Circles")
plt.axis("off")

plt.suptitle("THUC HANH II.4: KET HOP CANNY VOI CONTOUR VA HOUGH TRANSFORM (HUY)", fontsize=14, fontweight="bold")
plt.tight_layout()

print("\n" + "=" * 70)
print("HOAN THANH CHAY TOAN BO MA NGUON CUAR 7 THANH VIEN!")
print("=" * 70)

# Tránh treo terminal khi chạy script tự động
if os.environ.get('MPLBACKEND') != 'Agg':
    plt.show()
