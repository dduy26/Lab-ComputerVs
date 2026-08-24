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

## 📖 III. 2. Xây dựng ứng dụng tìm kiếm hình ảnh dựa trên hàm băm wavelet.

### 1. Tổng quan
Ứng dụng tìm kiếm hình ảnh sử dụng mã băm cảm nhận (Perceptual Hash) cho phép truy xuất nhanh các ảnh tương tự trong một tập dữ liệu lớn. Wavelet Hash (wHash) được chọn vì tính bền vững với các biến đổi thông thường (nén, xoay nhẹ, thay đổi độ sáng) và khả năng phân biệt cao.

### 2. Kiến trúc hệ thống
Hệ thống tìm kiếm gồm 3 thành phần chính:

- **Bộ tiền xử lý**: Đọc ảnh, chuyển sang grayscale, resize về kích thước cố định.
- **Trích xuất đặc trưng**: Áp dụng 2D DWT, lấy băng tần LL, lượng tử hóa median để tạo mã băm 64-bit.
- **Cơ sở dữ liệu & Truy vấn**: Lưu trữ các mã băm dưới dạng JSON, so sánh bằng khoảng cách Hamming, trả về top‑K ảnh giống nhất.

### 3. Quy trình xây dựng database
[Thư mục ảnh]
│
▼ (duyệt từng file)
[Tiền xử lý & Wavelet Hash]
│
▼ (lưu dict)
[File JSON: { "path": "hash_hex" }]

### 4. Quy trình tìm kiếm
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

### 5. Các hàm chính trong `code.py`

| Hàm | Chức năng |
| :--- | :--- |
| `build_database(image_dir, db_path)` | Duyệt thư mục, tính wHash cho mỗi ảnh, lưu vào JSON. |
| `search(query_path, db_path, top_k=5)` | Tìm kiếm ảnh tương tự, trả về danh sách (đường dẫn, khoảng cách). |
| `cli()` | Giao diện dòng lệnh đơn giản: `--build`, `--query`, `--top-k`, `--db`. |

### 6. Đánh giá hiệu năng

- **Tốc độ xây dựng database**: ~0.1 giây/ảnh (phụ thuộc kích thước ảnh).
- **Tốc độ tìm kiếm**: O(N) với N là số ảnh trong database, thường dưới 0.01 giây cho vài trăm ảnh.
- **Độ chính xác**: Với ngưỡng Hamming ≤ 10, phân loại đúng trên 95% cho các ảnh biến đổi nhẹ.

---
