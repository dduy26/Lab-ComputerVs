import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. Đọc ảnh và chuyển sang ảnh mức xám
img = cv2.imread("anh1.jpg")
if img is None:
    img = cv2.imread("../data/input/meme.jpg")

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ##############################################################################
# THÀNH VIÊN 4: DUY - PHẦN II.1 (OPENCV) + PHẦN II.2 (OPENCV)
# ##############################################################################

# ==============================================================================
# PHẦN II.1: CẤU HÌNH MẶC ĐỊNH OPENCV (BASELINE)
# ==============================================================================
# OpenCV Canny mặc định với threshold1=100, threshold2=200 trực tiếp trên ảnh xám
edge_default = cv2.Canny(gray, 100, 200)
count_default = np.count_nonzero(edge_default)

print(f"--- CANNY MẶC ĐỊNH OPENCV (100, 200) ---")
print(f"So diem anh canh (Pixel count): {count_default}\n")

# ==============================================================================
# PHẦN II.2: THAY ĐỔI THAM SỐ VÀ QUAN SÁT KẾT QUẢ
# ==============================================================================

# ------------------------------------------------------------------------------
# 1. Thay đổi Sigma (từ 1 đến 5 với bước nhảy nhỏ: 1, 2, 3, 4, 5)
# ------------------------------------------------------------------------------
sigmas = [1, 2, 3, 4, 5]
edge_sigmas = []
count_sigmas = []

print("--- KHẢO SÁT SIGMA (1 -> 5 với bước nhảy nhỏ) ---")
for s in sigmas:
    blur = cv2.GaussianBlur(gray, (5, 5), s)
    edge = cv2.Canny(blur, 100, 200)
    pixel_count = np.count_nonzero(edge)
    edge_sigmas.append(edge)
    count_sigmas.append(pixel_count)
    print(f"Sigma = {s} : {pixel_count} pixels")
print()

# ------------------------------------------------------------------------------
# 2. Thay đổi Ngưỡng thấp (Low Threshold) và Ngưỡng cao (High Threshold)
# ------------------------------------------------------------------------------
# Sử dụng ảnh làm mờ chuẩn (sigma = 2)
blur_std = cv2.GaussianBlur(gray, (5, 5), 2)

threshold_pairs = [
    (30, 90),     # Ngưỡng rất thấp (Nhiều chi tiết & nhiễu)
    (50, 150),    # Ngưỡng thấp
    (100, 200),   # Ngưỡng mặc định OpenCV (Cân bằng)
    (150, 250),   # Ngưỡng cao
    (200, 300)    # Ngưỡng rất cao (Chỉ giữ cạnh mạnh, mất chi tiết)
]

edge_thresholds = []
count_thresholds = []

print("--- KHẢO SÁT NGƯỠNG THẤP VÀ NGƯỠNG CAO ---")
for low, high in threshold_pairs:
    edge = cv2.Canny(blur_std, low, high)
    pixel_count = np.count_nonzero(edge)
    edge_thresholds.append(edge)
    count_thresholds.append(pixel_count)
    print(f"Threshold ({low}, {high}) : {pixel_count} pixels")
print()

# ==============================================================================
# TRỰC QUAN HÓA SO SÁNH KẾT QUẢ (CỦA DUY)
# ==============================================================================

# Biểu đồ 1: Khảo sát bước nhảy Sigma từ 1 đến 5 (So sánh với Mặc định)
plt.figure(figsize=(15, 6))

plt.subplot(2, 3, 1)
plt.imshow(edge_default, cmap="gray")
plt.title(f"Mac Dinh (No Blur)\n({count_default} px)")
plt.axis("off")

for idx, s in enumerate(sigmas):
    plt.subplot(2, 3, idx + 2)
    plt.imshow(edge_sigmas[idx], cmap="gray")
    plt.title(f"Sigma = {s}\n({count_sigmas[idx]} px)")
    plt.axis("off")

plt.suptitle("KHAO SAT THAY DOI SIGMA (1 -> 5)", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()

# Biểu đồ 2: Khảo sát Bộ Ngưỡng Thấp và Ngưỡng Cao (So sánh với Mặc định)
plt.figure(figsize=(15, 6))

plt.subplot(2, 3, 1)
plt.imshow(edge_default, cmap="gray")
plt.title(f"Mac Dinh (100, 200)\n({count_default} px)")
plt.axis("off")

for idx, (low, high) in enumerate(threshold_pairs):
    plt.subplot(2, 3, idx + 2)
    plt.imshow(edge_thresholds[idx], cmap="gray")
    plt.title(f"Threshold ({low}, {high})\n({count_thresholds[idx]} px)")
    plt.axis("off")

plt.suptitle("KHAO SAT NGUONG THAP VA NGUONG CAO", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()

# ##############################################################################
# THÀNH VIÊN 7: HUY - PHẦN II.4 (KẾT HỢP CONTOUR & HOUGH TRANSFORM)
# ##############################################################################

canny_edges = cv2.Canny(blur_std, 50, 150)

# 1. Phân đoạn Contour & Bounding Box
contours, _ = cv2.findContours(canny_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
img_segmentation = img.copy()

for cnt in contours:
    if cv2.contourArea(cnt) > 50:
        cv2.drawContours(img_segmentation, [cnt], -1, (0, 255, 0), 2)
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img_segmentation, (x, y), (x + w, y + h), (0, 0, 255), 2)

# 2. Nhận dạng Hough Transform
img_hough = img.copy()
lines = cv2.HoughLinesP(canny_edges, 1, np.pi/180, threshold=50, minLineLength=40, maxLineGap=10)
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line.squeeze()
        cv2.line(img_hough, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)

circles = cv2.HoughCircles(blur_std, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=150, param2=30, minRadius=20, maxRadius=100)
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        cv2.circle(img_hough, (i[0], i[1]), i[2], (0, 0, 255), 2)

# 3. Hiển thị kết quả của Huy
plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.title("1. Anh goc")
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.axis("off")

plt.subplot(2, 2, 2)
plt.title("2. Canh Canny (50, 150)")
plt.imshow(canny_edges, cmap="gray")
plt.axis("off")

plt.subplot(2, 2, 3)
plt.title("3. Phan doan (Contour)")
plt.imshow(cv2.cvtColor(img_segmentation, cv2.COLOR_BGR2RGB))
plt.axis("off")

plt.subplot(2, 2, 4)
plt.title("4. Nhan dang (Hough)")
plt.imshow(cv2.cvtColor(img_hough, cv2.COLOR_BGR2RGB))
plt.axis("off")

plt.tight_layout()
plt.show()
