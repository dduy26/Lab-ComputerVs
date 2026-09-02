#  LÝ THUYẾT TỔNG HỢP & THỰC NGHIỆM - LAB-CHAP3P2
## SO SÁNH SỰ TƯƠNG ĐỒNG CỦA CÁC HÌNH ẢNH SỬ DỤNG WAVELET HASH (wHash)

> **Môn học:** Xử Lý Ảnh Số / Thị Giác Máy Tính  
> **Dự án:** `Lab-chap3p2`  
> **Tệp báo cáo:** `docs/lythuyet.md`  
> **Mã nguồn tích hợp:** [`notebook/code.py`](file:///d:/X%E1%BB%AD%20L%C3%AD%20%E1%BA%A2nh/Lab/Lab-chap3p2/notebook/code.py)  
> **Notebook hoàn chỉnh:** [`notebook/lab-chap3-p2.ipynb`](file:///d:/X%E1%BB%AD%20L%C3%AD%20%E1%BA%A2nh/Lab/Lab-chap3p2/notebook/lab-chap3-p2.ipynb)

---

## 📌 BẢNG PHÂN CÔNG NHIỆM VỤ DỰ ÁN (7 THÀNH VIÊN)

| STT | Thành viên | Phụ trách nội dung | Phần bài làm |
| :---: | :--- | :--- | :--- |
| **1** | **Thông** | Tổng quan mục tiêu, Chuẩn bị dữ liệu (thư mục, naming, 22 ảnh), Trích xuất Wavelet 2D (`pywt.wavedec2`), Phân tích 4 băng tần (LL, LH, HL, HH) và ảnh hưởng của wavelet base. | **Phần I + II.1 + II.2** |
| **2** | **Đức** | Quá trình lượng tử hóa hệ số (Median/Mean), Nhị phân hóa mã băm (64-bit/Hex), Giải thích Khoảng cách Hamming, Ngưỡng quyết định tương đồng ($\le 10\%$), Thực nghiệm 3 cặp ảnh. | **Phần II.3 + II.4** |
| **3** | **Duy** | Đánh giá chỉ số hiệu suất: Accuracy, Sensitivity (Recall), Specificity, Confusion Matrix; Ý nghĩa AUC và Hướng dẫn vẽ Đường cong ROC bằng `sklearn.metrics` & `matplotlib`. | **Phần II.5 (Đánh giá & ROC)** |
| **4** | **Thọ** | Giải thích 3 bước Wavelet Hash (Phân tích tần số $\rightarrow$ Lượng tử hóa $\rightarrow$ Tạo mã băm); Code hoàn chỉnh đọc & chuẩn hóa ảnh đầu vào bằng OpenCV và PIL. | **Phần IV (Tham khảo & Pipeline)** |
| **5** | **Vinh** | Cải tiến code mẫu (tham số `hash_size`, xử lý ngoại lệ, tối ưu lấy LL, chuẩn hóa Min-Max); So sánh 4 loại Wavelet (`haar`, `db4`, `sym4`, `coif2`) về độ chính xác và tốc độ. | **Phần V (Triển khai & Cải tiến)** |
| **6** | **Huy** | Khảo sát các phương pháp băm Wavelet: PP1 (LL Hash), PP2 (Detail Energy Hash), PP3 (Combined Hash); Bảng so sánh 3 PP về Accuracy, Execution Time và Khả năng phân biệt. | **Phần III.1 (Khảo sát các PP)** |
| **7** | **Phước** | Xây dựng ứng dụng tìm kiếm hình ảnh dựa trên Wavelet Hash (CLI app, CSDL JSON, Tìm kiếm Top-K Hamming, Đánh giá tốc độ & độ chính xác). | **Phần III.2 (Ứng dụng Tìm kiếm)** |

---

## 📖 PHẦN I: MỤC TIÊU BÀI TẬP (MEMBER 1: THÔNG)

### 1. Tổng quan bài tập
Mã băm cảm nhận (Perceptual Image Hashing) là kỹ thuật nén nội dung thị giác của hình ảnh thành một chuỗi nhị phân cố định (mã băm - hash code).
Khác với các thuật toán băm mật mã học (như MD5, SHA-256 - nơi chỉ cần thay đổi 1 pixel cũng làm mã băm thay đổi hoàn toàn), mã băm Perceptual sở hữu tính chất **Bền vững (Robustness)**:
- Hai bức ảnh có cùng nội dung cấu trúc nhưng chịu các biến đổi nhẹ (nén JPEG, xoay góc nhỏ, đổi độ sáng, mờ nhiễu) sẽ cho hai mã băm tương đồng (khoảng cách Hamming nhỏ).
- Thuật toán **Wavelet Hash (wHash)** sử dụng Phép biến đổi Wavelet rời rạc 2D (2D DWT) để trích xuất đặc trưng cấu trúc ở băng tần tần số thấp, mang lại độ chính xác cao và khả năng chống nhiễu vượt trội hơn hẳn so với aHash (Average Hash) hay dHash (Difference Hash).

### 2. Mục tiêu kỹ thuật
- **Nắm vững biến đổi Wavelet 2D:** Sử dụng thư viện `PyWavelets` (`pywt.wavedec2()`) để phân tích đa độ phân giải.
- **Biết cách trích xuất thông tin:** Tách biệt thành phần xấp xỉ ($LL$) chứa thông tin năng lượng chính và thành phần chi tiết ($LH, HL, HH$).
- **Lượng tử hóa & So sánh:** Biến đổi các hệ số Wavelet liên tục thành mã nhị phân 64-bit và đo khoảng cách Hamming.
- **Đánh giá & Ứng dụng:** Khảo sát các biến thể thuật toán, đánh giá chỉ số ROC/AUC và xây dựng hệ thống tìm kiếm ảnh.

---

## 🗂️ PHẦN II.1 & II.2: CHUẨN BỊ DỮ LIỆU & TRÍCH XUẤT WAVELET (MEMBER 1: THÔNG)

### 1. Chuẩn bị dữ liệu (II.1)

#### 🏢 Cách tổ chức thư mục:
```
data/input/
├── meme.jpg                    # Ảnh gốc (nhóm giống)
├── memetest.jpg                # Ảnh đối chứng mặc định
├── similar/                    # 16 biến thể của meme.jpg (ảnh giống nhau)
│   ├── similar_meme_rot5.png   # Xoay 5°
│   ├── similar_meme_rot15.png  # Xoay 15°
│   ├── similar_meme_scale90.png# Thu nhỏ 90%
│   ├── similar_meme_gauss15.png# Nhiễu Gaussian σ=15
│   ├── similar_meme_saltpepper3.png # Nhiễu muối tiêu 3%
│   ├── similar_meme_blur.png   # Làm mờ Gaussian (5x5)
│   ├── similar_meme_bright30.png    # Tăng độ sáng +30
│   ├── similar_meme_contrast1p5.png # Tăng tương phản x1.5
│   └── ...
└── different/                  # 6 ảnh khác hẳn (ẢNH THẬT người dùng chụp)
    ├── different_memetest.png
    ├── different_awww.png
    ├── different_hehehe.jpg
    └── different_huhu.png
```

#### 🏷️ Quy tắc đặt tên file:
`<nhóm>_<đối tượng>_<biến thể>.<jpg|png>`
- `similar` / `different`: Nhóm dữ liệu.
- `meme` / `memetest` / `awww`: Tên đối tượng gốc.
- `rot15`, `gauss15`, `blur`: Phép biến đổi áp dụng.

#### 📊 Số lượng ảnh:
- **Tập Similar (Dương tính):** 16 ảnh (từ `meme.jpg` qua 6 nhóm biến đổi: xoay, scale, nhiễu, blur, sáng/tương phản, crop/flip).
- **Tập Different (Âm tính):** 6 ảnh (ảnh `memetest.jpg` + 5 ảnh chụp thực tế ngoài đời).
- **Tổng cộng:** 22 ảnh (đạt tiêu chuẩn yêu cầu 20-30 ảnh).

---

### 2. Trích xuất Wavelet 2D (II.2)

#### 📐 Giải thích biến đổi Wavelet 2D (`pywt.wavedec2`):
Hàm `pywt.wavedec2(img, wavelet, level)` thực hiện phân tích đa độ phân giải 2D:
1. Chiều ngang và chiều dọc của ảnh lần lượt đi qua bộ lọc thông thấp (Low-pass $L$) và thông cao (High-pass $H$).
2. Kết quả thu được 4 băng tần ở cấp 1:
   - **$LL$ (Low-Low):** Băng tần xấp xỉ tần số thấp theo cả 2 chiều, chứa **năng lượng chính và cấu trúc tổng thể** của hình ảnh.
   - **$LH$ (Low-High):** Chi tiết tần số cao theo chiều ngang (chứa đường biên ngang).
   - **$HL$ (High-Low):** Chi tiết tần số cao theo chiều dọc (chứa đường biên dọc).
   - **$HH$ (High-High):** Chi tiết tần số cao theo chiều chéo (chứa đường biên chéo và nhiễu).

#### 🔬 Kích thước các băng tần (với ảnh $256 \times 256$, `haar`, level 3):
- Ma trận $LL_3$: kích thước $32 \times 32$.
- Các chi tiết $LH_3, HL_3, HH_3$: kích thước $32 \times 32$.
- Các chi tiết Cấp 2 ($64 \times 64$), Cấp 1 ($128 \times 128$).

#### ⚖️ Ảnh hưởng của việc chọn loại Wavelet base:
- **`haar`:** Đơn giản nhất, bậc lọc ngắn (length=2), tốc độ tính toán cực nhanh. Phản ứng nhạy với biên độ thay đổi đột ngột.
- **`db4` (Daubechies 4):** Bậc lọc dài hơn, mịn hơn `haar`, khả năng triệt tiêu nhiễu cao hơn nhưng chi phí tính toán tăng.
- **`sym2` (Symlet 2):** Tính đối xứng gần đúng, giúp giảm biến dạng pha khi trích xuất cấu trúc hình học.

---

## 🧮 PHẦN II.3 & II.4: LƯỢNG TỬ HÓA MÃ BĂM & HAMMING DISTANCE (MEMBER 2: ĐỨC)

### 1. Quá trình lượng tử hóa hệ số (II.3)
Các hệ số thu được ở băng tần $LL$ là các số thực chấm động (floating-point). Quá trình lượng tử hóa (Quantization) làm giảm độ chính xác số học để chuyển các giá trị liên tục này thành các bit nhị phân $0$ và $1$.

#### 📉 Các phương pháp phân ngưỡng lượng tử:
1. **Lượng tử hóa dựa trên Trung vị (Median Thresholding - Khuyên dùng):**
   - Resize ma trận $LL$ về kích thước $8 \times 8 = 64$ hệ số.
   - Tính giá trị Trung vị $M = \text{median}(LL_{8 \times 8})$.
   - Tạo bit nhị phân:
     $$Q(i, j) = \begin{cases} 1 & \text{nếu } LL(i, j) \ge M \\ 0 & \text{nếu } LL(i, j) < M \end{cases}$$
   - **Ưu điểm:** Đảm bảo số lượng bit `1` và `0` luôn cân bằng chính xác 50% - 50% (32 bit `1` và 32 bit `0`), triệt tiêu hoàn toàn ảnh hưởng của việc tăng giảm độ sáng tổng thể.
2. **Lượng tử hóa dựa trên Trung bình (Mean Thresholding):**
   - So sánh với giá trị $M = \text{mean}(LL_{8 \times 8})$. Dễ bị lệch bit khi ảnh có một số vùng quá sáng hoặc quá tối.
3. **Thư viện `pywt.quantize`:** Lượng tử hóa theo mức cố định.

#### 🔢 Chuyển ma trận thành mã nhị phân & Hex:
- Duỗi thẳng ma trận $8 \times 8$ thành vector 64 bits nhị phân.
- Gom nhóm mỗi 4 bits nhị phân thành 1 ký tự Hexadecimal (0-F) thu được chuỗi Hex 16 ký tự (ví dụ: `ffffffffff99ffff`).

---

### 2. So sánh hàm băm & Khoảng cách Hamming (II.4)

#### 📐 Công thức Khoảng cách Hamming:
Khoảng cách Hamming giữa hai mã băm nhị phân $H_1$ và $H_2$ đếm tổng số bit khác biệt tại cùng vị trí:
$$D_{\text{Hamming}} = \sum_{i=1}^{K} (H_1[i] \neq H_2[i])$$
Tỷ lệ tương đồng (%):
$$\text{Similarity} = \left(1 - \frac{D_{\text{Hamming}}}{K}\right) \times 100\%$$

#### 🎯 Ngưỡng quyết định tương đồng:
- Với độ dài mã băm $K = 64$ bits, ngưỡng quyết định hai ảnh tương đồng là **$\le 10\%$ độ dài hash**, tương đương:
  $$D_{\text{Hamming}} \le 6 \text{ bits} \quad (\text{hoặc } \le 10 \text{ bits tùy độ mở rộng})$$
- Nếu $D_{\text{Hamming}} \le 6$ (hoặc $\le 10$): Hai ảnh được kết luận là **TƯƠNG ĐỒNG / GIỐNG NHAU**.
- Nếu $D_{\text{Hamming}} > 10$: Hai ảnh được kết luận là **KHÁC NHAU**.

#### 📊 Minh họa số liệu thực nghiệm trên 3 cặp ảnh mẫu:

| Phép thử | Khoảng cách Hamming | Tỷ lệ Tương đồng (%) | Đánh giá phân loại |
| :--- | :---: | :---: | :---: |
| **Cặp 1: Ảnh gốc vs Ảnh gốc (meme.jpg)** | `0 / 64 bit` | `100.00%` | **TƯƠNG ĐỒNG (Match)** |
| **Cặp 2: Gốc vs Biến thể (Blur + Noise)** | `2 / 64 bit` | `96.88%` | **TƯƠNG ĐỒNG (Match)** |
| **Cặp 3: Gốc vs Ảnh khác loại (memetest.jpg)** | `33 / 64 bit` | `48.44%` | **KHÁC NHAU (Mismatch)** |

---

## 📈 PHẦN II.5: ĐÁNH GIÁ HIỆU SUẤT VÀ ĐƯỜNG CONG ROC (MEMBER 3: DUY)

### 1. Ma trận Nhầm lẫn (Confusion Matrix)
Khi kiểm thử bài toán phân loại nhị phân trên $N$ cặp ảnh với ngưỡng Hamming $D \le 10$:
- **TP (True Positive):** Cặp ảnh thực sự **Tương đồng** được dự đoán đúng là **Tương đồng**.
- **TN (True Negative):** Cặp ảnh thực sự **Khác biệt** được dự đoán đúng là **Khác biệt**.
- **FP (False Positive):** Cặp ảnh **Khác biệt** bị dự đoán nhầm là **Tương đồng** (Báo động giả).
- **FN (False Negative):** Cặp ảnh **Tương đồng** bị dự đoán nhầm là **Khác biệt** (Bỏ sót).

### 2. Các chỉ số đánh giá cốt lõi

1. **Độ chính xác (Accuracy):**
   $$\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$$
2. **Độ nhạy (Sensitivity / Recall / True Positive Rate - TPR):**
   $$\text{Sensitivity} = \frac{TP}{TP + FN}$$
3. **Độ đặc hiệu (Specificity / True Negative Rate - TNR):**
   $$\text{Specificity} = \frac{TN}{TN + FP}$$

---

### 3. Đường cong ROC (Receiver Operating Characteristic) & Ý nghĩa AUC

- **Đường cong ROC:** Biểu diễn sự biến thiên của $TPR$ (Trục $Y$) theo $FPR = 1 - \text{Specificity}$ (Trục $X$) tại mọi ngưỡng điểm tương đồng $S \in [0, 1]$.
- **Ý nghĩa chỉ số AUC (Area Under Curve):**
  - $\text{AUC} = 1.0$: Phân loại hoàn hảo 100%.
  - $0.9 \le \text{AUC} < 1.0$: Mô hình xuất sắc.
  - $\text{AUC} = 0.5$: Phân loại ngẫu nhiên (không có giá trị).

---

### 4. Hướng dẫn vẽ đường cong ROC bằng `sklearn` và `matplotlib`

```python
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

# 1. Tính toán FPR, TPR và AUC
fpr, tpr, thresholds = roc_curve(y_true, y_scores)
roc_auc = auc(fpr, tpr)

# 2. Vẽ biểu đồ ROC
plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2.5, label=f'ROC curve (AUC = {roc_auc:.4f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Chance (AUC = 0.5)')
plt.xlabel('False Positive Rate (1 - Specificity)')
plt.ylabel('True Positive Rate (Sensitivity)')
plt.title('ROC CURVE - WAVELET HASH EVALUATION')
plt.legend(loc="lower right")
plt.grid(True, linestyle=':', alpha=0.6)
plt.savefig("data/output/roc_curve_evaluation.png", dpi=150)
```

---

## 🛠️ PHẦN IV: THAM KHẢO & CODE OPENCV / PIL HOÀN CHỈNH (MEMBER 4: THỌ)

### 1. Chi tiết 3 bước của thuật toán Wavelet Hash (wHash)
```
[Ảnh Đầu Vào]
      │
      ▼ (Bước 1: Phân tách tần số 2D-DWT)
[Băng tần LL (Tần số thấp xấp xỉ)] ──► Giữ năng lượng & bố cục chính
      │
      ▼ (Bước 2: Lượng tử hóa Median)
[Ma trận Bit 8x8] ──► So sánh từng phần tử với Median(LL)
      │
      ▼ (Bước 3: Tạo mã nhị phân & Hex)
[Mã băm 64-bit & Chuỗi Hex 16 ký tự] ──► So sánh bằng Khoảng cách Hamming
```

### 2. Code xử lý ảnh đầu vào bằng OpenCV và PIL

#### 🔹 Đọc ảnh bằng OpenCV (Chống lỗi tiếng Việt Unicode trên Windows):
```python
def preprocess_image_cv2(image_path, target_size=(256, 256)):
    # Đọc mảng byte an toàn bằng np.fromfile
    img_array = np.fromfile(image_path, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if len(img.shape) == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    return cv2.resize(gray, target_size, interpolation=cv2.INTER_AREA)
```

#### 🔹 Đọc ảnh bằng PIL:
```python
def preprocess_image_pil(image_path, target_size=(256, 256)):
    img = Image.open(image_path)
    gray = img.convert('L')
    resized = gray.resize(target_size, Image.Resampling.LANCZOS)
    return np.array(resized)
```

#### 🔹 Code mẫu tham khảo từ Slide 17:
```python
def wavelet_hash_slide_sample(image_path, wavelet='db4', level=3):
    img = preprocess_image_cv2(image_path)
    coeffs = pywt.wavedec2(img, wavelet=wavelet, level=level)
    coeffs_quant = [np.floor(np.abs(c) / 2.0).astype(int) for c in coeffs]
    flattened = np.concatenate([c.flatten() for c in coeffs_quant])
    hash_code = [int(bit) % 2 for bit in flattened]
    return hash_code
```

---

## ⚡ PHẦN V: TRIỂN KHAI VỚI PYTHON & PYWAVELETS (MEMBER 5: VINH)

### 1. Các cải tiến thuật toán wHash
- **Tham số `hash_size`:** Cho phép linh hoạt thay đổi độ dài mã băm ($8 \times 8 = 64$ bits hoặc $16 \times 16 = 256$ bits).
- **Chuẩn hóa hệ số (Min-Max Normalization):** Đưa ma trận $LL$ về khoảng $[0, 1]$ trước khi lượng tử hóa giúp tăng khả năng chống biến đổi độ tương phản.
- **Xử lý ngoại lệ (Exception Handling):** Kiểm tra đường dẫn an toàn, bẫy lỗi ảnh hỏng, đảm bảo chương trình không bị crash khi duyệt thư mục lớn.
- **Tối ưu hóa năng lượng:** Chỉ tính toán trên băng tần $LL$, bỏ qua các băng tần chi tiết để giảm $75\%$ khối lượng bộ nhớ.

### 2. Khảo sát so sánh 4 họ Wavelet (`haar`, `db4`, `sym4`, `coif2`)

| Họ Wavelet | Accuracy (%) | Thời gian xử lý TB (ms/ảnh) | Nhận xét tính chất |
| :--- | :---: | :---: | :--- |
| **`haar`** | **100.0%** | **0.85 ms** | Nhanh nhất, đơn giản nhất, hiệu quả tối ưu cho ảnh rõ nét. |
| **`db4`** | **100.0%** | **1.24 ms** | Mịn màng hơn, lọc nhiễu tần số cao tốt hơn `haar`. |
| **`sym4`** | **100.0%** | **1.31 ms** | Tính đối xứng cao, giữ hình dạng tốt khi bị xoay/biến dạng nhẹ. |
| **`coif2`** | **100.0%** | **1.52 ms** | Triệt tiêu triệt để các thành phần nhiễu phức tạp. |

---

## 🔍 PHẦN III.1: KHẢO SÁT CÁC PHƯƠNG PHÁP BĂM WAVELET (MEMBER 6: HUY)

Khảo sát 3 phương pháp băm khác nhau trên cùng tập dữ liệu 22 ảnh:

1. **Phương pháp 1 (PP1 - LL Hash):** Trích xuất ma trận xấp xỉ $LL$, resize $8 \times 8$, so sánh với Median để tạo 64 bits. (Đơn giản, nhanh).
2. **Phương pháp 2 (PP2 - Detail Energy Hash):** Chia các băng tần chi tiết $LH, HL, HH$ thành 64 ô block, tính tổng năng lượng $E = \sum I_{ij}^2$ trên từng block, so sánh với Median. (Nhạy với kết cấu bề mặt).
3. **Phương pháp 3 (PP3 - Combined Hash):** Ghép 45 bits từ $LL$ Hash (giữ cấu trúc tổng thể) và 19 bits từ Detail Energy Hash (giữ chi tiết biên).

### 📊 Bảng so sánh kết quả thực nghiệm 3 phương pháp:

| Phương pháp | Accuracy (%) | Thời gian (ms/ảnh) | Khả năng phân biệt (Avg Hamming ảnh khác) |
| :--- | :---: | :---: | :---: |
| **PP1: Băm LL (Appr. Hash)** | **100.0%** | **0.82 ms** | **31.4 / 64 bit (49.1%)** |
| **PP2: Băm Năng lượng chi tiết** | **81.8%** | **3.45 ms** | **24.2 / 64 bit (37.8%)** |
| **PP3: Băm Kết hợp (LL + Energy)**| **95.5%** | **3.88 ms** | **29.8 / 64 bit (46.5%)** |

**Nhận xét:** PP1 (Băm LL) đạt hiệu năng vượt trội nhất cả về độ chính xác ($100\%$), tốc độ xử lý nhanh nhất ($0.82$ ms) và khả năng phân biệt hai ảnh khác biệt rõ ràng nhất (~50% bit khác nhau).

---

## 🔎 PHẦN III.2: ỨNG DỤNG TÌM KIẾM HÌNH ẢNH (MEMBER 7: PHƯỚC)

### 1. Kiến trúc hệ thống
Xây dựng ứng dụng dòng lệnh CLI (`notebook/search_app.py`) bao gồm:
- **Index Builder:** Duyệt thư mục ảnh, tính mã băm wHash cho từng ảnh và lưu trữ vào Cơ sở dữ liệu JSON (`data/output/image_hashes.json`).
- **Search Engine:** Đọc ảnh Query, tính wHash query, đo Khoảng cách Hamming với toàn bộ DB, sắp xếp theo thứ tự khoảng cách tăng dần và xuất Top K kết quả tương đồng nhất.

### 2. Kết quả đánh giá ứng dụng
- **Tốc độ Xây dựng CSDL:** ~0.08 giây cho 22 ảnh (~3.6 ms/ảnh).
- **Tốc độ Truy vấn Tìm kiếm:** ~99 ms cho 22 ảnh.
- **Độ chính xác Top-K:** 100% các biến thể của ảnh gốc được xếp ở vị trí Top 1 đến Top 16 với khoảng cách Hamming $\le 6$, các ảnh khác bị đẩy xuống cuối với Hamming $\ge 28$.

---

## 🎯 PHẦN VI: KẾT LUẬN TỔNG KẾT DỰ ÁN

1. **Hiệu quả của Wavelet Hash (wHash):** Việc trích xuất băng tần $LL$ qua biến đổi Wavelet 2D tạo ra mã băm có tính bền vững cao trước các phép biến đổi ảnh thông thường (xoay, nén, mờ, nhiễu, tương phản) đồng thời phân biệt tuyệt đối giữa các ảnh khác loại.
2. **Lượng tử hóa Median:** Đảm bảo độ cân bằng bit 50-50, giúp triệt tiêu sự thay đổi ánh sáng.
3. **Thư viện Python & PyWavelets:** Cung cấp công cụ mạnh mẽ, linh hoạt và tối ưu tốc độ cho các bài toán xử lý ảnh số và thị giác máy tính.
