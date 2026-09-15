# PHÂN TÍCH CHI TIẾT YÊU CẦU & NHIỆM VỤ BÀI TẬP (LAB-2)

---

## 📖 I. TỔNG QUAN VỀ BÀI TẬP LAB-2

Bài tập Lab 2 tập trung vào **Xử lý ảnh trên miền không gian (Spatial Domain Image Processing)**, bao gồm hai kỹ thuật cốt lõi:
1. **Toán tử điểm ảnh (Point Operations):** Tác động độc lập lên từng pixel đơn lẻ (điều chỉnh độ sáng, độ tương phản, tạo ảnh âm bản, phân ngưỡng nhị phân và cân bằng lược đồ xám).
2. **Lọc không gian tuyến tính & phi tuyến tính (Spatial Filtering via Convolution):** Sử dụng các ma trận nhân chập hạt nhân (Kernel/Mask) để làm mịn ảnh, làm sắc nét ảnh, trích xuất biên cạnh và khử nhiễu.

Mục tiêu chính:
1. Nắm vững cơ sở toán học của các phép biến đổi cường độ xám $s = T(r)$ và bản chất phép tích chập không gian 2D ($g = f * h$).
2. Cài đặt và thực nghiệm các bộ lọc làm mịn (Box filter, Gaussian blur), làm sắc nét (Laplacian sharpening) và phát hiện biên (Toán tử vi phân Sobel, Prewitt).
3. Khảo sát các bộ lọc phi tuyến tính nâng cao: Lọc trung vị (Median filter) khử nhiễu muối tiêu và Lọc song phương (Bilateral filter) bảo toàn biên cạnh.
4. Đánh giá chất lượng xử lý ở hai tầng: Mức thuật toán/bộ lọc và mức toàn bộ luồng pipeline.

---

## 🔍 II. PHÂN TÍCH CHI TIẾT CÁC CÂU HỎI & NHIỆM VỤ CẦN LÀM (REQUIREMENTS BREAKDOWN)

### 📌 PHẦN I: NGUYÊN LÝ LÝ THUYẾT & NỀN TẢNG TOÁN HỌC

#### 🔹 Câu I.1: Toán tử điểm ảnh & Biến đổi lược đồ xám
- **Toán tử tuyến tính:** Hàm biến đổi $g(x,y) = \alpha \cdot f(x,y) + \beta$. Phân tích tác động của hệ số khuếch đại $\alpha$ (Tương phản) và hệ số dịch chuyển $\beta$ (Độ sáng) lên lược đồ Histogram. Cơ chế cắt cụt bão hòa (Saturation clipping).
- **Ảnh âm bản (Negative):** Phép biến đổi đảo ngược $s = 255 - r$ và ứng dụng trong chẩn đoán hình ảnh y tế.
- **Phân ngưỡng nhị phân (Thresholding):** Nguyên lý cắt ngưỡng đơn mức $T$ và thuật toán tối ưu hóa phương sai giữa hai lớp Otsu's Thresholding.
- **Biến đổi phi tuyến:** Biến đổi Logarit ($s = c\ln(1+r)$) và Hiệu chỉnh Gamma ($s = c \cdot r^\gamma$).

#### 🔹 Câu I.2: Lọc tuyến tính 2D & Tích chập không gian
- **Tích chập 2D (Spatial Convolution):** Định nghĩa toán học của phép nhân chập trượt kernel $h$ qua ảnh $f$.
- **Bộ lọc trung bình (Box/Mean Filter):** Kernel đồng nhất $1/K^2$, hiện tượng làm mờ phẳng và nhòe biên cạnh.
- **Bộ lọc Gaussian (Gaussian Blur):** Hàm mật độ phân phối chuẩn 2 chiều $G(x,y,\sigma)$, vai trò của độ lệch chuẩn $\sigma$ trong việc kiểm soát mức độ làm mờ mịn tự nhiên.
- **Làm sắc nét bằng toán tử Laplacian (Sharpening):** Đạo hàm bậc hai $\nabla^2 f$, nguyên lý Unsharp Masking và cấu trúc kernel làm sắc nét với tổng trọng số bằng $1$.

#### 🔹 Câu I.3: Trích xuất biên & Bộ lọc phi tuyến tính
- **Toán tử phát hiện biên Gradient Sobel & Prewitt:** Đạo hàm bậc nhất theo hai hướng $X, Y$, tính độ lớn Gradient Magnitude. So sánh khả năng chống nhiễu của Sobel (tích hợp Gaussian $[1, 2, 1]$) so với Prewitt.
- **Bộ lọc trung vị (Median Filter):** Thuật toán sắp xếp thứ tự trong cửa sổ trượt, lý do bộ lọc trung vị loại bỏ hoàn toàn nhiễu muối tiêu (Salt-and-pepper) mà không làm suy hao đường biên.
- **Bộ lọc song phương (Bilateral Filter):** Phân tích sự kết hợp giữa hàm suy giảm không gian $g_s$ và hàm suy giảm cường độ sáng $g_r$, cơ chế bảo toàn biên tuyệt đối khi làm mịn da/nền.

---

### 📌 PHẦN II: BÀI TẬP THỰC HÀNH & THỰC NGHIỆM (HANDS-ON IMPLEMENTATION)

#### 🔹 Câu II.1: Thực nghiệm Toán tử Điểm ảnh
- Điều chỉnh độ sáng ($\beta = +50$) và tăng độ tương phản ($\alpha = 1.5$) sử dụng `cv2.convertScaleAbs`.
- Tạo ảnh âm bản ($255 - \text{img}$).
- Cắt ngưỡng nhị phân với ngưỡng $T = 127$ (`cv2.threshold` cờ `THRESH_BINARY`).
- Lưu và trực quan hóa lưới ảnh đối sánh 5 khung hình (`part1_point.png`).

#### 🔹 Câu II.2: Khảo sát Bộ lọc Tuyến tính (Làm mịn & Sắc nét)
- Áp dụng bộ lọc làm mịn trung bình với kernel $7 \times 7$ (`cv2.blur`).
- Áp dụng bộ lọc Gaussian làm mờ mịn với kernel $7 \times 7$, $\sigma = 0$ (`cv2.GaussianBlur`).
- Áp dụng bộ lọc làm sắc nét bằng kernel Laplacian $3 \times 3$ (`cv2.filter2D`).
- Lưu và trực quan hóa lưới ảnh so sánh 4 khung hình (`part2_linear.png`).

#### 🔹 Câu II.3: Phát hiện Biên & Lọc Phi tuyến Nâng cao
- Tính toán đạo hàm Sobel theo hai hướng $X, Y$ và tổng hợp độ lớn biên bằng `cv2.magnitude`.
- Thiết kế kernel Prewitt $3 \times 3$ và tính độ lớn biên tương ứng.
- Khử nhiễu bằng lọc trung vị `cv2.medianBlur` với kích thước cửa sổ $5$.
- Làm mịn da giữ biên bằng `cv2.bilateralFilter` ($d=9, \sigma_r=75, \sigma_s=75$).
- Thiết kế kernel tùy biến Emboss (Dập nổi 3D) và lọc bằng `cv2.filter2D`.
- Lưu và hiển thị đồ thị so sánh 5 khung hình nâng cao (`part3_advanced.png`).

---

### 📌 PHẦN III: KIỂM THỬ, ĐÁNH GIÁ 2 TẦNG & CÂU HỎI MỞ RỘNG

- **Đánh giá Tầng 1 (Algorithm Level):** Đo lường và đối sánh định lượng giữa các bộ lọc: Độ sắc nét biên, mức độ làm mờ nhòe, khả năng khử nhiễu hạt và độ đo tương đồng cấu trúc SSIM.
- **Đánh giá Tầng 2 (Full-flow Level):** Đánh giá độ trễ thực thi (Runtime latency) từng thuật toán, xây dựng chuỗi tiền xử lý chuẩn mực cho bài toán Computer Vision: `Khử nhiễu Bilateral -> Tăng tương phản -> Trích xuất biên`.
- **Câu hỏi mở rộng:**
  - Định lý tích chập: So sánh miền không gian (Spatial domain) và miền tần số (Frequency domain qua 2D-FFT).
  - Kỹ thuật tách nhân (Separable Filter): Phân tích giảm độ phức tạp từ $O(K^2)$ xuống $O(2K)$ cho kernel Gaussian và Sobel.

---

## 📌 III. PHÂN CÔNG NHIỆM VỤ 7 THÀNH VIÊN TRONG NHÓM

| STT | Thành viên | Phụ trách chi tiết | Tệp tin đảm nhận |
| :---: | :--- | :--- | :--- |
| **1** | **Đức** | **Phần I.1:** Cơ sở toán học toán tử điểm ảnh: Hàm cường độ sáng, tuyến tính độ sáng/tương phản, âm bản, phân ngưỡng nhị phân và Otsu. | `docs/plan.md` |
| **2** | **Thọ** | **Phần I.2:** Bản chất toán học tích chập không gian 2D, bộ lọc Box filter, phân phối Gaussian 2D và toán tử đạo hàm bậc hai Laplacian làm sắc nét. | `docs/plan.md` |
| **3** | **Thông** | **Phần I.3:** Toán tử phát hiện biên Gradient Sobel/Prewitt; cơ chế lọc trung vị Median khử nhiễu muối tiêu và lọc song phương Bilateral bảo toàn biên. | `docs/plan.md` |
| **4** | **Duy** | **Phần II.1:** Cài đặt thực nghiệm toán tử điểm ảnh: Độ sáng, tương phản, âm bản, phân ngưỡng nhị phân và xuất lưới ảnh đối sánh `part1_point.png`. | `notebook/lab2.ipynb` |
| **5** | **Phước** | **Phần II.2:** Cài đặt thực nghiệm lọc tuyến tính: Lọc trung bình Box $7\times 7$, Gaussian blur $7\times 7$, làm sắc nét Laplacian và xuất `part2_linear.png`. | `notebook/lab2.ipynb` |
| **6** | **Vinh** | **Phần II.3 & II.4:** Thực nghiệm phát hiện biên Sobel vs Prewitt, lọc trung vị Median, lọc song phương Bilateral và thiết kế kernel Emboss 3D (`part3_advanced.png`). | `notebook/lab2.ipynb` |
| **7** | **Huy** | **Phần III:** Đánh giá 2 tầng (Chất lượng lọc, độ trễ toàn luồng); Câu hỏi mở rộng miền không gian vs miền tần số và tối ưu hóa Separable Filter. | `notebook/lab2.ipynb`, `docs/plan.md` |