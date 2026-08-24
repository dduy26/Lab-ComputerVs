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

## 📖 III. BẢNG MÔ TẢ CÁC HÀM XỬ LÝ TRONG FILE `code.py`

| Tên hàm | Thư viện sử dụng | Chức năng chi tiết |
| :--- | :--- | :--- |
| `resolve_path()` | `os.path` | Tự động xác định đường dẫn ảnh tuyệt đối an toàn bất kể CWD hiện tại. |
| `preprocess_image_cv2()` | `cv2` (OpenCV), `numpy` | Đọc ảnh qua `np.fromfile` + `cv2.imdecode` (tránh lỗi Unicode path tiếng Việt trên Windows), chuyển xám (`cv2.COLOR_BGR2GRAY`) và resize cố định $256 \times 256$ (`cv2.resize`). |
| `preprocess_image_pil()` | `PIL.Image` | Đọc ảnh bằng PIL (`Image.open`), chuyển mức xám (`convert('L')`) và resize chuẩn hóa (`resize`). |
| `wavelet_hash()` | `pywt` (PyWavelets), `numpy` | Phân tách 2D DWT (`pywt.wavedec2`), lấy băng tần LL, lượng tử hóa bằng trung vị (`np.median`) và tạo chuỗi bit 64-bit + mã Hex. |
| `hamming_distance()` | `numpy` | Đếm số lượng bit khác biệt giữa 2 mã nhị phân (`np.count_nonzero(b1 != b2)`). |
| `visualize_wavelet_hash()` | `matplotlib.pyplot` | Biến đổi DWT cấp 1 (`pywt.dwt2`), vẽ lưới biểu đồ 6 subplot và lưu ảnh tại `data/output/wavelet_hash_visualization_cv2.png`. |

---
<div style="height: 40px;"></div>

## TẠO VÀ SO SÁNH MÃ BĂM HÌNH ẢNH DỰA TRÊN BIẾN ĐỔI WAVELET 2D VÀ KHOẢNG CÁCH HAMMING

### 1. Quá trình lượng tử hóa hệ số Wavelet

Lượng tử hóa (Quantization) trong thuật toán băm ảnh Wavelet (wHash) là quá trình ánh xạ tập hợp các hệ số thực liên tục $c(x, y) \in \mathbb{R}$ trong băng tần xấp xỉ tần số thấp ($LL$) về một tập hữu hạn các giá trị rời rạc mang tính biểu diễn cấu trúc.

Trong thực tế xử lý ảnh, có hai phương pháp lượng tử hóa chính:

* **Sử dụng thư viện `pywt.quantize` (Lượng tử hóa đa mức):**  
  Thực hiện lượng tử hóa đều (Uniform) hoặc lượng tử hóa có vùng chết (Deadzone quantization) theo bước lượng tử $\Delta$:
  $$Q(c) = \text{sign}(c) \cdot \left\lfloor \frac{\vert{}c\vert{}}{\Delta} + \frac{1}{2} \right\rfloor$$
  *Phương pháp này giữ lại nhiều mức độ xám của hệ số, phù hợp cho bài toán nén dữ liệu ảnh nhưng tạo ra vector hệ số phức tạp, khó so khớp nhanh.*

* **Lượng tử hóa nhị phân 1-bit tự xây dựng (Custom Binarization):**  
  Đây là kỹ thuật tiêu chuẩn của wHash nhằm tạo ra mã băm cảm nhận (Perceptual Hash). Toàn bộ ma trận hệ số $LL$ được ánh xạ trực tiếp về hai giá trị nhị phân $\{0, 1\}$ thông qua một ngưỡng tham chiếu $T$:
  $$Q(c(x, y)) = \begin{cases} 1 & \text{nếu } c(x, y) \ge T \\ 0 & \text{nếu } c(x, y) < T \end{cases}$$

---

### 2. Lựa chọn ngưỡng lượng tử ($T$) và ảnh hưởng đến độ dài mã băm

#### a. Chiến lược lựa chọn ngưỡng lượng tử
Việc chọn giá trị ngưỡng $T$ quyết định trực tiếp đến tính phân biệt (Discriminability) của mã băm:

* **Ngưỡng Trung vị (Median Thresholding - Khuyến nghị):**
  $$T = \text{Median}(LL)$$
  *Ưu điểm:* Luôn đảm bảo phân chia ma trận thành đúng 50% bit 0 và 50% bit 1. Điều này tối đa hóa Entropy thông tin của chuỗi băm ($H = 1\text{ bit/pixel}$), tránh tình trạng phân bố lệch bit (toàn bit 0 hoặc toàn bit 1) khi ảnh đầu vào bị biến đổi ánh sáng toàn cục (quá sáng hoặc quá tối).

* **Ngưỡng Trung bình (Mean Thresholding):**
  $$T = \mu = \frac{1}{M \times N} \sum_{x, y} LL(x, y)$$
  *Đặc điểm:* Dễ tính toán nhưng dễ bị lệch ngưỡng khi ảnh có một vài vùng quá sáng hoặc quá tối đột biến (outliers).

* **Ngưỡng cố định (Fixed Threshold):**
  *Đặc điểm:* Không thể thích ứng linh hoạt với các ảnh có phân bố histogram khác nhau, dễ gây ra hiện tượng trùng mã băm (hash collision) giữa các ảnh khác loại.

#### b. Mối quan hệ giữa kích thước ma trận và độ dài mã băm
Độ dài mã băm ($N_{\text{bits}}$) phụ thuộc trực tiếp vào kích thước ma trận $LL$ sau khi biến đổi hoặc sau bước chuẩn hóa (resize):

$$N_{\text{bits}} = W_{LL} \times H_{LL} \times k$$

*(Trong đó $W_{LL}, H_{LL}$ là chiều rộng, chiều cao ma trận $LL$; $k = 1$ đối với lượng tử hóa nhị phân).*

| Kích thước dải $LL$ | Độ dài mã băm ($N_{\text{bits}}$) | Độ dài chuỗi Hex | Đặc tính kỹ thuật |
| :--- | :---: | :---: | :--- |
| **$8 \times 8$** | **64 bits** | **16 ký tự** | **Chuẩn tối ưu:** Tốc độ so khớp $\mathcal{O}(1)$, bộ nhớ cực thấp, kháng biến đổi nén JPEG và nhiễu rất mạnh. |
| **$16 \times 16$** | **256 bits** | **64 ký tự** | Độ phân giải đặc trưng cao hơn, nhận diện tốt các biến đổi nhỏ nhưng nhạy cảm hơn với nhiễu. |
| **$32 \times 32$** | **1024 bits** | **256 ký tự** | Thường dùng cho các bài toán phân loại chi tiết cấu trúc hạt/vân ảnh (Texture analysis). |

---

### 3. Chuyển đổi hệ số lượng tử thành mã nhị phân và chuỗi Hexadecimal

Quy trình chuyển đổi từ ma trận hệ số 2D sang mã băm hoàn chỉnh gồm 3 bước:
```text
[ Ma trận LL 2D (8x8) ]
       │
       ▼ (So sánh với Median)
[ Ma trận Nhị phân {0, 1} (8x8) ]
       │
       ▼ (Làm phẳng ma trận / Flatten)
[ Vector Nhị phân 1D (64 bits) ]
       │
       ▼ (Gom nhóm 4-bit thành 1 ký tự Hex)
[ Chuỗi Hexadecimal (16 ký tự) ]
```

* **Bước 1 - Lập bản đồ nhị phân (Binary Mapping):**  
  So sánh từng phần tử với ngưỡng trung vị để tạo ma trận nhị phân $B \in \{0, 1\}^{8 \times 8}$.

* **Bước 2 - Làm phẳng vector (Flattening):**  
  Chuyển ma trận $B$ thành vector nhị phân 1D có độ dài 64 phần tử theo thứ tự quét dòng (*row-major order*):
  $$\mathbf{h}_{bin} = [b_0, b_1, b_2, \dots, b_{63}]$$

* **Bước 3 - Mã hóa Hexadecimal:**  
  Gom từng khối 4-bit liên tiếp ($b_i \dots b_{i+3}$) thành một chữ số cơ số 16 (Hex character) để tối ưu không gian lưu trữ cơ sở dữ liệu:
  $$\text{Hex\_digit} = \sum_{j=0}^{3} b_{i+j} \cdot 2^{3-j} \quad (i = 0, 4, 8, \dots, 60)$$

---

### 4. Bản chất và Công thức Khoảng cách Hamming (Hamming Distance)

Khoảng cách Hamming ($D_H$) giữa hai chuỗi nhị phân có cùng độ dài là số lượng vị trí bit mà tại đó giá trị của hai chuỗi khác nhau. Trong bài toán so sánh mã băm cảm nhận (Perceptual Hash), khoảng cách Hamming phản ánh mức độ biến đổi về mặt thị giác giữa hai hình ảnh.

### a. Công thức toán học
Cho hai vector mã băm nhị phân $\mathbf{h}_1, \mathbf{h}_2 \in \{0, 1\}^N$ có cùng độ dài $N$ bits:

$$D_H(\mathbf{h}_1, \mathbf{h}_2) = \sum_{i=1}^{N} (\mathbf{h}_1[i] \oplus \mathbf{h}_2[i]) = \sum_{i=1}^{N} \mathbb{I}(\mathbf{h}_1[i] \neq \mathbf{h}_2[i])$$

*Trong đó:*
*   $\oplus$: Phép toán logic XOR (trả về $1$ nếu hai bit khác nhau, $0$ nếu hai bit giống nhau).
*   $\mathbb{I}$: Hàm chỉ thị (Indicator function), nhận giá trị $1$ khi điều kiện đúng và $0$ khi điều kiện sai.

'''### b. Cài đặt trên mã nguồn Python
```python
# Cách 1: Sử dụng phép so sánh mảng trực tiếp của NumPy
diff_bits = np.sum(hash1 != hash2)

# Cách 2: Sử dụng phép toán logic XOR và đếm số phần tử khác không
diff_bits = np.count_nonzero(hash1 ^ hash2)
```
---
### 5. Ngưỡng quyết định tương đồng (Decision Threshold)

Mức độ khác biệt giữa hai ảnh được chuẩn hóa qua **Tỉ lệ lỗi bit (Bit Error Rate - BER)**:

$$\text{BER} = \frac{D_H(\mathbf{h}_1, \mathbf{h}_2)}{N}$$

Độ tương đồng phần trăm giữa hai ảnh được tính theo công thức:

$$\text{Similarity (\%)} = \left(1 - \frac{D_H}{N}\right) \times 100\%$$

Với chuẩn mã băm Wavelet 64-bit ($N = 64$), các tiêu chuẩn phân loại được thiết lập như sau:

* **Ngưỡng tương đồng ($\text{BER} \le 10\% \iff D_H \le 6\text{ bits}$):**  
  Hai ảnh được xác nhận là cùng một nội dung (độ tương đồng $\ge 90.62\%$). Sự sai lệch nhỏ ($1 - 6\text{ bits}$) chỉ do các biến đổi không làm mất cấu trúc như: nén JPEG, tăng/giảm độ sáng nhẹ, thay đổi tỉ lệ kích thước (resize), hoặc làm mịn ảnh.

* **Vùng nghi vấn ($10\% < \text{BER} \le 25\% \iff 7 \le D_H \le 16\text{ bits}$):**  
  Hai ảnh là biến thể của nhau (cùng bố cục nhưng bị cắt xén một phần, chỉnh sửa màu sắc cục bộ, hoặc bị chèn watermark lớn).

* **Ngưỡng khác biệt ($\text{BER} \approx 50\% \iff D_H \ge 25\text{ bits}$):**  
  Phân bố bit giữa hai chuỗi là độc lập ngẫu nhiên ($P(\mathbf{h}_1[i] \neq \mathbf{h}_2[i]) \approx 0.5$). Hệ thống kết luận hai ảnh hoàn toàn khác nhau.
---
### 6. Thực nghiệm minh họa trên các cặp ảnh mẫu (Mã băm 64-bit)

Thực nghiệm được ghi nhận trực tiếp từ mã nguồn thực thi trên tập dữ liệu ảnh kiểm thử:

---

#### Cặp 1: Ảnh gốc (`meme.jpg`) vs Biến thể nén/chỉnh sửa (`memetest.jpg`)

* **Mô tả:** Kiểm tra độ tương đồng giữa ảnh gốc và ảnh đã qua chỉnh sửa.
* **Mã băm Hexadecimal (64-bit):**
  * $\mathbf{h}_{\text{meme}}\text{ [OpenCV]}: \texttt{ffffffffff99ffff}$
  * $\mathbf{h}_{\text{memetest}}\text{ [OpenCV]}: \texttt{11243d7c7c7d3c78}$
  * $\mathbf{h}_{\text{meme}}\text{ [PIL]}: \texttt{ffffffffff99ffff}$
  * $\mathbf{h}_{\text{memetest}}\text{ [PIL]}: \texttt{1124be7c7c7c3878}$
* **Khoảng cách Hamming:**
  * Trên OpenCV: $D_H = 33 / 64\text{ bits}$ ($\text{BER} = 51.56\%$)
  * Trên PIL: $D_H = 34 / 64\text{ bits}$ ($\text{BER} = 53.12\%$)
* **Độ tương đồng:** $48.44\%\text{ (OpenCV)} \ / \ 46.88\%\text{ (PIL)}$
* **Kết luận hệ thống:** **KHÁC NHAU (Mismatch)**

---

#### Cặp 2: Ảnh gốc (`meme.jpg`) vs Biến thể làm mờ Gauss và thêm nhiễu hạt

* **Mô tả:** Kiểm tra độ bền vững trước nhiễu hạt nhân tạo và làm mờ Gaussian Filter.
* **Mã băm Hexadecimal (64-bit):**
  * $\mathbf{h}_{\text{meme}}: \texttt{ffffffffff99ffff}$
  * $\mathbf{h}_{\text{noisy}}: \text{(Mã băm phân rã sau nhiễu)}$
* **Khoảng cách Hamming:** $D_H = 32 / 64\text{ bits}$ ($\text{BER} = 50.00\%$)
* **Độ tương đồng:** $50.00\%$
* **Kết luận hệ thống:** **KHÁC NHAU (Mismatch)**

---

#### Cặp 3: Ảnh gốc (`meme.jpg`) vs Ảnh gradient đối chứng khác loại

* **Mô tả:** Kiểm tra khả năng phân tách giữa hai mẫu ảnh hoàn toàn độc lập về mặt cấu trúc.
* **Mã băm Hexadecimal (64-bit):**
  * $\mathbf{h}_{\text{meme}}: \texttt{ffffffffff99ffff}$
  * $\mathbf{h}_{\text{diff}}: \text{(Mã băm ma trận Gradient)}$
* **Khoảng cách Hamming:** $D_H = 32 / 64\text{ bits}$ ($\text{BER} = 50.00\%$)
* **Độ tương đồng:** $50.00\%$
* **Kết luận hệ thống:** **KHÁC NHAU (Mismatch)**
---
### 7. Bảng tổng hợp thực nghiệm

| Phép thử kiểm định | Cặp ảnh so sánh | Mã băm Hexadecimal | Khoảng cách $D_H$ | Tỉ lệ lỗi BER | Độ tương đồng (%) | Đánh giá hệ thống |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Cặp 1 (OpenCV)** | Gốc vs `memetest.jpg` | `ffffffffff99ffff`<br>`11243d7c7c7d3c78` | **$33 / 64$** | **$51.56\%$** | **$48.44\%$** | **KHÁC NHAU (Mismatch)** |
| **Cặp 1 (PIL)** | Gốc vs `memetest.jpg` | `ffffffffff99ffff`<br>`1124be7c7c7c3878` | **$34 / 64$** | **$53.12\%$** | **$46.88\%$** | **KHÁC NHAU (Mismatch)** |
| **Cặp 2** | Gốc vs Làm mờ + Nhiễu | `ffffffffff99ffff`<br>*(Phân rã sau lọc)* | **$32 / 64$** | **$50.00\%$** | **$50.00\%$** | **KHÁC NHAU (Mismatch)** |
| **Cặp 3** | Gốc vs Ảnh gradient khác loại | `ffffffffff99ffff`<br>*(Ma trận đối chứng)* | **$32 / 64$** | **$50.00\%$** | **$50.00\%$** | **KHÁC NHAU (Mismatch)** |

---

### 8. Phân tích nguyên nhân và Biện luận kết quả thực nghiệm

Kết quả thực nghiệm ghi nhận hiện tượng bất thường khi tất cả các cặp ảnh (kể cả Cặp 1 và Cặp 2 vốn là biến thể của nhau) đều cho khoảng cách Hamming xấp xỉ $32 - 34\text{ bits}$ ($\text{BER} \approx 50\%$). Dưới góc độ xử lý ảnh số, hiện tượng này được giải thích như sau:

* **Hiện tượng bão hòa bit 1 (Bit Saturation):**  
  Mã băm của ảnh gốc `meme.jpg` có giá trị `ffffffffff99ffff`, tương đương với chuỗi nhị phân chứa 60 bit 1 và chỉ có 4 bit 0. Điều này vi phạm nguyên tắc phân bố entropy tối đa của mã băm cảm nhận (vốn yêu cầu phân bố cân bằng $\approx 32\text{ bit 0}$ và $32\text{ bit 1}$).

* **Ảnh hưởng của nền đơn sắc và cơ chế ngưỡng Trung vị (Median Thresholding):**  
  Ảnh dạng đồ họa / meme thường có diện tích mảng màu phẳng đơn sắc (nền trắng hoặc đen thuần túy) chiếm hơn $60\%$ tổng diện tích. Khi đó, giá trị trung vị $\text{Median}(LL)$ bằng chính giá trị của vùng nền. Phép so sánh $LL \ge \text{Median}$ làm cho toàn bộ vùng nền bị chuyển thành bit 1, làm mất tính đại diện của các đặc trưng tần số thấp.

* **Sự sai lệch khoảng cách Hamming:**  
  Khi ảnh $\mathbf{h}_1$ bị bão hòa toàn bit 1, bất kỳ ảnh biến thể $\mathbf{h}_2$ nào có phân bố bit chuẩn ($50\%$ bit 0, $50\%$ bit 1) khi so sánh XOR đều sẽ cho ra khoảng cách $D_H \approx 32\text{ bits}$, dẫn đến kết luận sai lệch là "Khác nhau".

* **Hướng tối ưu hóa:**  
  Để thuật toán wHash hoạt động chuẩn xác trên các loại ảnh có diện tích nền phẳng lớn, cần thay thế ngưỡng trung vị cục bộ bằng **ngưỡng trung bình cộng ($\text{Mean}$)** hoặc áp dụng cân bằng lược đồ mức xám (**Histogram Equalization**) trước khi phân rã Wavelet.