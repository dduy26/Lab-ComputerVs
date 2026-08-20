# TIẾN ĐỘ THỰC HIỆN & AUDIT LOG - LAB-2-P2

Tài liệu cập nhật tiến độ công việc theo mô hình **Roadmap** và **Nhật ký Audit Kiểm thử (Audit Log)** cho bài thực hành Canny OpenCV.

---

## 1. Roadmap Tiến độ Dự án

###  Phước (Scikit-image) - `canny_skimage/`
- [DONE] Tạo thư mục riêng, chạy thực nghiệm 2 ảnh, lưu kết quả và báo cáo.

---

### 👤 Thành viên 4: Duy (OpenCV Canny - II.1 & II.2)
- [DONE] **II.1 - Canny OpenCV Baseline & Ứng dụng Thực tế**:
  - Đọc ảnh xám, tiền xử lý mờ Gaussian (`cv2.GaussianBlur`).
  - Phân đoạn đường biên bằng Contour & vẽ Bounding Box (`cv2.findContours`, `cv2.boundingRect`).
  - Nhận dạng hình học bằng phép biến đổi Hough Lines (`cv2.HoughLinesP`) & Hough Circles (`cv2.HoughCircles`).
- [DONE] **II.2.1 - Khảo sát Biến đổi Sigma (Làm mờ Gaussian)**:
  - Thử nghiệm 3 mức `sigma = 1, 2, 5`.
  - **Đánh giá định lượng**: Đếm chính xác số pixel cạnh bằng `np.count_nonzero()`.
- [DONE] **II.2.2 - Khảo sát Bộ Ngưỡng Kép (Threshold Low / High)**:
  - Thử nghiệm 3 bộ ngưỡng: `50-150` (Thấp/Nhạy), `100-200` (Mặc định/Cân bằng), `150-300` (Cao/Lọc mạnh).
  - **Đánh giá định lượng**: Đếm số pixel cạnh `np.count_nonzero()` tương ứng.
- [DONE] **II.2.3 - Trực quan hóa & So sánh Kết quả**:
  - Hiển thị lưới 2x3 cho khảo sát tham số (Sigma & Thresholds).
  - Hiển thị lưới 2x2 cho phần ứng dụng thực tế (Anh gốc, Canny, Contour, Hough).

---

## 2. Nhật ký Audit Kiểm thử (Audit Log)

| Audit ID | Người Audit | Nội dung kiểm thử | Cấu hình & Hàm thử nghiệm | Kết quả nghiệm thu & Thống kê | Trạng thái |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **AUDIT-01** | Duy (TV4) | Thống kê định lượng số pixel cạnh theo Sigma | `GaussianBlur(gray, (5,5), sigma)` với `sigma = 1, 2, 5` | Đếm thành công bằng `np.count_nonzero()`. Sigma càng lớn số pixel cạnh thu được càng giảm (do đường biên được làm mịn). | **PASS** |
| **AUDIT-02** | Duy (TV4) | Thống kê định lượng số pixel cạnh theo Threshold | Bộ ngưỡng: `50-150`, `100-200`, `150-300` | Ngưỡng `50-150` cho số lượng pixel cạnh cao nhất (nhiều nét), `150-300` cho ít pixel nhất (lọc sạch nhiễu). | **PASS** |
| **AUDIT-03** | Duy (TV4) | Hiển thị Lưới 2x3 So sánh Tham số | Matplotlib Subplots `(2, 3)` | Trực quan hóa rõ ràng sự khác biệt giữa 3 mức Sigma và 3 bộ ngưỡng Threshold. | **PASS** |
| **AUDIT-04** | Duy (TV4) | Kiểm thử Phân đoạn Contour & Hough Transform | `cv2.findContours`, `cv2.HoughLinesP`, `cv2.HoughCircles` | Nhận dạng và vẽ thành công Bounding Box đường biên, đoạn thẳng Hough Lines và đường tròn Hough Circles. | **PASS** |
| **AUDIT-05** | Duy (TV4) | Kiểm định mã nguồn `notebook/4.py` | Cấu trúc code trong `notebook/4.py` | Code ngắn gọn, phân chia rõ ràng giữa thống kê số liệu `np.count_nonzero()` và hiển thị đồ thị `plt.show()`. | **VERIFIED** |
