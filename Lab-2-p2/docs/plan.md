# KẾ HOẠCH THỰC HIỆN & PHÂN CÔNG TỔNG THỂ (LAB-2-P2)

---

## 📌 Bảng Phân công 7 Thành viên trong Nhóm

| STT | Thành viên | Phần phụ trách | Nhiệm vụ chính | Phạm vi tệp tin |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Đức** | I.1 (a + b) + III.1 | Lý thuyết 5 bước Canny, so sánh Sobel/Laplacian, đánh giá chất lượng cạnh. | `docs/` |
| **2** | **Thọ** | I.2 (a + b) + III.2 | Phân tích tham số Sigma, Ngưỡng Low/High, phương pháp nâng cao hiệu suất. | `docs/` |
| **3** | **Thông** | I.3 (a + b + c) + III.3 | Ưu/nhược điểm Canny, lĩnh vực ứng dụng, Canny cho ảnh màu. | `docs/` |
| **4** | **Duy** | **II.1 (OpenCV) + II.2 (OpenCV)** | **Canny OpenCV baseline, khảo sát Sigma $1\rightarrow 5$ bước nhảy 1, khảo sát Ngưỡng Low/High, đếm `np.count_nonzero()`, so sánh mặc định.** | **`notebook/4.py` (Phần II.1 & II.2)** |
| **5** | **Phước** | II.1 & II.2 (Scikit-image) | Thực hành Canny bằng Scikit-image, khảo sát tham số trên skimage. | `canny_skimage/` |
| **6** | **Vinh** | II.3 | Thử nghiệm Canny trên nhiều loại ảnh (nhiễu, tương phản thấp, chi tiết). | `docs/` |
| **7** | **Huy** | II.4 + III.4 | Kết hợp Contour & Hough Transform, trả lời câu hỏi Canny cho Video. | `notebook/4.py` (Phần II.4) |

---

## 📝 Chi tiết Kế hoạch của Duy (Thành viên 4)

1. **Khởi tạo Baseline Mặc định OpenCV**: `cv2.Canny(gray, 100, 200)` tính số pixel cạnh chuẩn đối chứng.
2. **Khảo sát Sigma (1 -> 5 với bước nhảy 1)**: Vòng lặp `sigma = [1, 2, 3, 4, 5]`, đếm `np.count_nonzero()`.
3. **Khảo sát Bộ Ngưỡng Low/High**: Thử nghiệm các bộ ngưỡng `(30, 90)`, `(50, 150)`, `(100, 200)`, `(150, 250)`, `(200, 300)`.
4. **Trực quan hóa So sánh Đối chứng**: Hiển thị lưới Subplot 2x3 đối chiếu kết quả khảo sát với Baseline mặc định OpenCV.