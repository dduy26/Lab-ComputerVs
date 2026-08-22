# PHÂN TÍCH CHI TIẾT YÊU CẦU & CÂU HỎI BÀI TẬP (LAB-2-P2: CANNY EDGE DETECTOR)

---

## 📖 I. TỔNG QUAN VỀ BÀI TẬP LAB-2-P2

Bài tập Lab-2-Part 2 tập trung vào **Thuật toán phát hiện cạnh Canny (Canny Edge Detector)** - một trong những thuật toán phát hiện cạnh tối ưu và phổ biến nhất trong Xử lý ảnh số & Thị giác máy tính. 

Mục tiêu chính:
1. Nắm vững nền tảng lý thuyết toán học & 5 bước xử lý của thuật toán Canny.
2. Cài đặt thực hành và khảo sát sự ảnh hưởng của các tham số chính ($\sigma$, Ngưỡng Low, Ngưỡng High) sử dụng thư viện **OpenCV** và **Scikit-image**.
3. Ứng dụng Canny vào các bài toán thực tế: Phân đoạn đối tượng (Contour/Bounding Box), Nhận dạng hình học (Hough Line/Circle) và xử lý Video thời gian thực.

---

## 🔍 II. PHÂN TÍCH CHI TIẾT CÁC CÂU HỎI & NHIỆM VỤ CẦN LÀM (REQUIREMENTS BREAKDOWN)

### 📌 PHẦN I: NGUYÊN LÝ LÝ THUYẾT & SO SÁNH (THEORY & ANALYSIS)

#### 🔹 Câu I.1: Tìm hiểu thuật toán Canny & So sánh bộ lọc
- **I.1.a - 5 Bước chi tiết của thuật toán Canny:** Phân tích sâu từng bước toán học:
  1. *Làm mịn (Gaussian Smoothing):* Loại bỏ nhiễu bằng bộ lọc Gaussian 2D $G(x,y,\sigma)$.
  2. *Tính Gradient (Gradient Calculation):* Tính độ lớn (Magnitude) và hướng (Direction) của Gradient bằng toán tử Sobel ($K_x, K_y$).
  3. *Triệt tiêu phi cực đại (Non-Maximum Suppression - NMS):* Làm mỏng đường biên, chỉ giữ lại các điểm pixel là cực đại cục bộ theo hướng Gradient (làm tròn hướng về 0°, 45°, 90°, 135°).
  4. *Lọc ngưỡng kép (Double Thresholding):*Phân loại pixel cạnh thành Cạnh mạnh (Strong Edge $> T_{\text{high}}$), Cạnh yếu (Weak Edge $T_{\text{low}} \le pixel \le T_{\text{high}}$) và Non-edge ($< T_{\text{low}}$).
  5. *Theo dõi cạnh qua liên kết (Hysteresis Edge Tracking):* Giữ lại các cạnh yếu nếu chúng liên kết chuỗi với ít nhất một cạnh mạnh.
- **I.1.b - So sánh Canny với Sobel và Laplacian:**
  - *Sobel:* Bộ lọc Gradient đơn giản, nhạy cảm với nhiễu, đường cạnh bị dày (dày nhiều pixel).
  - *Laplacian / DoG:* Bộ lọc đạo hàm cấp 2, phát hiện điểm qua số 0 (Zero-crossing), cực kỳ nhạy cảm với nhiễu.
  - *Canny:* Tối ưu hóa 3 tiêu chí của Canny (Độ chính xác cao, Định vị cạnh tốt, Một phản hồi duy nhất cho mỗi cạnh).

#### 🔹 Câu I.2: Phân tích các tham số cốt lõi trong Canny
- **I.2.a - Tham số Sigma ($\sigma$) trong Gaussian Filter:**
  - Tác động của $\sigma$: $\sigma$ nhỏ $\rightarrow$ giữ chi tiết mịn nhưng còn nhiễu; $\sigma$ lớn $\rightarrow$ khử nhiễu tốt nhưng làm mờ cạnh và biến mất các chi tiết nhỏ.
- **I.2.b - Ngưỡng thấp (Low Threshold) và Ngưỡng cao (High Threshold):**
  - $T_{\text{high}}$ quyết định việc chọn các đường biên chắc chắn (Cạnh mạnh). $T_{\text{high}}$ quá cao làm đứt đoạn đường biên.
  - $T_{\text{low}}$ quyết định việc kết nối các đường biên yếu. $T_{\text{low}}$ quá thấp nạp thêm nhiều chi tiết nhiễu.
  - Tỷ lệ khuyến nghị giữa $T_{\text{high}} : T_{\text{low}}$ thường là $2:1$ hoặc $3:1$.

#### 🔹 Câu I.3: Đánh giá, So sánh & Ứng dụng thực tế
- **I.3.a - Đánh giá độ chính xác, tốc độ & chống nhiễu:** So sánh bảng chỉ số giữa Canny, Sobel, Prewitt, Roberts, Laplacian.
- **I.3.b - Lĩnh vực ứng dụng:** Xe tự lái (phát hiện làn đường), Y tế (phân đoạn ảnh X-quang/MRI), Công nghiệp (kiểm tra lỗi sản phẩm), OCR (nhận dạng chữ viết).
- **I.3.c - Ví dụ ứng dụng thực tế cụ thể:** Minh họa sơ đồ pipeline xử lý ảnh thực tế tích hợp Canny.

---

### 📌 PHẦN II: BÀI TẬP THỰC HÀNH & THỰC NGHIỆM (HANDS-ON IMPLEMENTATION)

#### 🔹 Câu II.1: Cài đặt thuật toán Canny Baseline
- Cần thực hiện: Đọc ảnh đầu vào, chuyển về ảnh mức xám (Grayscale), áp dụng hàm `cv2.Canny()` của OpenCV và `skimage.feature.canny()` của Scikit-image với các tham số mặc định.

#### 🔹 Câu II.2: Khảo sát biến đổi tham số & Trực quan hóa
- **Khảo sát Sigma ($\sigma = 1.0 \to 5.0$, bước nhảy 0.5):** Áp dụng bộ lọc Gaussian với 9 mức làm mờ khác nhau ($\sigma = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]$), sau đó chạy Canny.
- **Khảo sát Ngưỡng kép (Low / High Threshold):** Thử nghiệm ít nhất 5 cặp ngưỡng khác nhau (từ ngưỡng thấp tới ngưỡng cao).
- **Đo lường định lượng:** Đếm tổng số pixel cạnh được tìm thấy bằng `np.count_nonzero()`.
- **Trực quan hóa:** Hiển thị mạng lưới ảnh Subplot (2x3) so sánh đối chiếu trực quan với cấu hình mặc định (Baseline).

#### 🔹 Câu II.3: Thử nghiệm trên các loại ảnh khác nhau
- Thử nghiệm Canny trên 3 kịch bản ảnh thách thức:
  1. *Ảnh nhiều nhiễu (Noisy Image):* Nhiễu hạt muối tiêu hoặc nhiễu Gauss.
  2. *Ảnh độ tương phản thấp (Low Contrast Image):* Biên độ xám giữa vật thể và nền nhỏ.
  3. *Ảnh nhiều chi tiết/Hoa văn (Complex Texture Image):* Dễ gây nhiễu đường biên.
- Đưa ra nhận xét và giải pháp xử lý (ví dụ: tiền xử lý cân bằng ánh sáng CLAHE, lọc Bilateral).

#### 🔹 Câu II.4: Ứng dụng nâng cao (Kết hợp Canny với Contour & Hough Transform)
- **Tích hợp Contour Detection (`cv2.findContours` & `cv2.boundingRect`):** Trích xuất các đường viền khép kín từ ảnh Canny và vẽ khung bao (Bounding Box) quanh vật thể.
- **Tích hợp Hough Transform (`cv2.HoughLinesP` & `cv2.HoughCircles`):** Dùng cạnh Canny làm đầu vào để nhận dạng đường thẳng (làn đường, cạnh bàn) và đường tròn (đồng xu, bánh xe).

---

### 📌 PHẦN III: CÂU HỎI MỞ RỘNG & NÂNG CAO (ADVANCED TOPICS)

- **III.1 - Phương pháp đánh giá chất lượng cạnh:** Phân tích các độ đo định lượng như PSNR (Peak Signal-to-Noise Ratio), Pratt's Figure of Merit (FOM), SSIM, và so sánh với ảnh chuẩn (Ground Truth).
- **III.2 - Kỹ thuật nâng cao cải thiện Canny:** Khảo sát Adaptive Thresholding (tự động tính ngưỡng theo Otsu/Median), lọc giữ biên (Bilateral Filter), và tăng tốc xử lý GPU CUDA.
- **III.3 - Canny cho Ảnh màu (Color Images):** Phân tích 2 hướng giải quyết: Chạy Canny độc lập trên 3 kênh màu (R, G, B hoặc H, S, V) rồi hợp nhất (Logical OR) HOẶC tính Gradient tổng hợp từ ma trận Jacobian.
- **III.4 - Canny cho Video thời gian thực:** Phân tích quy trình xử lý theo khung hình (Frame-by-frame), kỹ thuật khử nhiễu thời gian (Temporal smoothing `cv2.addWeighted`), cắt vùng quan tâm (ROI), và tối ưu hóa FPS.

---

## 📌 III. PHÂN CÔNG NHIỆM VỤ 7 THÀNH VIÊN TRONG NHÓM

| STT | Thành viên | Phụ trách chi tiết | Tệp tin đảm nhận |
| :---: | :--- | :--- | :--- |
| **1** | **Đức** | **Phần I.1 (a + b) + III.1**: Lý thuyết 5 bước Canny, So sánh Sobel/Laplacian, Đánh giá chất lượng cạnh. | `docs/` |
| **2** | **Thọ** | **Phần I.2 (a + b) + III.2**: Phân tích tham số Sigma, Ngưỡng Low/High, Phương pháp nâng cao hiệu suất Canny. | `docs/` |
| **3** | **Thông** | **Phần I.3 (a + b + c) + III.3**: Ưu/Nhược điểm Canny, Lĩnh vực ứng dụng & Ví dụ, Canny cho Ảnh màu. | `docs/` |
| **4** | **Duy** | **Phần II.1 (OpenCV) + II.2 (OpenCV)**: Cài đặt OpenCV baseline, Khảo sát Sigma ($1\to 5$), Khảo sát Ngưỡng Low/High, Đếm `np.count_nonzero()`, Trực quan hóa đối chứng. | `notebook/4.py` |
| **5** | **Phước** | **Phần II.1 (Scikit-image) + II.2 (Scikit-image)**: Cài đặt & Khảo sát tham số Canny với Scikit-image. | `canny_skimage/` |
| **6** | **Vinh** | **Phần II.3**: Thử nghiệm Canny trên ảnh nhiễu, tương phản thấp và ảnh chi tiết phức tạp. | `docs/` |
| **7** | **Huy** | **Phần II.4 + III.4**: Kết hợp Canny với Contour (Bounding Box) & Hough Transform; Trả lời mở rộng Canny cho Video. | `notebook/4.py` & `docs/Câu hỏi mở rộng` |