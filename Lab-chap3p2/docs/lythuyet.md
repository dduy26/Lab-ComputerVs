# PHẦN IV: BÁO CÁO LÝ THUYẾT BĂM HÌNH ẢNH WAVELET (WAVELET HASHING - wHash)

> **Dự án:** `Lab-chap3p2`  
> **Tên tệp báo cáo:** `docs/lythuyet.md`  
> **Tệp mã nguồn đi kèm:** [`notebook/code.py`](file:///d:/X%E1%BB%AD%20l%C3%AD%20%E1%BA%A3nh/FileGit/Lab-ComputerVs/Lab-chap3p2/notebook/code.py)

---

## 📖 I. TỔNG QUAN VỀ BĂM HÌNH ẢNH CẢM NHẬN (PERCEPTUAL IMAGE HASHING)

Mã băm hình ảnh cảm nhận (Perceptual Image Hashing) là kỹ thuật tạo ra một chuỗi nhị phân cố định (mã băm - hash code) đại diện cho nội dung cấu trúc thị giác của hình ảnh.

Khác với các hàm băm mật mã học truyền thống (như MD5, SHA-256 - nơi chỉ cần thay đổi 1 pixel cũng làm mã băm thay đổi hoàn toàn), mã băm Perceptual có tính chất **Bền vững (Robustness)**:
- Hai bức ảnh có nội dung giống nhau nhưng bị biến đổi nhỏ (nén JPEG, xoay góc nhẹ, thay đổi ánh sáng, chỉnh độ tương phản) sẽ cho ra hai mã băm gần như trùng khớp.
- Thuật toán **Wavelet Hash (wHash)** sử dụng phép biến đổi Wavelet rời rạc 2D (2D DWT) để trích xuất đặc trưng cấu trúc tần số thấp, mang lại độ chính xác và tính bền vững cao vượt trội so với các phương pháp dựa trên DCT (Discrete Cosine Transform) hay Average Hash (aHash).

---

## 📖 II. GIẢI THÍCH CHI TIẾT 3 BƯỚC CỦA THUẬT TOÁN WAVELET HASH (wHash)

Sơ đồ quy trình tạo mã băm Wavelet bao gồm 3 bước cốt lõi:

```
[Ảnh đầu vào] 
      │
      ▼ (Bước 1: Phân tách tần số)
[Biến đổi Wavelet 2D (2D DWT)] ──► Phân tách 4 băng tần (LL, LH, HL, HH) ──► Trích xuất Băng tần LL
      │
      ▼ (Bước 2: Lượng tử hóa)
[Lượng tử hóa hệ số (Quantization)] ──► So sánh hệ số LL với giá trị Trung vị (Median)
      │
      ▼ (Bước 3: Tạo mã nhị phân & Hex)
[Tạo mã băm Nhị phân (Binary Hash)] ──► Chuỗi 64-bit Nhị phân & Chuỗi Hex ──► Khoảng cách Hamming
```

---

### 1️⃣ Bước 1: Biến đổi Wavelet (Phân tích tần số và không gian)

* **Nguyên lý:**
  Ảnh đầu vào (sau khi được đưa về dạng ảnh mức xám và chuẩn hóa kích thước $256 \times 256$) được phân tích đa độ phân giải bằng biến đổi Wavelet rời rạc 2D (2D DWT) với các hàm cơ sở như `haar` hoặc `db4` (Daubechies 4).
* **Phân tách các băng tần (Sub-bands):**
  Phép biến đổi 2D DWT phân tách ảnh thành 4 băng tần tần số ở cấp 1 (và tiếp tục phân tách cấp 2, cấp 3 trên băng tần LL):
  1. **Băng tần LL (Low-Low):** Băng tần xấp xỉ tần số thấp theo cả chiều ngang và chiều dọc. Đây là nơi chứa **phần lớn năng lượng và cấu trúc hình học tổng thể** của hình ảnh.
  2. **Băng tần LH (Low-High):** Chứa các chi tiết biên tần số cao theo chiều ngang.
  3. **Băng tần HL (High-Low):** Chứa các chi tiết biên tần số cao theo chiều dọc.
  4. **Băng tần HH (High-High):** Chứa các chi tiết đường chéo và nhiễu tần số cao.
* **Tác dụng của Băng tần LL:**
  Băng tần **LL** giữ thông tin hình dạng nội dung chính mà mắt người cảm nhận được. Các chi tiết tần số cao (LH, HL, HH) dễ bị làm mờ hoặc mất đi do nén ảnh JPEG, trong khi băng tần LL cực kỳ bền vững trước nhiễu và biến đổi môi trường.

---

### 2️⃣ Bước 2: Lượng tử hóa hệ số (Quantization - Giảm độ chính xác)

* **Khái niệm Lượng tử hóa:**
  Các hệ số thu được từ băng tần LL là các số thực chấm động (floating-point continuous values). Lượng tử hóa làm giảm độ phân giải số (precision reduction), biến các hệ số liên tục thành các giá trị rời rạc nhị phân $0$ và $1$ nhằm **giảm độ nhạy cảm đối với các biến động số học nhỏ**.
* **Lượng tử hóa dựa trên Trung vị (Median Thresholding):**
  1. Resize/Crop ma trận hệ số LL về kích thước mã băm mong muốn $N \times N$ (ví dụ: $8 \times 8 = 64$ hệ số).
  2. Tính giá trị **Trung vị (Median)** của toàn bộ 64 hệ số trong ma trận $8 \times 8$:
     $$M = \text{median}(LL_{8 \times 8})$$
  3. Áp dụng phân ngưỡng nhị phân:
     $$Q(i, j) = \begin{cases} 1 & \text{nếu } LL(i, j) \ge M \\ 0 & \text{nếu } LL(i, j) < M \end{cases}$$
* **Ý nghĩa:**
  So sánh với giá trị trung vị đảm bảo phân bố bit `1` và `0` luôn cân bằng 50% - 50%. Kỹ thuật này triệt tiêu ảnh hưởng của sự thay đổi độ sáng tổng thể (brightness) hoặc độ tương phản (contrast).

---

### 3️⃣ Bước 3: Tạo mã băm (Binary Hash Code & Hex Representation)

* **Chuỗi nhị phân:**
  Ma trận lượng tử hóa $Q$ kích thước $8 \times 8$ được duỗi thẳng (flatten) thành một mảng 1D gồm **64 bits nhị phân** ($0$ và $1$).
* **Chuỗi Hexadecimal:**
  Gom mỗi 4 bits nhị phân thành 1 ký tự Hex (0-F) để tạo chuỗi băm Hex ngắn gọn 16 ký tự (ví dụ: `ffffffffff99ffff`).
* **So sánh độ tương đồng bằng Khoảng cách Hamming (Hamming Distance):**
  Khoảng cách Hamming giữa hai mã băm nhị phân $H_A$ và $H_B$ đếm số lượng bit khác biệt:
  $$D_{\text{Hamming}} = \sum_{i=1}^{K} (H_A[i] \oplus H_B[i])$$
  * **Tỷ lệ tương đồng (%):** $\text{Similarity} = \left(1 - \frac{D_{\text{Hamming}}}{K}\right) \times 100\%$
  * **Quy tắc đánh giá:**
    * $D_{\text{Hamming}} \le 10 \text{ bits}$: Hai hình ảnh **TƯƠNG ĐỒNG / GIỐNG NHAU** (Duplicate / Similar images).
    * $D_{\text{Hamming}} > 10 \text{ bits}$: Hai hình ảnh **KHÁC NHAU** (Different images).

---

## 📖 II.5. ĐÁNH GIÁ HIỆU SUẤT THUẬT TOÁN VÀ ĐƯỜNG CONG ROC (EVALUATION METRICS & ROC CURVE)
> **Phụ trách:** Thành viên 3: Duy (random)

### 1️⃣ Khái niệm Ma trận Nhầm lẫn (Confusion Matrix) & Chỉ số đánh giá

Khi đánh giá bài toán phân loại nhị phân cặp hình ảnh (Tương đồng vs Khác biệt) dựa trên ngưỡng khoảng cách Hamming $D_{\text{Hamming}} \le 10$ bits, các kết quả dự đoán được phân loại vào 4 ô của Ma trận Nhầm lẫn:

- **TP (True Positive - Dương tính thật):** Số lượng cặp ảnh thực sự **TƯƠNG ĐỒNG** được mô hình dự đoán chính xác là **TƯƠNG ĐỒNG** ($D_{\text{Hamming}} \le 10$).
- **TN (True Negative - Âm tính thật):** Số lượng cặp ảnh thực sự **KHÁC BIỆT** được mô hình dự đoán chính xác là **KHÁC BIỆT** ($D_{\text{Hamming}} > 10$).
- **FP (False Positive - Dương tính giả / Type I Error):** Số lượng cặp ảnh thực sự **KHÁC BIỆT** nhưng mô hình phán đoán nhầm là **TƯƠNG ĐỒNG**.
- **FN (False Negative - Âm tính giả / Type II Error):** Số lượng cặp ảnh thực sự **TƯƠNG ĐỒNG** nhưng mô hình phán đoán nhầm là **KHÁC BIỆT**.

#### Công thức toán học các chỉ số đánh giá:

1. **Độ chính xác (Accuracy):**
   Tỷ lệ dự đoán đúng (cả Tương đồng và Khác biệt) trên tổng số cặp thử nghiệm:
   $$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$

2. **Độ nhạy (Sensitivity / Recall / True Positive Rate - TPR):**
   Tỷ lệ các cặp ảnh tương đồng thực tế được mô hình nhận diện thành công:
   $$\text{Sensitivity} = \frac{TP}{TP + FN}$$

3. **Độ đặc hiệu (Specificity / True Negative Rate - TNR):**
   Tỷ lệ các cặp ảnh khác biệt thực tế được mô hình phát hiện và loại trừ chính xác:
   $$\text{Specificity} = \frac{TN}{TN + FP}$$

---

### 2️⃣ Đường cong ROC (Receiver Operating Characteristic) & Ý nghĩa AUC

* **Đường cong ROC (ROC Curve):**
  Là biểu đồ đường biểu diễn sự thay đổi của **True Positive Rate (Sensitivity)** trên trục tung $y$ so với **False Positive Rate ($\text{FPR} = 1 - \text{Specificity}$)** trên trục hoành $x$ tại mọi ngưỡng quyết định điểm tương đồng (Similarity Score thresholds từ 0.0 đến 1.0).

* **Giải thích ý nghĩa AUC (Area Under Curve):**
  - **AUC** là diện tích bề mặt nằm dưới đường cong ROC, mang giá trị số thực nằm trong khoảng $[0.5, 1.0]$.
  - **$\text{AUC} = 1.0$ (Lý tưởng):** Thuật toán phân loại hoàn hảo, phân tách tuyệt đối 100% giữa tập các cặp ảnh tương đồng và tập khác biệt mà không có sự chồng lấp điểm số.
  - **$0.9 \le \text{AUC} < 1.0$ (Xuất sắc):** Khả năng phân biệt cực kỳ cao và ổn định.
  - **$\text{AUC} = 0.5$ (Ngẫu nhiên):** Thuật toán không có khả năng phân biệt (tương đương tung đồng xu ngẫu nhiên).

---

### 3️⃣ Hướng dẫn vẽ ROC bằng `sklearn.metrics.roc_curve` và `matplotlib`

Để vẽ đường cong ROC thực nghiệm từ tập mã băm thu được, quy trình gồm 4 bước:

1. **Chuẩn bị mảng nhãn `y_true` và mảng điểm số `y_scores`:**
   Mỗi cặp ảnh được gán nhãn thực tế $y_{\text{true}} \in \{0, 1\}$ và tính điểm tương đồng liên tục:
   $$s_i = 1 - \frac{D_{\text{Hamming}}}{64}$$

2. **Gọi hàm `roc_curve` và `auc` từ thư viện `sklearn.metrics`:**
   ```python
   from sklearn.metrics import roc_curve, auc
   
   # Tính toán các tỷ lệ FPR, TPR và tập ngưỡng
   fpr, tpr, thresholds = roc_curve(y_true, y_scores)
   
   # Tính diện tích dưới đường cong AUC
   roc_auc = auc(fpr, tpr)
   ```

3. **Vẽ biểu đồ đồ họa với `matplotlib.pyplot`:**
   ```python
   import matplotlib.pyplot as plt
   
   plt.figure(figsize=(8, 6))
   # Vẽ đường ROC thực nghiệm
   plt.plot(fpr, tpr, color='darkorange', lw=2, label=f'Đường cong ROC (AUC = {roc_auc:.4f})')
   # Vẽ đường phân cách ngẫu nhiên AUC = 0.5
   plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Phân loại ngẫu nhiên (AUC = 0.5)')
   
   plt.xlim([0.0, 1.0])
   plt.ylim([0.0, 1.05])
   plt.xlabel('False Positive Rate (1 - Specificity)', fontsize=11)
   plt.ylabel('True Positive Rate (Sensitivity / Recall)', fontsize=11)
   plt.title('ĐƯỜNG CONG ROC VÀ ĐÁNH GIÁ HIỆU SUẤT WAVELET HASH (wHash)', fontsize=12, fontweight='bold')
   plt.legend(loc="lower right")
   plt.grid(True, linestyle=':', alpha=0.6)
   
   # Lưu biểu đồ xuất ra file
   plt.savefig("data/output/roc_curve_evaluation.png", dpi=150)
   plt.close()
   ```

---

### 4️⃣ Đánh giá hiệu suất thuật toán dựa trên các chỉ số thực nghiệm

* **Đánh giá về tính Bền vững (Robustness):**
  Thuật toán Wavelet Hash trích xuất đặc trưng xấp xỉ tần số thấp ở băng tần $LL$ (Low-Low) qua phép biến đổi `pywt.wavedec2()`. Do đó, các biến đổi hình ảnh như nén nhe, làm mờ Gauss, xoay nhỏ ($\pm 15^\circ$), hay chỉnh độ sáng không làm thay đổi các hệ số LL chính, giúp **Sensitivity (Recall)** tiến sát $100\%$.

* **Đánh giá về khả năng Phân biệt (Discrimination):**
  Lượng tử hóa trung vị `np.median()` tạo ra mã nhị phân 64-bit cân bằng entropy. Khi so sánh hai ảnh có nội dung hoàn toàn khác biệt, khoảng cách Hamming dao động trung bình khoảng $28 - 36$ bits ($\text{BER} \approx 50\%$), giúp **Specificity** đạt $100\%$.

* **Kết luận chung:**
  Tổng hợp lại, thuật toán đạt chỉ số **Accuracy = 1.0**, **Sensitivity = 1.0**, **Specificity = 1.0** và **AUC = 1.0** trên tập thử nghiệm chuẩn hóa, chứng minh tính hiệu quả vượt trội của Wavelet Hash trong ứng dụng tìm kiếm và so sánh ảnh cảm nhận.

---

## 📖 III. BẢNG MÔ TẢ CÁC HÀM XỬ LÝ TRONG FILE `code.py`

| Tên hàm | Thư viện sử dụng | Chức năng chi tiết |
| :--- | :--- | :--- |
| `resolve_path()` | `os.path` | Tự động xác định đường dẫn ảnh tuyệt đối an toàn bất kể CWD hiện tại. |
| `preprocess_image_cv2()` | `cv2` (OpenCV), `numpy` | Đọc ảnh qua `np.fromfile` + `cv2.imdecode` (tránh lỗi Unicode path tiếng Việt trên Windows), chuyển xám (`cv2.COLOR_BGR2GRAY`) và resize cố định $256 \times 256$ (`cv2.resize`). |
| `preprocess_image_pil()` | `PIL.Image` | Đọc ảnh bằng PIL (`Image.open`), chuyển mức xám (`convert('L')`) và resize chuẩn hóa (`resize`). |
| `wavelet_hash()` | `pywt` (PyWavelets), `numpy` | Phân tách 2D DWT (`pywt.wavedec2`), lấy băng tần LL, lượng tử hóa bằng trung vị (`np.median`) và tạo chuỗi bit 64-bit + mã Hex. |
| `hamming_distance()` | `numpy` | Đếm số lượng bit khác biệt giữa 2 mã nhị phân (`np.count_nonzero(b1 != b2)`). |
| `visualize_wavelet_hash()` | `matplotlib.pyplot` | Biến đổi DWT cấp 1 (`pywt.dwt2`), vẽ lưới biểu đồ 6 subplot và lưu ảnh tại `data/output/wavelet_hash_visualization_cv2.png`. |
| `evaluate_performance_and_roc()` | `sklearn.metrics`, `matplotlib.pyplot` | Tính Confusion Matrix ($TP, TN, FP, FN$), các chỉ số Accuracy, Sensitivity, Specificity, vẽ và lưu đường cong ROC (`roc_curve_evaluation.png`). |

---
<div style="height: 40px;"></div>


## 📖 III. 2. Xây dựng ứng dụng tìm kiếm hình ảnh dựa trên hàm băm wavelet.

### 1. Tổng quan
Ứng dụng tìm kiếm hình ảnh sử dụng mã băm cảm nhận (Perceptual Hash) cho phép truy xuất nhanh các ảnh tương tự trong một tập dữ liệu lớn. Wavelet Hash (wHash) được chọn vì tính bền vững với các biến đổi thông thường (nén, xoay nhẹ, thay đổi độ sáng) và khả năng phân biệt cao.

### 2. Kiến trúc hệ thống
Hệ thống tìm kiếm gồm 3 thành phần chính:

- **Bộ tiền xử lý**: Đọc ảnh, chuyển sang grayscale, resize về kích thước cố định.
- **Trích xuất đặc trưng**: Áp dụng 2D DWT, lấy băng tần LL, lượng tử hóa median để tạo mã băm 64-bit.
- **Cơ sở dữ liệu & Truy vấn**: Lưu trữ các mã băm dưới dạng JSON, so sánh bằng khoảng cách Hamming, trả về top‑K ảnh giống nhất.

### 3. Quy trình xây dựng database
```
[Thư mục ảnh]
│
▼ (duyệt từng file)
[Tiền xử lý & Wavelet Hash]
│
▼ (lưu dict)
[File JSON: { "path": "hash_hex" }]
```

### 4. Quy trình tìm kiếm
```
[Ảnh truy vấn]
│
▼ (tính hash)
[Hash query]
│
▼ (so sánh với DB)
[Khoảng cách Hamming → Sắp xếp tăng dần]
│
▼
[Top K ảnh giống nhất]
```

### 5. Các hàm chính trong `search_app.py`

| Hàm | Chức năng |
| :--- | :--- |
| `build_database(image_dir, db_path)` | Duyệt thư mục, tính wHash cho mỗi ảnh, lưu vào JSON. |
| `search(query_path, db_path, top_k)` | Tìm kiếm ảnh tương tự, trả về danh sách (đường dẫn, khoảng cách, độ tương đồng). |
| `cli()` | Giao diện dòng lệnh với argparse. |

### 6. Đánh giá hiệu năng

- **Tốc độ xây dựng database**: ~0.08 giây cho 22 ảnh.
- **Tốc độ tìm kiếm**: ~99 ms cho 22 ảnh.
- **Độ chính xác**: Với ngưỡng Hamming ≤ 1 cho ảnh giống, >10 cho ảnh khác (dựa trên kết quả kiểm thử).

PHẦN III.1 Thực hiện khảo sát về các phương pháp băm wavelet khác nhau và so sánh hiệu suất của chúng.
1. Khái niệm Biến đổi Wavelet (Discrete Wavelet Transform - DWT)
Nguyên lý: Phân rã ảnh thành 4 băng tần tần số ở cấp độ 1:
LL (Low-Low): Băng tần xấp xỉ tần số thấp, chứa hầu hết năng lượng và khung bố cục chính của ảnh.
LH (Low-High): Bắt các chi tiết đường biên ngang.
HL (High-Low): Bắt các chi tiết đường biên dọc.
HH (High-High): Bắt các chi tiết đường chéo và nhiễu.
2. Khái niệm Mã băm ảnh (Perceptual Image Hashing)
Khác với mã băm mật mã (như MD5, SHA-256 - chỉ cần đổi 1 bit là mã thay đổi hoàn toàn), Perceptual Hash tạo ra chuỗi bit đại diện cho "cảm nhận trực quan" của ảnh. Hai ảnh có nội dung tương tự nhau sẽ cho hai chuỗi mã băm gần giống nhau (khoảng cách Hamming nhỏ).
3. Nguyên lý 3 phương pháp khảo sát
Phương pháp 1 (LL Hash): Rút gọn băng tần $LL$ về kích thước cố định (ví dụ $8 \times 8$). So sánh giá trị từng phần tử với giá trị trung vị (median) để tạo chuỗi bit 0/1.
Phương pháp 2 (Detail Energy Hash): Chia các băng tần $LH, HL, HH$ thành các ô nhỏ (blocks), tính tổng năng lượng $E = \sum I_{ij}^2$ trên từng ô để đại diện cho mật độ kết cấu, sau đó nhị phân hóa chuỗi năng lượng này.
Phương pháp 3 (Combined Hash): Ghép nối chuỗi bit từ $LL$ (giữ cấu trúc tổng thể) và chuỗi bit từ $Energy$ (giữ độ sắc nét/chi tiết bề mặt) theo tỷ lệ trọng số nhất định (ví dụ 70% - 30%).
4. Các chỉ số đánh giá hiệu suất (Performance Metrics)
Khoảng cách Hamming: Số lượng bit khác nhau giữa 2 chuỗi mã băm.
Độ chính xác (Accuracy): Tỷ lệ dự đoán đúng cặp ảnh "Tương tự" hay "Khác nhau".
Khả năng phân biệt (Discrimination): Khoảng cách Hamming chuẩn hóa giữa 2 ảnh hoàn toàn khác nhau (giá trị lý tưởng tiến sát $0.5$).
