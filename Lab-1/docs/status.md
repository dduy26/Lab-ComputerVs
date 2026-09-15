# TIẾN ĐỘ THỰC HIỆN & ROADMAP DỰ ÁN - LAB-1

Tài liệu cập nhật tiến độ công việc theo mô hình **Roadmap** cho tất cả 7 thành viên trong nhóm cho bài thực hành **Lab-1: Các thao tác cơ bản với ảnh số & Tiền xử lý**.

---

## 1. Roadmap Tiến độ 7 Thành viên

### 📖 Phần I & Phần III: Lý thuyết & Câu hỏi mở rộng
- [DONE] **Thành viên 1: Đức** (I.1):
  - Cấu trúc ma trận ảnh số 2D/3D trong OpenCV (BGR) và Pillow (RGB).
  - Cơ chế nén mất mát (JPEG DCT) và không mất mát (PNG LZ77, WebP).
  - Phân tích đánh đổi giữa dung lượng lưu trữ vs chất lượng hình ảnh.
- [DONE] **Thành viên 2: Thọ** (I.2):
  - Cơ sở toán học chuyển đổi không gian màu: Grayscale ITU-R BT.601 ($Y = 0.299R + 0.587G + 0.114B$).
  - Không gian màu hình nón HSV (Hue, Saturation, Value) và chuẩn hóa góc trong OpenCV.
  - Không gian màu cảm nhận đồng đều CIE-Lab ($L^*a^*b^*$).
- [DONE] **Thành viên 3: Thông** (I.3):
  - Cơ sở toán học biến đổi hình học: Cắt xén ROI (NumPy slicing).
  - Toán học ánh xạ ngược và 4 thuật toán nội suy điểm ảnh (Nearest Neighbor, Bilinear, Bicubic, Area Interpolation).

---

### 💻 Phần II: Bài tập thực hành & Thực nghiệm
- [DONE] **Thành viên 4: Duy** (II.1):
  - Xây dựng pipeline đọc, hiển thị chuẩn màu RGB qua Matplotlib.
  - Lưu trữ đa định dạng: PNG, WebP và khảo sát JPEG ở 3 mức chất lượng (`quality = 95, 30, 10`).
  - Đo đạc dung lượng tệp và tốc độ I/O.
  - *Tệp thực thi:* `lab1.py`, `main.py`, `notebook/lab1.ipynb`.
- [DONE] **Thành viên 5: Phước** (II.2):
  - Chuyển đổi không gian màu Grayscale, HSV và LAB bằng `cv2.cvtColor`.
  - Phân tách 3 kênh màu độc lập và trực quan hóa bản đồ màu.
  - *Tệp thực thi:* `notebook/lab1.ipynb`.
- [DONE] **Thành viên 6: Vinh** (II.3 & II.4):
  - Cắt xén vùng khuôn mặt trung tâm và thay đổi kích thước theo tỷ lệ 50%, 150% và kích thước cố định 300x300.
  - Vẽ đồ họa hình học (Line, Rectangle, Circle) và chèn văn bản khử răng cưa `LINE_AA` cùng font Unicode tiếng Việt qua Pillow.
  - *Tệp thực thi:* `notebook/lab1.ipynb`, `main.py`.

---

### 📊 Phần III: Đánh giá 2 tầng & Mở rộng
- [DONE] **Thành viên 7: Huy** (III.1, III.2 & III.3):
  - Đánh giá Tầng 1: Đo lường chất lượng nén ảnh, phân tích hiện tượng block artifacts và méo tỷ lệ khung hình.
  - Đánh giá Tầng 2: Đo lường độ trễ toàn luồng pipeline ($12.4\text{ ms}$), quản lý an toàn mảng `uint8`.
  - Câu hỏi mở rộng: Phân tích thuật toán khử răng cưa Wu's Anti-aliasing và giải pháp streaming I/O cho ảnh kích thước siêu lớn.
  - *Tệp thực thi:* `notebook/lab1.ipynb`, `docs/plan.md`.