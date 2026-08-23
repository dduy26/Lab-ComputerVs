# PHẦN IV: THAM KHẢO & THỰC HÀNH BĂM HÌNH ẢNH WAVELET (WAVELET HASHING - wHash)

> **Dự án:** `Lab-chap3p2`  
> **Bài thực hành 4:** So sánh sự tương đồng của các hình ảnh sử dụng Wavelet, Python  
> **Tệp mã nguồn:** [`notebook/wavelet_hash.py`](file:///d:/X%E1%BB%AD%20l%C3%AD%20%E1%BA%A3nh/FileGit/Lab-ComputerVs/Lab-chap3p2/notebook/wavelet_hash.py)

---

## 📖 I. GIẢI THÍCH CHI TIẾT 3 BƯỚC CỦA THUẬT TOÁN WAVELET HASH (wHash)

Băm hình ảnh dựa trên Wavelet (Wavelet Perceptual Hashing - wHash) là kỹ thuật tạo ra một chuỗi nhị phân (mã băm - hash code) nhỏ gọn đại diện cho cấu trúc đặc trưng nội dung thị giác của hình ảnh. Không giống như các hàm băm mật mã học (như MD5, SHA-256 - chỉ cần 1 bit thay đổi sẽ làm thay đổi toàn bộ mã băm), mã băm percept (Perceptual Hash) có tính chất **bền vững (Robustness)**: hai bức ảnh giống nhau hoặc chỉ khác nhau do nén ảnh, biến đổi ánh sáng, cắt viền nhẹ sẽ cho ra hai mã băm cực kỳ gần nhau (khoảng cách Hamming nhỏ).

Quá trình tạo mã băm Wavelet bao gồm **3 bước chính**:

```
[Ảnh đầu vào] 
      │
      ▼ (Bước 1)
[Biến đổi Wavelet 2D (DWT)] ──► Phân tách 4 băng tần (LL, LH, HL, HH) ──► Trích xuất LL
      │
      ▼ (Bước 2)
[Lượng tử hóa hệ số (Quantization)] ──► So sánh hệ số LL với giá trị Trung vị (Median)
      │
      ▼ (Bước 3)
[Tạo mã băm Nhị phân (Binary Hash)] ──► Chuỗi Bit (64-bit / 256-bit) & Mã Hex ──► So sánh Hamming
```

---

### Bước 1: Biến đổi Wavelet (Phân tích tần số và không gian)

* **Nguyên lý:**
  Ảnh đầu vào (sau khi chuyển xám và resize về $256 \times 256$) được đưa qua phép biến đổi Wavelet rời rạc 2 chiều (2D Discrete Wavelet Transform - 2D DWT) bằng các hàm cơ sở như `haar` hoặc `db4` (Daubechies 4).
* **Phân tách băng tần (Sub-bands):**
  Phép biến đổi Wavelet phân tách ảnh thành 4 băng tần tần số ở cấp 1 (và tiếp tục phân tách băng tần LL ở các cấp tiếp theo):
  1. **Băng tần LL (Low-Low):** Băng tần xấp xỉ tần số thấp theo cả chiều ngang và chiều dọc. Đây là nơi tập trung **phần lớn năng lượng và cấu trúc hình học tổng thể** của hình ảnh.
  2. **Băng tần LH (Low-High):** Chứa các chi tiết biến đổi tần số cao theo chiều ngang (đường biên ngang).
  3. **Băng tần HL (High-Low):** Chứa các chi tiết biến đổi tần số cao theo chiều dọc (đường biên dọc).
  4. **Băng tần HH (High-High):** Chứa các chi tiết chéo và nhiễu tần số cao.
* **Tại sao lại dùng Băng tần LL để tạo mã băm?**
  Băng tần **LL** lưu giữ thông tin cốt lõi của hình ảnh mà mắt người cảm nhận được. Các chi tiết tần số cao (LH, HL, HH) rất dễ bị biến đổi hoặc mất đi khi nén JPEG hoặc lọc nhiễu, trong khi băng tần LL cực kỳ bền vững trước các tác động này.

---

### Bước 2: Lượng tử hóa hệ số (Quantization - Giảm độ chính xác)

* **Khái niệm Lượng tử hóa:**
  Các hệ số Wavelet thu được từ băng tần LL là các số thực chấm động (floating-point) liên tục có phạm vi biến thiên lớn. Lượng tử hóa là quá trình quy đổi các giá trị liên tục này về các mức rời rạc (discrete values), nhằm **giảm độ nhạy cảm đối với các biến động số học nhỏ**.
* **Phương pháp Lượng tử hóa dựa trên Trung vị (Median Thresholding):**
  1. Thu nhỏ ma trận băng tần LL về kích thước mã băm mong muốn $N \times N$ (ví dụ: $8 \times 8 = 64$ hệ số).
  2. Tính giá trị **Trung vị (Median)** của toàn bộ các hệ số trong ma trận $8 \times 8$:
     $$M = \text{median}(LL_{8 \times 8})$$
  3. Áp dụng hàm lượng tử hóa nhị phân:
     $$Q(i, j) = \begin{cases} 1 & \text{nếu } LL(i, j) \ge M \\ 0 & \text{nếu } LL(i, j) < M \end{cases}$$
* **Ý nghĩa:**
  Việc so sánh với giá trị trung vị đảm bảo phân bố số lượng bit `1` và `0` luôn cân bằng nhau (50% bit 1, 50% bit 0). Kỹ thuật này giúp loại bỏ ảnh hưởng của độ sáng tổng thể (brightness adjustment) hoặc độ tương phản (contrast modification).

---

### Bước 3: Tạo mã băm (Binary Hash Code & Hex Representation)

* **Chuyển đổi sang mã nhị phân:**
  Ma trận lượng tử hóa $Q$ kích thước $8 \times 8$ được duỗi thẳng (flatten) thành một mảng 1D gồm **64 bits nhị phân** ($0$ và $1$).
* **Biểu diễn chuỗi Hexadecimal:**
  Gom nhóm mỗi 4 bits nhị phân thành 1 ký tự lục giác (Hexadecimal digit) để thu được chuỗi Hex ngắn gọn độ dài 16 ký tự (ví dụ: `ffffffffff99ffff`).
* **So sánh độ tương đồng bằng Khoảng cách Hamming (Hamming Distance):**
  Để so sánh hai bức ảnh $A$ và $B$, ta tính khoảng cách Hamming giữa hai mã băm nhị phân $H_A$ và $H_B$:
  $$D_{\text{Hamming}} = \sum_{i=1}^{K} (H_A[i] \oplus H_B[i])$$
  * **Độ tương đồng (%):** $\text{Similarity} = \left(1 - \frac{D_{\text{Hamming}}}{K}\right) \times 100\%$
  * **Tiêu chí đánh giá:**
    * $D_{\text{Hamming}} = 0 \rightarrow 10$: Hai ảnh **Trùng lặp / Tương đồng cao** (Duplicate / Similar images).
    * $D_{\text{Hamming}} > 10$: Hai ảnh **Khác nhau** (Different images).

---

## 💻 II. THỰC HÀNH XỬ LÝ ÁNH ĐẦU VÀO VÀ HIỆN THỰC CODE PYTHON

### 1. Chuẩn hóa & Tiền xử lý ảnh đầu vào (OpenCV vs PIL)

Thuật toán xử lý ảnh đầu vào theo 3 bước chuẩn hóa:
1. **Nạp ảnh từ file:** Hỗ trợ cả 2 thư viện phổ biến **OpenCV (`cv2.imread`)** và **PIL (`Image.open`)**.
2. **Chuyển ảnh sang mức xám (Grayscale):** 
   - Với OpenCV: `cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)`
   - Với PIL: `img.convert('L')`
3. **Resize chuẩn hóa kích thước:** Đưa ảnh về kích thước cố định $256 \times 256$ pixel để đảm bảo cùng quy mô phân tích Wavelet.

### 2. Code Python Hoàn chỉnh (`notebook/wavelet_hash.py`)

```python
import os
import cv2
import numpy as np
import pywt
import matplotlib.pyplot as plt
from PIL import Image

def preprocess_image_cv2(image_path, target_size=(256, 256)):
    """Đọc ảnh bằng OpenCV, chuyển xám và resize chuẩn hóa."""
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Không thể đọc ảnh: {image_path}")
    if len(img.shape) == 3 and img.shape[2] == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    return cv2.resize(gray, target_size, interpolation=cv2.INTER_AREA)

def preprocess_image_pil(image_path, target_size=(256, 256)):
    """Đọc ảnh bằng PIL, chuyển xám và resize chuẩn hóa."""
    img = Image.open(image_path)
    gray = img.convert('L')
    return np.array(gray.resize(target_size, Image.Resampling.LANCZOS))

def wavelet_hash(img_array, wavelet='haar', level=3, hash_size=8):
    """
    Tính mã băm Wavelet (wHash):
    1. Phân tách Wavelet 2D
    2. Trích xuất băng tần LL & Lượng tử hóa theo Median
    3. Tạo chuỗi bit nhị phân & mã Hex
    """
    coeffs = pywt.wavedec2(img_array, wavelet=wavelet, level=level)
    ll_coeffs = coeffs[0]
    ll_resized = cv2.resize(ll_coeffs, (hash_size, hash_size), interpolation=cv2.INTER_AREA)
    
    # Lượng tử hóa theo giá trị Trung vị (Median)
    median_val = np.median(ll_resized)
    quantized_matrix = (ll_resized >= median_val).astype(int)
    binary_hash = quantized_matrix.flatten()
    
    # Chuyển mã nhị phân sang Hex
    hex_hash = ""
    for i in range(0, len(binary_hash), 4):
        chunk = binary_hash[i:i+4]
        digit = sum(b << (3 - idx) for idx, b in enumerate(chunk))
        hex_hash += hex(digit)[2:]
        
    return {
        "binary_hash": binary_hash,
        "hex_hash": hex_hash,
        "quantized_matrix": quantized_matrix,
        "ll_coeffs": ll_coeffs
    }

def hamming_distance(hash1, hash2):
    """Tính khoảng cách Hamming và phần trăm tương đồng giữa 2 mã băm."""
    b1, b2 = hash1["binary_hash"], hash2["binary_hash"]
    diff_bits = np.count_nonzero(b1 != b2)
    similarity_pct = (1.0 - diff_bits / len(b1)) * 100.0
    return diff_bits, similarity_pct
```

---

## 📊 III. KẾT QUẢ THỰC NGHIỆM TRÊN DỮ LIỆU THỰC TẾ

Khi chạy file thực thi [`notebook/wavelet_hash.py`](file:///d:/X%E1%BB%AD%20l%C3%AD%20%E1%BA%A3nh/FileGit/Lab-ComputerVs/Lab-chap3p2/notebook/wavelet_hash.py) với 2 ảnh mẫu trong thư mục `data/input/meme.jpg` và `data/input/memetest.jpg`:

```text
======================================================================
THỰC HÀNH BĂM HÌNH ẢNH WAVELET (WAVELET HASHING) - BÀI THỰC HÀNH 4
======================================================================

[1] XỬ LÝ ẢNH ĐẦU VÀO BẰNG OPENCV...
[2] XỬ LÝ ẢNH ĐẦU VÀO BẰNG PIL (PILLOW)...

--------------------------------------------------
KẾT QUẢ MÃ BĂM WAVELET HASH (64-BIT):
--------------------------------------------------
Ảnh 1 (meme.jpg) [OpenCV]:     ffffffffff99ffff
Ảnh 2 (memetest.jpg) [OpenCV]: 11243d7c7c7d3c78
Ảnh 1 (meme.jpg) [PIL]:        ffffffffff99ffff
Ảnh 2 (memetest.jpg) [PIL]:    1124be7c7c7c3878

--------------------------------------------------
KẾT QUẢ SO SÁNH SỰ TƯƠNG ĐỒNG (HAMMING DISTANCE):
--------------------------------------------------
[OpenCV] Khoảng cách Hamming: 33 / 64 bits | Độ tương đồng: 48.44%
[PIL]    Khoảng cách Hamming: 34 / 64 bits | Độ tương đồng: 46.88%
=> ĐÁNH GIÁ: Hai hình ảnh KHÁC NHAU!

[3] TRỰC QUAN HÓA TOÀN BỘ BẰNG BIỂU ĐỒ...
[+] Đã lưu biểu đồ trực quan hóa tại: data/output/wavelet_hash_visualization_cv2.png
```

---

## 🖼️ IV. ĐÁNH GIÁ HÌNH ẢNH TRỰC QUAN HÓA

Biểu đồ xuất ra tại `data/output/wavelet_hash_visualization_cv2.png` minh họa rõ 6 giai đoạn:
1. **Ảnh mức xám $256 \times 256$**: Ảnh đầu vào được chuẩn hóa màu và kích thước.
2. **Băng tần LL (Low-Low)**: Lưu trữ nội dung xấp xỉ tần số thấp (năng lượng chính).
3. **Băng tần LH, HL, HH**: Lưu trữ các nét chi tiết đường biên ngang, dọc và chéo.
4. **Ma trận Lượng tử hóa $8 \times 8$**: Ma trận ô vuông đen-trắng ($0$ và $1$) đại diện mã băm nhị phân 64-bit.
