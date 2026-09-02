# PHÂN TÍCH CHI TIẾT YÊU CẦU & CÂU HỎI BÀI TẬP (LAB-CHAP3P2)

---

## 📖 I. TỔNG QUAN VỀ BÀI TẬP LAB-CHAP3P2

**Bài thực hành 4:** So sánh sự tương đồng của các hình ảnh sử dụng Wavelet, Python (`Lab-chap3p2`)

Mục tiêu chính:
1. **Trích xuất thông tin bằng biến đổi Wavelet:** Nắm vững biến đổi Wavelet rời rạc 2D (2D DWT) để phân tách hình ảnh thành các băng tần tần số (LL, LH, HL, HH).
2. **Thực hành với PyWavelets (`pywt`):** Sử dụng các hàm biến đổi wavelet rời rạc như `pywt.wavedec2()`, `pywt.dwt2()`, `pywt.quantize()` trong Python.
3. **Mã băm cảm nhận (Perceptual Wavelet Hash - wHash):** Lượng tử hóa các hệ số Wavelet để tạo mã băm nhị phân 64-bit và so sánh độ tương đồng bằng khoảng cách Hamming.
4. **Đánh giá & Khảo sát:** Đo lường hiệu suất (Accuracy, Sensitivity, Specificity, ROC curve, AUC), khảo sát các họ Wavelet (`haar`, `db4`, `sym4`, `coif2`), so sánh các phương pháp băm khác nhau (LL, Detail Energy, Combined) và xây dựng ứng dụng tìm kiếm ảnh.

---

## 👥 II. PHÂN CÔNG NHIỆM VỤ CHI TIẾT DÀNH CHO 7 THÀNH VIÊN

| STT | Thành viên | Phụ trách chi tiết các phần | Nội dung công việc |
| :---: | :--- | :--- | :--- |
| **1** | **Thông** | **Phần I + II.1 + II.2** | Tổng quan mục tiêu; Chuẩn bị dữ liệu (16 similar + 6 different, cấu trúc thư mục, quy tắc đặt tên, script generation); Trích xuất Wavelet 2D (`pywt.wavedec2`), phân tích 4 băng tần (LL, LH, HL, HH) và chọn loại wavelet (`haar`, `db4`, `sym2`). |
| **2** | **Đức** | **Phần II.3 + II.4** | Quá trình lượng tử hóa hệ số (`pywt.quantize` và tự viết), chọn ngưỡng (Median/Mean), tạo mã nhị phân bit 0/1; Giải thích khoảng cách Hamming $\sum(\text{bit1} \neq \text{bit2})$, ngưỡng tương đồng ($\le 10\%$), thực nghiệm trên 3 cặp ảnh. |
| **3** | **Duy** | **Phần II.5 + Biểu đồ** | Đánh giá chỉ số hiệu suất: Accuracy, Sensitivity (Recall), Specificity, Ma trận Nhầm lẫn (Confusion Matrix); Đường cong ROC và ý nghĩa AUC, hướng dẫn vẽ bằng `sklearn.metrics.roc_curve` & `matplotlib`. |
| **4** | **Thọ** | **Phần IV + Code OpenCV/PIL** | Giải thích chi tiết 3 bước của Wavelet Hash (Phân tích tần số $\rightarrow$ Lượng tử hóa $\rightarrow$ Mã băm nhị phân); Viết code hoàn chỉnh xử lý ảnh đầu vào bằng cả OpenCV (`cv2.imread`/`imdecode`) và PIL (`Image.open`), chuyển grayscale, resize $256 \times 256$. |
| **5** | **Vinh** | **Phần V + Cải tiến code** | Triển khai Python & PyWavelets, cải tiến code (thêm `hash_size`, xử lý ngoại lệ, tối ưu chỉ lấy băng LL, chuẩn hóa hệ số trước lượng tử); Khảo sát so sánh các loại Wavelet (`haar`, `db4`, `sym4`, `coif2`) về độ chính xác và tốc độ. |
| **6** | **Huy** | **Phần III.1** | Khảo sát các phương pháp băm Wavelet khác nhau: PP1 (Hệ số xấp xỉ LL), PP2 (Năng lượng chi tiết LH/HL/HH), PP3 (Kết hợp LL + Detail Energy); So sánh trên cùng dataset về Accuracy, thời gian xử lý và khả năng phân biệt. |
| **7** | **Phước** | **Phần III.2** | Xây dựng ứng dụng tìm kiếm hình ảnh dựa trên Wavelet Hash: Thiết kế CLI app, xây dựng CSDL hash (lưu file JSON), chức năng tìm kiếm query vs DB bằng khoảng cách Hamming, trả về Top K ảnh giống nhất và đánh giá tốc độ/độ chính xác. |

---

## 🔍 III. NỘI DUNG CHI TIẾT CÁC PHẦN BÀI LÀM

### 📌 PHẦN I: MỤC TIÊU BÀI TẬP
- Tổng quan biến đổi Wavelet rời rạc 2D trong trích xuất đặc trưng hình ảnh.
- Làm quen thư viện `PyWavelets` (`pywt`) trong xử lý ảnh Python.
- Đánh giá khả năng của thuật toán mã băm Wavelet (wHash) trong bài toán so sánh độ tương đồng hình ảnh.

### 📌 PHẦN II: BÀI TOÁN CỤ THỂ
1. **Chuẩn bị dữ liệu (II.1):**
   - Tổ chức thư mục `data/input/similar/` và `data/input/different/`.
   - Quy tắc đặt tên file: `<nhóm>_<đối tượng>_<biến thể>.<ext>`.
   - Đề xuất số lượng ảnh: 20-30 ảnh (16 ảnh similar từ các phép biến đổi xoay, scale, noise, blur, bright/contrast, crop/flip + 6 ảnh different từ ảnh chụp thực tế).
2. **Trích xuất Wavelet đặc trưng (II.2):**
   - Giải thích phép biến đổi 2D DWT qua `pywt.wavedec2()`.
   - Phân tích vai trò của 4 băng tần: LL (xấp xỉ tần số thấp), LH (chi tiết ngang), HL (chi tiết dọc), HH (chi tiết chéo).
   - Ảnh hưởng của việc chọn loại wavelet (`haar`, `db4`, `sym2`).
3. **Tạo mã băm Wavelet (II.3):**
   - Giải thích bản chất lượng tử hóa (Quantization): biến hệ số thực thành bit 0/1.
   - So sánh chọn ngưỡng theo Median (Trung vị) vs Mean (Trung bình) vs `pywt.quantize`.
   - Chuyển ma trận lượng tử thành chuỗi nhị phân 64-bit và mã Hex 16 ký tự.
4. **So sánh hàm băm (II.4):**
   - Giải thích công thức khoảng cách Hamming: $D_{\text{Hamming}} = \sum (b_1 \neq b_2)$.
   - Thiết lập ngưỡng quyết định tương đồng ($\le 10\%$ độ dài hash, tức $\le 6$ bits cho hash 64-bit).
   - Minh họa kết quả số liệu trên 3 cặp ảnh mẫu.
5. **Đánh giá hiệu suất & ROC (II.5):**
   - Lập Confusion Matrix ($TP, TN, FP, FN$).
   - Công thức & Ý nghĩa: Accuracy, Sensitivity (Recall), Specificity.
   - Vẽ đường cong ROC bằng `sklearn.metrics.roc_curve` và `matplotlib.pyplot`, giải thích chỉ số AUC.

### 📌 PHẦN III: BÀI TẬP NÂNG CAO
1. **Khảo sát các phương pháp băm Wavelet (III.1):**
   - PP1: Băm dựa trên hệ số xấp xỉ $LL$ ($8 \times 8$).
   - PP2: Băm dựa trên Năng lượng hệ số chi tiết $LH, HL, HH$ (Block Detail Energy).
   - PP3: Băm kết hợp $LL + \text{Detail Energy}$ (ví dụ 45 bit LL + 19 bit Energy).
   - Bảng so sánh 3 phương pháp về Accuracy, Execution Time (ms), Discrimination.
2. **Xây dựng ứng dụng tìm kiếm hình ảnh (III.2):**
   - Thiết kế ứng dụng CLI (`search_app.py`).
   - Xây dựng database JSON lưu trữ mã băm cho toàn bộ thư mục ảnh.
   - Truy vấn ảnh Query, tính khoảng cách Hamming, xếp hạng và trả về Top K kết quả giống nhất.
   - Đánh giá thời gian truy vấn và độ chính xác.

### 📌 PHẦN IV: THAM KHẢO & CODE HOÀN CHỈNH (OPENCV / PIL)
- Giải thích 3 bước cốt lõi: Phân tích tần số $\rightarrow$ Lượng tử hóa $\rightarrow$ Tạo băm nhị phân.
- Cài đặt quy trình xử lý ảnh đầu vào hoàn chỉnh hỗ trợ cả OpenCV (`cv2.imdecode` chống lỗi path Unicode tiếng Việt trên Windows) và PIL (`Image.open`), chuyển mức xám, resize $256 \times 256$.

### 📌 PHẦN V: TRIỂN KHAI VỚI PYTHON & PYWAVELETS (CẢI TIẾN CODE)
- Cải tiến hàm `wavelet_hash` với tham số `hash_size`, xử lý ngoại lệ (file hỏng/không tồn tại), chuẩn hóa hệ số (Min-Max/Z-score) trước lượng tử hóa, tối ưu hóa băng tần LL.
- Thử nghiệm khảo sát 4 họ Wavelet (`haar`, `db4`, `sym4`, `coif2`) trên cùng tập ảnh và đánh giá Accuracy vs Speed.