# BÀI TẬP BÁO CÁO NHÓM - LAB-2-P2: THUẬT TOÁN PHÁT HIỆN CẠNH CANNY

---

## 📌 PHÂN CÔNG NHIỆM VỤ CHI TIẾT (7 THÀNH VIÊN)

### 📖 NGUYÊN LÝ LÝ THUYẾT & CÂU HỎI MỞ RỘNG (PHẦN I & PHẦN III)

#### 1. Thành viên 1: Đức $\rightarrow$ Phần I.1 (a + b) + III.1
- **I.1.a**: Tìm hiểu và giải thích chi tiết 5 bước của thuật toán Canny: Giảm nhiễu (Gaussian), Tính toán Gradient, Non-maximum Suppression (NMS), Ngưỡng kép (Double Thresholding), Theo dõi cạnh (Hysteresis).
- **I.1.b**: So sánh Canny với các thuật toán phát hiện cạnh khác như Sobel, Laplacian.
- **III.1**: Phương pháp đánh giá chất lượng của các cạnh được phát hiện bởi Canny.

#### 2. Thành viên 2: Thọ $\rightarrow$ Phần I.2 (a + b) + III.2
- **I.2.a**: Phân tích tham số Sigma trong Gaussian Filter và ảnh hưởng đến kết quả.
- **I.2.b**: Phân tích ảnh hưởng của Ngưỡng thấp (Low threshold) và Ngưỡng cao (High threshold).
- **III.2**: Các phương pháp nâng cao để cải thiện hiệu suất của Canny.

#### 3. Thành viên 3: Thông $\rightarrow$ Phần I.3 (a + b + c) + III.3
- **I.3.a**: So sánh Canny với các thuật toán khác về độ chính xác, tốc độ và khả năng xử lý nhiễu.
- **I.3.b**: Các lĩnh vực ứng dụng Canny phổ biến nhất trong thực tế.
- **I.3.c**: Ví dụ cụ thể về các ứng dụng thực tế của Canny Edge Detector.
- **III.3**: Phương pháp áp dụng Canny phát hiện cạnh trong ảnh màu (Color Images).

---

### 💻 BÀI TẬP THỰC HÀNH (PHẦN II)

#### 4. Thành viên 4: Duy $\rightarrow$ Phần II.1 (OpenCV) + Phần II.2 (OpenCV)
> **Phụ trách chính trong `notebook/4.py` (Phần II.1 & II.2)**
- **II.1**: Thực hiện thuật toán Canny bằng thư viện OpenCV (`cv2.Canny`).
- **II.2**: Thay đổi các tham số và quan sát kết quả:
  - Thay đổi Sigma làm mờ Gaussian ($1 \rightarrow 5$ bước nhảy 1), đếm số pixel cạnh `np.count_nonzero()`.
  - Thay đổi Ngưỡng thấp (Low) và Ngưỡng cao (High), đếm `np.count_nonzero()`.
  - So sánh kết quả thực nghiệm với các giá trị mặc định của OpenCV (`threshold1=100`, `threshold2=200`).

#### 5. Thành viên 5: Phước $\rightarrow$ Phần II.1 (Scikit-image) + Phần II.2 (Scikit-image)
- **II.1 & II.2**: Thực hiện thuật toán Canny bằng thư viện Scikit-image (`skimage.feature.canny`).
- Thay đổi tham số (sigma, low_threshold, high_threshold) và so sánh với giá trị mặc định trên Scikit-image.
- *Thực thi:* Thư mục `canny_skimage/`.

#### 6. Thành viên 6: Vinh $\rightarrow$ Phần II.3
- **II.3**: Áp dụng Canny cho các loại ảnh khác nhau (ảnh nhiều nhiễu, ảnh độ tương phản thấp, ảnh nhiều chi tiết). Đánh giá kết quả và rút ra kết luận.

#### 7. Thành viên 7: Huy $\rightarrow$ Phần II.4 + III.4
- **II.4**: Kết hợp Canny với các kỹ thuật khác:
  - Kết hợp thuật toán phân đoạn vùng tìm Contour & Bounding Box (`cv2.findContours`, `cv2.boundingRect`).
  - Kết hợp thuật toán nhận dạng hình dạng tìm đường thẳng & đường tròn (`cv2.HoughLinesP`, `cv2.HoughCircles`).
- **III.4**: Trả lời câu hỏi mở rộng: Phương pháp áp dụng Canny cho Video.