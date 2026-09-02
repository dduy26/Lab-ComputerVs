# KẾ HOẠCH THỰC HIỆN VÀ TÍCH HỢP TOÀN BỘ (PLAN.MD) - LAB-CHAP3P2

---

## 🎯 MỤC TIÊU DỰ ÁN
Hoàn thiện toàn bộ báo cáo, mã nguồn và tệp Jupyter Notebook cho dự án **Lab-chap3p2: So sánh sự tương đồng của các hình ảnh sử dụng Wavelet Hash (wHash)** theo chuẩn cấu trúc thư mục của `Lab-2-p2` và định dạng `lab3.ipynb`.

---

## 🗺️ NGUYÊN TẮC VÀ WORKFLOW THỰC HIỆN
Tuân thủ nghiêm ngặt 7 bước workflow:
1. **Refine Requirement**: Cập nhật đề bài chi tiết vào `docs/require.md`.
2. **Plan**: Soạn thảo kế hoạch triển khai trong `docs/plan.md`.
3. **Theory Report**: Soạn thảo báo cáo lý thuyết đầy đủ 7 thành viên trong `docs/lythuyet.md`.
4. **Status Update**: Cập nhật trạng thái từng hạng mục trong `docs/status.md`.
5. **Code Consolidation**: Gộp toàn bộ mã nguồn xử lý của 7 thành viên vào `notebook/code.py` theo thứ tự từ 1 đến 7.
6. **Notebook Completion**: Tạo và chạy tệp `notebook/lab-chap3-p2.ipynb` với đầy đủ Markdown và kết quả thực thi output, biểu đồ, bảng biểu tương tự format `lab3.ipynb`.
7. **Testing & Evaluation**: Kiểm thử toàn bộ luồng chạy và đánh giá chỉ số.

---

## 👥 CHI TIẾT KẾ HOẠCH THEO THÀNH VIÊN (1 - 7)

### 1️⃣ Thành viên 1: Thông (Phần I + II.1 + II.2)
- **Mục tiêu**: Nền tảng Wavelet 2D, Chuẩn bị dữ liệu và Trích xuất băng tần.
- **Kế hoạch thực hiện**:
  - Tạo script `notebook/prepare_dataset.py` sinh 16 ảnh similar từ 1 ảnh gốc (`meme.jpg`) qua 6 biến đổi (xoay 5°-45°, scale 90-110%, nhiễu Gauss/ Muối tiêu, blur 5x5/9x9, bright/contrast, crop/flip) và 6 ảnh different (ảnh thật người dùng chụp).
  - Trích xuất 2D-DWT bằng `pywt.wavedec2(img, wavelet, level=3)`.
  - Phân tích 4 băng tần: LL (xấp xỉ), LH (biên ngang), HL (biên dọc), HH (biên chéo).
  - So sánh ảnh hưởng của các wavelet base (`haar`, `db4`, `sym2`).

### 2️⃣ Thành viên 2: Đức (Phần II.3 + II.4)
- **Mục tiêu**: Lượng tử hóa, Tạo mã băm nhị phân & So sánh Khoảng cách Hamming.
- **Kế hoạch thực hiện**:
  - Thử nghiệm 2 phương pháp lượng tử hóa: Median thresholding `(LL >= median)` vs Mean thresholding `(LL >= mean)` và `pywt.quantize`.
  - Duỗi thẳng ma trận $8 \times 8$ thành vector 64-bit và chuyển đổi sang chuỗi Hex (16 ký tự).
  - Cài đặt hàm `hamming_distance(h1, h2)`: `np.count_nonzero(b1 != b2)`.
  - Thử nghiệm so sánh 3 cặp ảnh thực nghiệm (Gốc vs memetest, Gốc vs Blur+Noise, Gốc vs Ảnh khác loại) và xuất bảng kết quả.

### 3️⃣ Thành viên 3: Duy (Phần II.5)
- **Mục tiêu**: Đánh giá chỉ số hiệu suất & Đường cong ROC / AUC.
- **Kế hoạch thực hiện**:
  - Thu thập kết quả dự đoán trên toàn bộ tập ảnh (Positive pairs vs Negative pairs).
  - Lập Ma trận Nhầm lẫn (Confusion Matrix): $TP, TN, FP, FN$.
  - Tính toán các chỉ số:
    - $\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$
    - $\text{Sensitivity (Recall)} = \frac{TP}{TP + FN}$
    - $\text{Specificity} = \frac{TN}{TN + FP}$
  - Sử dụng `sklearn.metrics.roc_curve` và `sklearn.metrics.auc` để tính điểm FPR, TPR và diện tích AUC.
  - Trực quan hóa và xuất biểu đồ `data/output/roc_curve_evaluation.png` bằng `matplotlib.pyplot`.

### 4️⃣ Thành viên 4: Thọ (Phần IV)
- **Mục tiêu**: Tham khảo quy trình Wavelet Hash & Code hoàn chỉnh OpenCV / PIL.
- **Kế hoạch thực hiện**:
  - Giải thích 3 bước: Biến đổi Wavelet 2D $\rightarrow$ Lượng tử hóa $\rightarrow$ Tạo mã băm.
  - Cài đặt pipeline đọc ảnh bằng OpenCV (`preprocess_image_cv2`) với `np.fromfile` + `cv2.imdecode` hỗ trợ tiếng Việt Unicode.
  - Cài đặt pipeline đọc ảnh bằng PIL (`preprocess_image_pil`) với `Image.open` + `convert('L')`.
  - Resize chuẩn hóa $256 \times 256$ và so sánh kết quả mã băm sinh ra từ 2 thư viện.

### 5️⃣ Thành viên 5: Vinh (Phần V)
- **Mục tiêu**: Triển khai Python & PyWavelets, Cải tiến code & So sánh các họ Wavelet.
- **Kế hoạch thực hiện**:
  - Xây dựng hàm `wavelet_hash_enhanced(img, wavelet, level, hash_size, norm_type)` hỗ trợ:
    - Điều chỉnh kích thước `hash_size` ($8 \times 8, 16 \times 16$).
    - Tối ưu hóa chỉ lấy băng tần xấp xỉ LL.
    - Chuẩn hóa hệ số (Min-Max normalization) trước khi phân ngưỡng.
    - Xử lý ngoại lệ an toàn cho file không tồn tại hoặc ảnh hỏng.
  - Thử nghiệm khảo sát 4 họ Wavelet (`haar`, `db4`, `sym4`, `coif2`) trên tập test, đo lường Accuracy (%) và Thời gian xử lý trung bình (ms/ảnh).

### 6️⃣ Thành viên 6: Huy (Phần III.1)
- **Mục tiêu**: Khảo sát các phương pháp băm Wavelet khác nhau.
- **Kế hoạch thực hiện**:
  - Cài đặt 3 phương pháp băm:
    - **PP1 (LL Hash)**: Băm dựa trên ma trận xấp xỉ $LL$ ($8 \times 8$).
    - **PP2 (Detail Energy Hash)**: Chia băng tần $LH, HL, HH$ thành 64 ô block, tính tổng năng lượng $E = \sum I_{ij}^2$ và nhị phân hóa.
    - **PP3 (Combined Hash)**: Ghép 45 bits từ LL và 19 bits từ Detail Energy để tạo hash 64-bit.
  - Đo lường và lập bảng so sánh 3 phương pháp về Accuracy, Execution Time (ms) và Khả năng phân biệt ảnh khác (Average Hamming distance).

### 7️⃣ Thành viên 7: Phước (Phần III.2)
- **Mục tiêu**: Xây dựng ứng dụng tìm kiếm hình ảnh dựa trên Wavelet Hash.
- **Kế hoạch thực hiện**:
  - Cài đặt ứng dụng CLI `notebook/search_app.py`.
  - Xây dựng hàm `build_database(image_dir, db_path)` duyệt thư mục ảnh và lưu file CSDL JSON.
  - Xây dựng hàm `search(query_path, db_path, top_k)` tính hash query, so sánh khoảng cách Hamming với DB, sắp xếp tăng dần và trả về Top K ảnh giống nhất.
  - Đánh giá thời gian xây dựng DB (~80ms), thời gian truy vấn (~99ms) và trực quan hóa kết quả tìm kiếm Top-K.

---

## 📂 THƯ MỤC VÀ CÁC TỆP SẼ ĐƯỢC TỔ CHỨC VÀ GỘP LẠI
```
Lab-chap3p2/
├── docs/
│   ├── require.md              # [DONE] Đề bài & phân công 7 thành viên
│   ├── plan.md                 # [DONE] Kế hoạch tổng thể
│   ├── lythuyet.md             # [IN PROGRESS] Báo cáo lý thuyết gộp đầy đủ 7 thành viên
│   ├── status.md               # [IN PROGRESS] Cập nhật tiến độ dự án
│   └── flow.md                 # Quy trình 7 bước
├── notebook/
│   ├── code.py                 # [IN PROGRESS] Gộp toàn bộ mã nguồn theo thứ tự 1-7
│   ├── prepare_dataset.py      # Sinh tập dữ liệu 22 ảnh
│   ├── search_app.py           # App tìm kiếm ảnh CLI
│   └── lab-chap3-p2.ipynb      # [IN PROGRESS] Notebook gộp hoàn chỉnh format tương tự lab3.ipynb
└── data/
    ├── input/                  # meme.jpg, memetest.jpg, similar/, different/
    └── output/                 # Các biểu đồ & kết quả xuất ra (.png, .json)
```
