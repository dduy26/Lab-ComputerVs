# TIẾN ĐỘ THỰC HIỆN & ROADMAP DỰ ÁN - LAB-2

Tài liệu cập nhật tiến độ công việc theo mô hình **Roadmap** cho tất cả 7 thành viên trong nhóm cho bài thực hành **Lab-2: Xử lý ảnh trên miền không gian - Toán tử điểm ảnh & Các bộ lọc tích chập**.

---

## 1. Roadmap Tiến độ 7 Thành viên

### 📖 Phần I & Phần III: Lý thuyết & Câu hỏi mở rộng
- [DONE] **Thành viên 1: Đức** (I.1):
  - Cơ sở toán học toán tử điểm ảnh: Hàm biến đổi cường độ xám $s = T(r)$.
  - Phép biến đổi tuyến tính: Điều chỉnh độ sáng ($\beta$), độ tương phản ($\alpha$) và hàm cắt cụt bão hòa `cv2.convertScaleAbs`.
  - Ảnh âm bản ($255-I$), cắt ngưỡng nhị phân cố định và thuật toán phân ngưỡng tự động Otsu's Thresholding.
- [DONE] **Thành viên 2: Thọ** (I.2):
  - Bản chất toán học của tích chập không gian 2D ($g = f * h$).
  - Bộ lọc làm mịn trung bình Box filter $K \times K$ và hàm phân phối chuẩn Gaussian 2D ($G(x,y,\sigma)$).
  - Kỹ thuật làm sắc nét ảnh bằng toán tử đạo hàm bậc hai Laplacian ($\nabla^2 f$) và nguyên lý Unsharp Masking.
- [DONE] **Thành viên 3: Thông** (I.3):
  - Toán tử phát hiện biên Gradient bậc nhất: Sobel ($K_x, K_y$) vs Prewitt, tính độ lớn Gradient Magnitude.
  - Cơ chế lọc phi tuyến: Lọc trung vị Median filter khử triệt để nhiễu muối tiêu không làm mờ biên.
  - Lọc song phương Bilateral filter: Kết hợp suy giảm không gian và suy giảm mức xám, bảo toàn biên tuyệt đối.

---

### 💻 Phần II: Bài tập thực hành & Thực nghiệm
- [DONE] **Thành viên 4: Duy** (II.1):
  - Cài đặt thực nghiệm toán tử điểm ảnh: Tăng độ sáng $+50$, tương phản x1.5, tạo ảnh âm bản, cắt ngưỡng nhị phân $T=127$.
  - Trực quan hóa và xuất lưới ảnh đối sánh 5 khung hình `part1_point.png`.
  - *Tệp thực thi:* `notebook/lab2.ipynb`.
- [DONE] **Thành viên 5: Phước** (II.2):
  - Cài đặt bộ lọc làm mịn trung bình Box $7 \times 7$ và Gaussian blur $7 \times 7$.
  - Thiết kế kernel làm sắc nét Laplacian $3 \times 3$ qua `cv2.filter2D`.
  - Trực quan hóa và xuất lưới ảnh 4 khung hình `part2_linear.png`.
  - *Tệp thực thi:* `notebook/lab2.ipynb`.
- [DONE] **Thành viên 6: Vinh** (II.3 & II.4):
  - Trích xuất biên Sobel và Prewitt bằng `cv2.magnitude`.
  - Khử nhiễu muối tiêu bằng `cv2.medianBlur` và làm mịn da giữ biên bằng `cv2.bilateralFilter`.
  - Thiết kế kernel Emboss dập nổi 3D tùy biến, xuất lưới ảnh nâng cao `part3_advanced.png`.
  - *Tệp thực thi:* `notebook/lab2.ipynb`.

---

### 📊 Phần III: Đánh giá 2 tầng & Mở rộng
- [DONE] **Thành viên 7: Huy** (III.1, III.2 & III.3):
  - Đánh giá Tầng 1: Đối sánh chất lượng lọc, khả năng bảo toàn biên và độ mờ nhòe giữa các bộ lọc.
  - Đánh giá Tầng 2: Đo lường độ trễ toàn luồng (Runtime latency) từng toán tử và xây dựng pipeline chuẩn hóa cho Computer Vision.
  - Câu hỏi mở rộng: So sánh miền không gian vs miền tần số 2D-FFT và kỹ thuật tách nhân Separable Filter giảm độ phức tạp từ $O(K^2)$ xuống $O(2K)$.
  - *Tệp thực thi:* `notebook/lab2.ipynb`, `docs/plan.md`.