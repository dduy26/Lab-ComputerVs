# PHÂN TÍCH CHI TIẾT YÊU CẦU & NHIỆM VỤ BÀI TẬP (LAB-1)

---

## 📖 I. TỔNG QUAN VỀ BÀI TẬP LAB-1

Bài tập Lab 1 tập trung vào **Các thao tác tiền xử lý ảnh cơ bản (Basic Image Preprocessing)** sử dụng hai thư viện nền tảng hàng đầu trong Python là **OpenCV (Open Source Computer Vision Library)** và **Pillow (PIL Fork)**.

Mục tiêu chính:
1. Nắm vững cách thiết lập môi trường lập trình và tích hợp thư viện xử lý ảnh.
2. Hiểu và thực hiện thành thạo các thao tác nạp (Load), hiển thị (Display), chuyển đổi chuẩn màu (Color space conversion), và lưu trữ (Save) ảnh dưới nhiều định dạng/mức nén khác nhau.
3. Thực hiện các phép biến đổi hình học cơ bản (Cắt xén ROI, Thay đổi kích thước theo tỷ lệ/cố định với các thuật toán nội suy điểm ảnh).
4. Thao tác vẽ đồ họa vector cơ bản và chèn văn bản đa ngôn ngữ có khử răng cưa lên hình ảnh.
5. Kiểm thử và đánh giá kết quả ở hai tầng: Mức mô hình/chức năng và mức toàn bộ luồng pipeline.

---

## 🔍 II. PHÂN TÍCH CHI TIẾT CÁC CÂU HỎI & NHIỆM VỤ CẦN LÀM (REQUIREMENTS BREAKDOWN)

### 📌 PHẦN I: NGUYÊN LÝ LÝ THUYẾT & NỀN TẢNG TOÁN HỌC

#### 🔹 Câu I.1: Cấu trúc ma trận ảnh số & Cơ chế nén dữ liệu
- **Cấu trúc ảnh xám và ảnh màu:** Phân tích ma trận 2D ($H \times W$) và tensor 3D ($H \times W \times 3$), kiểu dữ liệu `uint8` miền $[0, 255]$.
- **Sự khác biệt BGR vs RGB:** Nguyên nhân lịch sử của chuẩn BGR trong OpenCV và cách hoán chuyển sang RGB cho Matplotlib/Pillow để tránh bị sai lệch màu sắc.
- **Nguyên lý nén ảnh:**
  - Nén không mất mát (Lossless) trong định dạng PNG: Thuật toán lọc vi sai 2D kết hợp DEFLATE (LZ77 + Huffman).
  - Nén mất mát (Lossy) trong định dạng JPEG: Biến đổi Cosin rời rạc 2D-DCT, ma trận lượng tử hóa và phân tích hiện tượng nhiễu khối $8 \times 8$ ở chất lượng thấp.
  - Định dạng hiện đại WebP: So sánh hiệu quả nén và chất lượng cảm nhận so với JPEG và PNG.

#### 🔹 Câu I.2: Toán học chuyển đổi không gian màu
- **RGB sang Grayscale:** Xây dựng công thức trọng số sinh học ITU-R BT.601 ($Y = 0.299R + 0.587G + 0.114B$).
- **Không gian màu HSV:** Mô hình trụ/nón màu, định nghĩa các trục $H$ (Màu sắc), $S$ (Độ bão hòa), $V$ (Cường độ sáng), công thức toán học và giải pháp xử lý giá trị $H \in [0, 179]$ trong OpenCV.
- **Không gian màu CIE-Lab:** Trục độ chói $L^*$ và hai trục đối lập màu $a^*, b^*$, tính chất đồng đều cảm nhận (Perceptually Uniform).

#### 🔹 Câu I.3: Biến đổi hình học & Thuật toán nội suy
- **Cắt xén (Crop):** Bản chất phép trích xuất ma trận con (NumPy slicing) và cơ chế chia sẻ bộ nhớ (Memory view).
- **Thay đổi kích thước (Resize) & 4 Thuật toán nội suy:**
  - *Nearest Neighbor (`cv2.INTER_NEAREST`):* Tốc độ $O(1)$, hiện tượng răng cưa.
  - *Bilinear (`cv2.INTER_LINEAR`):* Nội suy 4 điểm lân cận, cân bằng tốc độ và độ mượt.
  - *Bicubic (`cv2.INTER_CUBIC`):* Nội suy đa thức bậc ba 16 điểm lân cận, sắc nét.
  - *Area (`cv2.INTER_AREA`):* Lấy tích phân diện tích, tối ưu tuyệt đối khi thu nhỏ (Downsampling).

---

### 📌 PHẦN II: BÀI TẬP THỰC HÀNH & THỰC NGHIỆM (HANDS-ON IMPLEMENTATION)

#### 🔹 Câu II.1: Pipeline Đọc, Hiển thị & Lưu trữ ảnh
- Viết code đọc file ảnh đầu vào (`meme.jpg`), xử lý an toàn khi file không tồn tại.
- Hiển thị ảnh đúng chuẩn màu RGB qua Matplotlib.
- Lưu ảnh sang các định dạng: PNG, WebP và JPEG ở 3 mức chất lượng (`quality = 95`, `quality = 30`, `quality = 10`), đo lường dung lượng file tương ứng.

#### 🔹 Câu II.2: Chuyển đổi không gian màu & Phân tách kênh
- Chuyển đổi ảnh gốc sang Grayscale, HSV và LAB.
- Phân tách ma trận từng kênh màu độc lập, hiển thị trực quan các thành phần $H, S, V$ và $L, a, b$.

#### 🔹 Câu II.3: Cắt xén (Crop) và Thay đổi kích thước (Resize)
- Cắt xén vùng khuôn mặt trung tâm của ảnh gốc.
- Thay đổi kích thước ảnh theo kích thước cố định ($300 \times 300$) và theo tỷ lệ ($50\%$, $150\%$) sử dụng các cờ nội suy thích hợp.

#### 🔹 Câu II.4: Đồ họa hình học & Thêm văn bản
- Vẽ các hình học cơ bản: Đường thẳng (`cv2.line`), hình chữ nhật (`cv2.rectangle`), hình tròn (`cv2.circle`) với màu sắc BGR và độ dày tùy chỉnh.
- Chèn văn bản (`cv2.putText`) sử dụng cờ khử răng cưa `cv2.LINE_AA`.
- Triển khai giải pháp chèn chữ tiếng Việt Unicode có dấu thông qua Pillow.

---

### 📌 PHẦN III: KIỂM THỬ, ĐÁNH GIÁ 2 TẦNG & CÂU HỎI MỞ RỘNG

- **Đánh giá Tầng 1 (Function Level):** Đo lường sai lệch PSNR/SSIM của ảnh nén JPEG chất lượng thấp so với ảnh gốc; phân tích hiện tượng méo tỷ lệ (Aspect ratio distortion).
- **Đánh giá Tầng 2 (Full-flow Level):** Đánh giá độ trễ xử lý (Execution time) của toàn bộ luồng pipeline từ khâu nạp ảnh đến khi lưu file, kiểm soát tràn bộ nhớ mảng `uint8`.
- **Câu hỏi mở rộng:** Kỹ thuật khử răng cưa Wu's Anti-aliasing trong đồ họa máy tính; Cơ chế xử lý ảnh dung lượng lớn/streaming I/O trong các hệ thống Big Data.

---

## 📌 III. PHÂN CÔNG NHIỆM VỤ 7 THÀNH VIÊN TRONG NHÓM

| STT | Thành viên | Phụ trách chi tiết | Tệp tin đảm nhận |
| :---: | :--- | :--- | :--- |
| **1** | **Đức** | **Phần I.1:** Cấu trúc ma trận ảnh số 2D/3D, quy chuẩn BGR vs RGB, nguyên lý nén mất mát và không mất mát (JPEG/PNG/WebP). | `docs/plan.md` |
| **2** | **Thọ** | **Phần I.2:** Cơ sở toán học chuyển đổi không gian màu: Grayscale ITU-R BT.601, hình nón HSV, không gian cảm nhận CIE-Lab. | `docs/plan.md` |
| **3** | **Thông** | **Phần I.3:** Lý thuyết biến đổi hình học Crop ROI, toán học ánh xạ ngược và 4 thuật toán nội suy điểm ảnh trong Resize. | `docs/plan.md` |
| **4** | **Duy** | **Phần II.1:** Cài đặt pipeline nạp, hiển thị và lưu ảnh đa định dạng, khảo sát dung lượng và tốc độ nén I/O. | `lab1.py`, `notebook/lab1.ipynb` |
| **5** | **Phước** | **Phần II.2:** Cài đặt thực nghiệm chuyển đổi không gian màu Grayscale, HSV, LAB và trích xuất kênh màu. | `notebook/lab1.ipynb` |
| **6** | **Vinh** | **Phần II.3 & II.4:** Thực nghiệm Crop, Resize đa tỷ lệ; vẽ đồ họa vector và chèn văn bản khử răng cưa `LINE_AA`. | `notebook/lab1.ipynb`, `main.py` |
| **7** | **Huy** | **Phần III:** Đánh giá 2 tầng (Chất lượng nén PSNR, độ trễ toàn luồng); Câu hỏi mở rộng Unicode và Streaming I/O ảnh lớn. | `notebook/lab1.ipynb`, `docs/plan.md` |