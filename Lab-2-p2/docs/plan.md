# KẾ HOẠCH THỰC HIỆN & PHÂN CÔNG TỔNG THỂ (LAB-2-P2)

---

## 📌 I. BẢNG PHÂN CÔNG 7 THÀNH VIÊN TRONG NHÓM

| STT | Thành viên | Phần phụ trách | Nhiệm vụ chính | Phạm vi tệp tin |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Đức** | I.1 (a + b) + III.1 | Lý thuyết 5 bước Canny, so sánh Sobel/Laplacian, đánh giá chất lượng cạnh. | `docs/` |
| **2** | **Thọ** | I.2 (a + b) + III.2 | Phân tích tham số Sigma, Ngưỡng Low/High, phương pháp nâng cao hiệu suất. | `docs/` |
| **3** | **Thông** | I.3 (a + b + c) + III.3 | Ưu/nhược điểm Canny, lĩnh vực ứng dụng, Canny cho ảnh màu. | `docs/` |
| **4** | **Duy** | **II.1 (OpenCV) + II.2 (OpenCV)** | **Canny OpenCV baseline, khảo sát Sigma $1.0to 5.0$ (bước 0.5), khảo sát Ngưỡng Low/High, đếm `np.count_nonzero()`, trực quan hóa đối chứng.** | **`notebook/4.py` (Phần II.1 & II.2)** |
| **5** | **Phước** | II.1 & II.2 (Scikit-image) | Thực hành Canny bằng Scikit-image, khảo sát tham số trên skimage. | `canny_skimage/` |
| **6** | **Vinh** | II.3 | Thử nghiệm Canny trên nhiều loại ảnh (nhiễu, tương phản thấp, chi tiết). | `docs/` |
| **7** | **Huy** | II.4 + III.4 | Kết hợp Contour & Hough Transform, trả lời câu hỏi Canny cho Video. | `notebook/4.py` (Phần II.4) & `docs/` |

---

## 📝 II. CHI TIẾT KẾ HOẠCH & MÃ NGUỒN CẦN THỰC HIỆN CỦA DUY (THÀNH VIÊN 4)

**File đảm nhận:** [`notebook/4.py`](file:///d:/X%E1%BB%AD%20L%C3%AD%20%E1%BA%A2nh/Lab/Lab-2-p2/notebook/4.py) 
**Nhiệm vụ trọng tâm:** Cài đặt thuật toán Canny bằng thư viện OpenCV, thực hiện 2 bài khảo sát tham số (Sigma & Ngưỡng kép), tính toán chỉ số định lượng pixel và trực quan hóa so sánh đối chứng.

---

### 🚀 CÁC BƯỚC THỰC HIỆN VÀ CHI TIẾT CODE CẦN LÀM:

#### 🔹 Bước 1: Khởi tạo Dữ liệu & Tiền xử lý (Image Preprocessing)
- **Mục tiêu:** Nạp ảnh đầu vào từ đĩa và chuyển đổi không gian màu BGR sang mức xám (Grayscale).
- **Code cần thực hiện:**
```python
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Đọc ảnh từ đường dẫn hiện tại hoặc thư mục data
img = cv2.imread("anh1.jpg")
if img is None:
    img = cv2.imread("data/input/meme.jpg")
if img is None:
    img = cv2.imread("../data/input/meme.jpg")

# Chuyển đổi sang ảnh xám
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
```

---

#### 🔹 Bước 2: Cài đặt Cấu hình Mặc định OpenCV (II.1 Baseline)
- **Mục tiêu:** Trích xuất cạnh Canny mặc định của OpenCV ($T_{text{low}} = 100, T_{text{high}} = 200$) trực tiếp từ ảnh xám (chưa qua Gaussian Blur thủ công) để làm **Baseline chuẩn đối chứng**.
- **Chỉ số cần đo:** Đếm số điểm ảnh cạnh bằng `np.count_nonzero()`.
- **Code cần thực hiện:**
```python
# Canny mặc định OpenCV (100, 200)
edge_default = cv2.Canny(gray, 100, 200)
count_default = np.count_nonzero(edge_default)

print(f"--- CANNY MẶC ĐỊNH OPENCV (100, 200) ---")
print(f"So diem anh canh (Pixel count): {count_default}n")
```

---

#### 🔹 Bước 3: Khảo sát Tham số Sigma Làm Mờ Gaussian ($1.0 rightarrow 5.0$, bước 0.5) (II.2.a)
- **Mục tiêu:** Áp dụng bộ lọc `cv2.GaussianBlur` với kích thước Kernel `(5, 5)` và duyệt qua danh sách $sigma = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]$ (bước nhảy 0.5). Quan sát sự suy giảm số lượng pixel cạnh khi $sigma$ tăng.
- **Code cần thực hiện:**
```python
sigmas = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]
edge_sigmas = []
count_sigmas = []

print("--- KHẢO SÁT SIGMA (1.0 -> 5.0 với bước nhảy 0.5) ---")
for s in sigmas:
    blur = cv2.GaussianBlur(gray, (5, 5), s)
    edge = cv2.Canny(blur, 100, 200)
    pixel_count = np.count_nonzero(edge)
   
    edge_sigmas.append(edge)
    count_sigmas.append(pixel_count)
    print(f"Sigma = {s} : {pixel_count} pixels")
print()
```

---

#### 🔹 Bước 4: Khảo sát Bộ Ngưỡng Thấp và Ngưỡng Cao (II.2.b)
- **Mục tiêu:** Cố định ảnh làm mờ tiêu chuẩn ($sigma = 2$), thử nghiệm 5 bộ ngưỡng $(T_{text{low}}, T_{text{high}})$ để đánh giá tác động từ việc nạp nhiều chi tiết nhiễu (ngưỡng thấp) đến đứt đoạn cạnh (ngưỡng cao).
- **Các cặp ngưỡng thử nghiệm:** `(30, 90)`, `(50, 150)`, `(100, 200)` [Mặc định], `(150, 250)`, `(200, 300)`.
- **Code cần thực hiện:**
```python
# Sử dụng ảnh làm mờ tiêu chuẩn với sigma = 2
blur_std = cv2.GaussianBlur(gray, (5, 5), 2)

threshold_pairs = [
    (30, 90),    # Ngưỡng rất thấp (Nhiều chi tiết & nhiễu)
    (50, 150),    # Ngưỡng thấp
    (100, 200),  # Ngưỡng mặc định OpenCV (Cân bằng)
    (150, 250),  # Ngưỡng cao
    (200, 300)    # Ngưỡng rất cao (Chỉ giữ cạnh mạnh)
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
```

---

#### 🔹 Bước 5: Trực Quan Hóa So Sánh Với Baseline Mặc Định (II.2.c)
- **Mục tiêu:** Sử dụng `matplotlib` để hiển thị 2 biểu đồ mạng lưới Subplot (2x5 cho Sigma và 2x3 cho Ngưỡng). Đặt ảnh Canny Mặc định ở vị trí đầu tiên `(2, 5, 1)` và các vị trí còn lại cho các kết quả khảo sát, kèm số lượng pixel thu được.
- **Code cần thực hiện:**
```python
# Biểu đồ 1: Khảo sát Sigma vs Baseline (Mạng lưới 2x5 cho 9 giá trị Sigma + 1 Baseline)
plt.figure(figsize=(18, 7))
plt.subplot(2, 5, 1)
plt.imshow(edge_default, cmap="gray")
plt.title(f"Mac Dinh (No Blur)n({count_default} px)")
plt.axis("off")

for idx, s in enumerate(sigmas):
    plt.subplot(2, 5, idx + 2)
    plt.imshow(edge_sigmas[idx], cmap="gray")
    plt.title(f"Sigma = {s}n({count_sigmas[idx]} px)")
    plt.axis("off")

plt.suptitle("KHAO SAT THAY DOI SIGMA (1.0 -> 5.0, buoc 0.5)", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()

# Biểu đồ 2: Khảo sát Ngưỡng Low/High vs Baseline
plt.figure(figsize=(15, 6))
plt.subplot(2, 3, 1)
plt.imshow(edge_default, cmap="gray")
plt.title(f"Mac Dinh (100, 200)n({count_default} px)")
plt.axis("off")

for idx, (low, high) in enumerate(threshold_pairs):
    plt.subplot(2, 3, idx + 2)
    plt.imshow(edge_thresholds[idx], cmap="gray")
    plt.title(f"Threshold ({low}, {high})n({count_thresholds[idx]} px)")
    plt.axis("off")

plt.suptitle("KHAO SAT NGUONG THAP VA NGUONG CAO", fontsize=14, fontweight="bold")
plt.tight_layout()
plt.show()
```

---

#### 🔹 Bước 6: Phối Hợp Tích Hợp Bài Tập II.4 (Cùng Thành viên 7 - Huy)
- **Mục tiêu:** Cung cấp ảnh Canny chuẩn (`blur_std`, `50, 150`) để Huy áp dụng thuật toán `cv2.findContours`, `cv2.boundingRect`, `cv2.HoughLinesP` và `cv2.HoughCircles` ngay trong cùng file `notebook/4.py`.

---

## 📊 III. TIÊU CHÍ HOÀN THÀNH & KẾT QUẢ ĐẦU RA (ACCEPTANCE CRITERIA)

1. **Thực thi không lỗi:** File `notebook/4.py` chạy thành công từ đầu đến cuối không phát sinh lỗi ngoại lệ (Exception).
2. **Số liệu đầy đủ:** In ra màn hình terminal đầy đủ số lượng pixel `np.count_nonzero()` cho từng trường hợp khảo sát.
3. **Trực quan rõ ràng:** Xuất ra 2 cửa sổ đồ họa hiển thị lưới Subplot 2x3 có chú thích đầy đủ tiêu đề và chỉ số pixel đối chứng.