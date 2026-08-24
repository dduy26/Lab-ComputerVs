# KẾ HOẠCH THỰC HIỆN DỰ ÁN & ÁP DỤNG HÀM CHI TIẾT (LAB-CHAP3P2)

> **Dự án:** `Lab-chap3p2`  
> **Chủ đề:** So sánh sự tương đồng của các hình ảnh sử dụng Wavelet Hash (wHash)  
> **Tệp thực thi:** [`notebook/code.py`](file:///d:/X%E1%BB%AD%20l%C3%AD%20%E1%BA%A3nh/FileGit/Lab-ComputerVs/Lab-chap3p2/notebook/code.py) | **Báo cáo lý thuyết:** [`docs/lythuyet.md`](file:///d:/X%E1%BB%AD%20l%C3%AD%20%E1%BA%A3nh/FileGit/Lab-ComputerVs/Lab-chap3p2/docs/lythuyet.md)

---

## 📌 BẢNG ÁP DỤNG HÀM KỸ THUẬT THEO CÁC BƯỚC (FUNCTIONS MAPPING PLAN)

Dưới đây là kế hoạch chi tiết từng bước xử lý, mục tiêu kỹ thuật tương ứng và **tên hàm/phương pháp cụ thể được sử dụng kèm ví dụ code**:

```
[B1: Đọc & Chuẩn hóa Ảnh] ──► [B2: Khử Nhiễu & Biến Đổi Wavelet] ──► [B3: Lượng Tử Hóa Median]
          │                                  │                                   │
  cv2.imdecode / PIL                  pywt.wavedec2                       np.median
          │                                  │                                   │
          ▼                                  ▼                                   ▼
[B6: Trực Quan Hóa Subplots] ◄── [B5: Khoảng Cách Hamming] ◄── [B4: Duỗi Bit & Mã Hex]
        plt.subplots                  np.count_nonzero                   flatten / hex
```

---

### 1️⃣ Bước 1: Nạp ảnh & Tiền xử lý hình ảnh (Image Loading & Preprocessing)

* **Mục tiêu 1.1: Đọc ảnh an toàn hỗ trợ đường dẫn tiếng Việt trên Windows**
  * *Mục đích:* Tránh lỗi OpenCV `imread()` bị thất bại khi đường dẫn có chứa ký tự tiếng Việt có dấu (như `Xử lí ảnh`).
  * *Hàm sử dụng:* Kết hợp `np.fromfile()` và `cv2.imdecode()` cho OpenCV, hoặc `Image.open()` cho PIL.
  * *Ví dụ Code:*
    ```python
    # OpenCV hỗ trợ Unicode path:
    img_array = np.fromfile(full_path, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    # PIL / Pillow:
    img = Image.open(full_path)
    ```

* **Mục tiêu 1.2: Chuyển đổi không gian màu sang ảnh mức xám (Grayscale)**
  * *Mục đích:* Loại bỏ thông tin màu sắc (RGB/BGR), chỉ giữ lại thông tin độ xám cường độ sáng để phân tích cấu trúc.
  * *Hàm sử dụng:* `cv2.cvtColor()` (OpenCV) hoặc `img.convert('L')` (PIL).
  * *Ví dụ Code:*
    ```python
    # OpenCV:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # PIL:
    gray = img.convert('L')
    ```

* **Mục tiêu 1.3: Chuẩn hóa kích thước hình ảnh (Image Resizing)**
  * *Mục đích:* Đưa tất cả ảnh đầu vào về cùng một độ phân giải cố định ($256 \times 256$).
  * *Hàm sử dụng:* `cv2.resize()` với nội suy `cv2.INTER_AREA` (OpenCV) hoặc `img.resize()` với `LANCZOS` (PIL).
  * *Ví dụ Code:*
    ```python
    # OpenCV:
    resized = cv2.resize(gray, (256, 256), interpolation=cv2.INTER_AREA)
    
    # PIL:
    resized = gray.resize((256, 256), Image.Resampling.LANCZOS)
    ```

---

### 2️⃣ Bước 2: Khử nhiễu & Phân tách tần số Wavelet (Wavelet Decomposition & Denoising)

* **Mục tiêu 2.1: Phân tách tần số & Lọc nhiễu chi tiết cao**
  * *Mục đích:* Cần phân tích ảnh thành các băng tần tần số và khử nhiễu hạt/nhiễu biên không cần thiết.
  * *Hàm sử dụng:* Biến đổi Wavelet 2D nhiều cấp `pywt.wavedec2()` từ thư viện PyWavelets (`pywt`).
  * *Ví dụ Code:*
    ```python
    # Phân tách Wavelet 2D 3 cấp với hàm cơ sở 'haar' hoặc 'db4'
    coeffs = pywt.wavedec2(img_array, wavelet='haar', level=3)
    ```

* **Mục tiêu 2.2: Trích xuất băng tần tần số thấp LL (Approximation Sub-band)**
  * *Mục đích:* Lấy phần dữ liệu xấp xỉ tần số thấp LL — nơi chứa năng lượng chính và cấu trúc cơ bản của bức ảnh.
  * *Hàm sử dụng:* Trích xuất phần tử đầu tiên của danh sách hệ số `coeffs[0]`, sau đó resize ma trận LL về kích thước mã băm $8 \times 8$.
  * *Ví dụ Code:*
    ```python
    ll_coeffs = coeffs[0]  # Băng tần LL (Low-Low)
    ll_resized = cv2.resize(ll_coeffs, (8, 8), interpolation=cv2.INTER_AREA)
    ```

---

### 3️⃣ Bước 3: Lượng tử hóa hệ số (Quantization)

* **Mục tiêu 3.1: Giảm độ chính xác liên tục và triệt tiêu biến đổi ánh sáng**
  * *Mục đích:* Cần biến các hệ số số thực liên tục thành các giá trị nhị phân rời rạc ($0$ và $1$) bền vững trước biến đổi độ sáng/độ tương phản.
  * *Hàm sử dụng:* Tính trung vị `np.median()` và so sánh ngưỡng nhị phân `(ll_resized >= median_val).astype(int)`.
  * *Ví dụ Code:*
    ```python
    median_val = np.median(ll_resized)
    quantized_matrix = (ll_resized >= median_val).astype(int)
    ```

---

### 4️⃣ Bước 4: Tạo mã băm nhị phân & Hexadecimal (Hash Code Generation)

* **Mục tiêu 4.1: Duỗi thẳng ma trận nhị phân 2D và đóng gói mã Hex**
  * *Mục đích:* Chuyển ma trận $8 \times 8$ thành chuỗi 64-bit nhị phân 1D và nén thành mã Hex 16 ký tự.
  * *Hàm sử dụng:* `matrix.flatten()`, phép dịch bit `<<` và hàm `hex()`.
  * *Ví dụ Code:*
    ```python
    binary_hash = quantized_matrix.flatten()  # 64 bits nhị phân
    
    # Mã hóa Hexadecimal:
    hex_hash = ""
    for i in range(0, len(binary_hash), 4):
        chunk = binary_hash[i:i+4]
        digit = sum(b << (3 - idx) for idx, b in enumerate(chunk))
        hex_hash += hex(digit)[2:]
    ```

---

### 5️⃣ Bước 5: So sánh độ tương đồng (Similarity Comparison)

* **Mục tiêu 5.1: Đếm số bit khác biệt giữa 2 mã băm**
  * *Mục đích:* Cần tính độ khoảng cách giữa 2 bức ảnh để kết luận chúng giống hay khác nhau.
  * *Hàm sử dụng:* Khoảng cách Hamming `np.count_nonzero(hash1 != hash2)`.
  * *Ví dụ Code:*
    ```python
    diff_bits = np.count_nonzero(b1 != b2)
    similarity_pct = (1.0 - diff_bits / len(b1)) * 100.0
    ```

---

### 6️⃣ Bước 6: Trực quan hóa & Lưu biểu đồ đồ họa (Visualization & Output)

* **Mục tiêu 6.1: Phân tách 4 băng tần cấp 1 và vẽ đồ thị 6 subplots**
  * *Mục đích:* Hiển thị trực quan cho người dùng toàn bộ quá trình biến đổi.
  * *Hàm sử dụng:* `pywt.dwt2()` cho cấp 1, `plt.subplots(2, 3)` để tạo lưới đồ họa, `plt.savefig()` để lưu ảnh ra file png, và `plt.close()` để tránh nghẽn luồng GUI.
  * *Ví dụ Code:*
    ```python
    LL, (LH, HL, HH) = pywt.dwt2(img_gray, 'haar')
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    # ... vẽ 6 ô ...
    plt.savefig("data/output/wavelet_hash_visualization_cv2.png", dpi=150)
    plt.close()
    ```

---

## 📊 KẾT QUẢ VẬN HÀNH DỰ KIẾN (ACCEPTANCE CRITERIA)
1. **Chạy không lỗi:** Chạy `python code.py` thực thi 100% không phát sinh lỗi ngoại lệ `FileNotFoundError` hay `UnicodeEncodeError`.
2. **Xuất đủ kết quả:** In ra mã băm Hex 64-bit, Khoảng cách Hamming, và Đánh giá sự tương đồng.
3. **Lưu file đầu ra:** Xuất hình ảnh trực quan hóa đầy đủ tại `data/output/wavelet_hash_visualization_cv2.png`.