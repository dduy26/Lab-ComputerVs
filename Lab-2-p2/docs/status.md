# TIẾN ĐỘ THỰC HIỆN & ROADMAP DỰ ÁN - LAB-2-P2

Tài liệu cập nhật tiến độ công việc theo mô hình **Roadmap** cho tất cả 7 thành viên trong nhóm.

---

## 1. Roadmap Tiến độ 7 Thành viên

### 📖 Phần I & Phần III: Lý thuyết & Câu hỏi mở rộng
- [DONE] **Thành viên 1: Đức** (I.1 a+b, III.1) $\rightarrow$ Lý thuyết 5 bước Canny, so sánh Sobel/Laplacian, phương pháp đánh giá chất lượng cạnh.
- [DONE] **Thành viên 2: Thọ** (I.2 a+b, III.2) $\rightarrow$ Phân tích tham số Sigma, Ngưỡng Low/High, phương pháp nâng cao hiệu suất.
- [DONE] **Thành viên 3: Thông** (I.3 a+b+c, III.3) $\rightarrow$ Ưu/nhược điểm Canny, lĩnh vực ứng dụng, Canny cho ảnh màu.

---

### 💻 Phần II & III.4: Bài tập thực hành & Video
- [DONE] **Thành viên 4: Duy** (**II.1 OpenCV & II.2 OpenCV**):
  - Trích xuất cạnh Canny OpenCV mặc định baseline (`100, 200`).
  - Khảo sát mờ Gaussian với `sigma = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0]` (bước nhảy 0.5), đếm pixel `np.count_nonzero()`.
  - Khảo sát bộ ngưỡng Low/High `(30, 90)` đến `(200, 300)`.
  - Trực quan hóa Lưới 2x5 so sánh đối chứng với Canny Mặc định OpenCV.
  - *Tệp thực thi:* `notebook/4.py` (Phần II.1 & II.2).

- [DONE] **Thành viên 5: Phước** (II.1 & II.2 Scikit-image):
  - Hoàn thành thực hành Canny bằng `skimage.feature.canny` trong thư mục `canny_skimage/`.

- [DONE] **Thành viên 6: Vinh** (II.3):
  - Áp dụng Canny trên nhiều loại ảnh (ảnh nhiễu, ảnh độ tương phản thấp, ảnh nhiều chi tiết).
  - *Tài liệu kế hoạch:* `docs/plan.md` (Phần IV)

- [DONE] **Thành viên 7: Huy** (II.4 & III.4):
  - Kết hợp Canny với Phân đoạn Contour & Nhận dạng Hough Transform trong `notebook/4.py` (Phần II.4).
  - Trả lời câu hỏi mở rộng Canny cho Video trong `docs/Câu hỏi mở rộng`.
