# PHẦN I.2 & III.2: PHÂN TÍCH THAM SỐ VÀ CẢI THIỆN HIỆU SUẤT CANNY EDGE DETECTOR

> **Thành viên thực hiện:** Thọ  
> **Nhiệm vụ:**  
> - **Phần I.2 (a + b):** Các tham số của thuật toán Canny và ảnh hưởng của chúng (Sigma $\sigma$, Ngưỡng thấp $T_{\text{low}}$, Ngưỡng cao $T_{\text{high}}$).  
> - **Phần III.2:** Các phương pháp cải thiện hiệu suất của thuật toán Canny.

---

## 📌 PHẦN I.2: CÁC THAM SỐ CỦA THUẬT TOÁN CANNY VÀ ẢNH HƯỞNG CỦA CHÚNG

Thuật toán phát hiện cạnh Canny (Canny Edge Detector) sở dĩ đạt hiệu quả cao và được ứng dụng rộng rãi là nhờ khả năng tinh chỉnh linh hoạt thông qua 3 tham số cốt lõi:
1. Độ lệch chuẩn $\sigma$ (Sigma) của bộ lọc Gaussian.
2. Ngưỡng thấp ($T_{\text{low}}$ - Low Threshold).
3. Ngưỡng cao ($T_{\text{high}}$ - High Threshold).

---

### 1. Tham số $\sigma$ (Sigma) trong bộ lọc Gaussian Filter

#### a. Khái niệm và Vai trò
Ở bước đầu tiên của thuật toán Canny, bộ lọc Gaussian 2D được áp dụng để khử nhiễu (noise reduction) và làm mịn ảnh. Hàm mật độ xác suất Gaussian 2D được định nghĩa bởi công thức:

$$G(x, y) = \frac{1}{2\pi\sigma^2} \exp\left(-\frac{x^2 + y^2}{2\sigma^2}\right)$$

Trong đó:
- $\sigma$ (Sigma) là độ lệch chuẩn (standard deviation), điều khiển mức độ trải rộng của đồ thị hình chuông Gaussian.
- Kích thước ma trận bộ lọc (Kernel size $N \times N$) thường được chọn tỉ lệ thuận với $\sigma$ theo quy tắc $N \approx \lceil 6\sigma \rceil + 1$ (làm tròn thành số lẻ).

#### b. Phân tích tác động của $\sigma$

| Giá trị $\sigma$ | Tác động đến ảnh & cạnh | Ưu điểm | Nhược điểm |
| :--- | :--- | :--- | :--- |
| **$\sigma$ nhỏ** ($\sigma < 1.0$) | Ảnh ít bị làm mờ, vùng trải rộng của mặt nạ nhỏ. | - Giữ được chi tiết mịn, các đường biên mảnh.<br>- Định vị cạnh chính xác (Edge localization tốt). | - Rất nhạy cảm với nhiễu.<br>- Xuất hiện nhiều cạnh giả (False Positives) do nhiễu hạt/nhiễu xám gây ra. |
| **$\sigma$ vừa** ($1.0 \le \sigma \le 2.0$) | Mức độ làm mờ vừa phải, cân bằng tốt giữa lọc nhiễu và bảo toàn biên. | - Khử nhiễu hiệu quả.<br>- Phát hiện được đa số cạnh chính của vật thể. | - Giá trị chuẩn mặc định thường được ưu tiên trong xử lý ảnh thông thường. |
| **$\sigma$ lớn** ($\sigma > 3.0$) | Ảnh bị làm mờ rất mạnh, mất các chi tiết xám tần số cao. | - Loại bỏ triệt để nhiễu nặng và các hoa văn/kết cấu phức tạp (texture). | - Làm mờ và mất các cạnh yếu, chi tiết nhỏ.<br>- Cạnh bị xê dịch vị trí (Edge displacement).<br>- Các cạnh gần nhau dễ bị hòa tan thành một. |

#### c. Kết luận & Trade-off đối với $\sigma$
Lựa chọn $\sigma$ là sự đánh đổi (trade-off) giữa **Khả năng chống nhiễu (Noise suppression)** và **Độ chính xác định vị cạnh (Localization precision)**. Ảnh có nhiều nhiễu đòi hỏi $\sigma$ lớn hơn; ngược lại, ảnh cần trích xuất chi tiết sắc nét yêu cầu $\sigma$ nhỏ hơn.

---

### 2. Ngưỡng thấp ($T_{\text{low}}$) và Ngưỡng cao ($T_{\text{high}}$) trong Lọc ngưỡng kép (Double Thresholding)

#### a. Khái niệm và Quy trình phân loại
Sau khi tính độ lớn Gradient $M(x, y)$ và áp dụng Triệt tiêu phi cực đại (NMS), Canny sử dụng 2 ngưỡng ($T_{\text{low}}$ và $T_{\text{high}}$) để phân loại các điểm ảnh điểm cực đại thành 3 nhóm:

$$\text{Pixel Type}(x,y) = \begin{cases} 
\text{Cạnh mạnh (Strong Edge)} & \text{nếu } M(x,y) \ge T_{\text{high}} \\
\text{Cạnh yếu (Weak Edge)} & \text{nếu } T_{\text{low}} \le M(x,y) < T_{\text{high}} \\
\text{Không phải cạnh (Non-edge)} & \text{nếu } M(x,y) < T_{\text{low}}
\end{cases}$$

- **Cạnh mạnh:** Chắc chắn là đường biên chuẩn.
- **Cạnh yếu:** Được xét tuyển qua cơ chế **Theo dõi cạnh (Hysteresis Edge Tracking)**. Nếu cạnh yếu có kết nối 8-hướng (8-connectivity) với ít nhất một cạnh mạnh, nó được nâng cấp thành cạnh chính thức. Ngược lại, nếu cô lập, nó sẽ bị loại bỏ.

#### b. Phân tích tác động của $T_{\text{high}}$ và $T_{\text{low}}$

##### 🔹 Ảnh hưởng của Ngưỡng cao ($T_{\text{high}}$):
- **Khi $T_{\text{high}}$ quá cao:** Chỉ những pixel có sự biến đổi độ xám cực kỳ đột ngột mới được chọn làm cạnh mạnh.
  - *Hệ quả:* Thiếu hụt các cạnh mạnh hạt nhân $\rightarrow$ Chuỗi liên kết Hysteresis không khởi tạo được $\rightarrow$ Đường biên bị đứt đoạn nghiêm trọng hoặc mất hoàn toàn.
- **Khi $T_{\text{high}}$ quá thấp:** Nhiều điểm biến đổi độ xám trung bình/nhẹ bị nhận lầm là cạnh mạnh.
  - *Hệ quả:* Nạp thêm nhiều đường nét thừa, nhiễu nền bị biến thành cạnh chính thức.

##### 🔹 Ảnh hưởng của Ngưỡng thấp ($T_{\text{low}}$):
- **Khi $T_{\text{low}}$ quá thấp:** Ngưỡng lọc quá lỏng lẻo.
  - *Hệ quả:* Giữ lại vô số cạnh yếu do nhiễu gây ra. Nếu nhiễu vô tình đứng cạnh một cạnh mạnh, nó sẽ bị nối chuỗi vào đường biên, tạo nên các "râu" cạnh nhiễu (noise artifacts).
- **Khi $T_{\text{low}}$ quá cao ($T_{\text{low}} \to T_{\text{high}}$):** Không còn khoảng không cho cạnh yếu.
  - *Hysteresis mất tác dụng:* Các đoạn cạnh mờ nối giữa 2 cạnh mạnh bị loại bỏ, dẫn đến rách biên.

#### c. Tỷ lệ khuyến nghị giữa $T_{\text{high}}$ và $T_{\text{low}}$
Theo công trình gốc của John F. Canny, tỷ lệ tối ưu giữa ngưỡng cao và ngưỡng thấp thường nằm trong khoảng **$2:1$ đến $3:1$**.
- Ví dụ phổ biến: $(T_{\text{low}}=50, T_{\text{high}}=150)$ hoặc $(T_{\text{low}}=100, T_{\text{high}}=200)$.

---

## 📌 PHẦN III.2: CÁC PHƯƠNG PHÁP CẢI THIỆN HIỆU SUẤT CỦA THUẬT TOÁN CANNY

Mặc dù Canny truyền thống rất hiệu quả, nó vẫn tồn tại một số hạn chế như: phụ thuộc vào tham số cố định, nhạy cảm với nhiễu phi Gauss, làm mờ biên do bộ lọc Gaussian, và chi phí tính toán cao trên ảnh lớn. Dưới đây là các phương pháp cải tiến hiện đại:

### 1. Tự động hóa & Thích ứng Ngưỡng (Adaptive Thresholding)

- **Vấn đề:** Thiết lập $T_{\text{low}}, T_{\text{high}}$ thủ công cố định không thể tối ưu cho mọi bức ảnh hoặc ảnh có vùng sáng tối lệch nhau.
- **Giải pháp cải tiến:**
  1. **Phương pháp Otsu-Canny:** Sử dụng thuật toán Otsu để tìm ngưỡng phân đoạn độ xám tối ưu $T_{\text{Otsu}}$ của ảnh, sau đó đặt:
     $$T_{\text{high}} = T_{\text{Otsu}}, \quad T_{\text{low}} = 0.5 \times T_{\text{high}}$$
  2. **Phương pháp dựa trên Median (Median-based Canny):**
     Tính trung vị độ xám $v = \text{median}(I)$ của ảnh, xác định ngưỡng theo công thức tự động với tham số $\sigma_{\text{adapt}} \approx 0.33$:
     $$T_{\text{low}} = \max(0, (1 - \sigma_{\text{adapt}}) \cdot v)$$
     $$T_{\text{high}} = \min(255, (1 + \sigma_{\text{adapt}}) \cdot v)$$
  3. **Ngưỡng thích ứng theo vùng (Block-based / Local Adaptive Thresholding):** Chia ảnh thành các ô vuông nhỏ (blocks) và tính toán cặp ngưỡng riêng cho từng ô để xử lý ảnh có độ chiếu sáng không đều (non-uniform illumination).

---

### 2. Cải tiến Bộ lọc Tiền xử lý (Advanced Preserving Smoothing)

- **Vấn đề:** Bộ lọc Gaussian truyền thống làm mờ cả nhiễu lẫn độ sắc nét của đường biên, gây xê dịch vị trí cạnh.
- **Giải pháp cải tiến:**
  1. **Lọc song phương (Bilateral Filter):** Kết hợp cả khoảng cách không gian và sự tương đồng về mức xám. Khử nhiễu cực tốt ở vùng phẳng nhưng giữ nguyên độ dốc sắc nét tại đường biên.
  2. **Lọc khuếch tán không đẳng hướng (Anisotropic Diffusion Filter):** Làm mờ trong lòng vật thể nhưng dừng lại tại các đường biên, giúp bảo toàn cấu trúc mỏng.
  3. **Lọc hướng dẫn (Guided Filter) & Lọc trung vị (Median Filter):** Loại bỏ hiệu quả nhiễu hạt muối tiêu (Salt-and-Pepper) mà bộ lọc Gaussian không xử lý triệt để được.

---

### 3. Cải tiến Toán tử Gradient & Độ chính xác dưới Pixel (Sub-pixel Accuracy)

- **Vấn đề:** Toán tử Sobel $3 \times 3$ trong Canny nhạy với nhiễu tần số cao và ước lượng góc gradient có độ phân giải thô ($0^\circ, 45^\circ, 90^\circ, 135^\circ$).
- **Giải pháp cải tiến:**
  1. **Toán tử Scharr / Deriche Filter:** Sử dụng các ma trận làm mịn tối ưu hơn ($5 \times 5$ hoặc $7 \times 7$) giúp ước lượng hướng gradient chính xác hơn nhiều so với Sobel.
  2. **Định vị cạnh mức dưới Pixel (Sub-pixel Edge Detection):** Áp dụng nội suy Parabol hoặc Spline 2D tại vị trí cực đại NMS để xác định tọa độ cạnh với độ chính xác dưới $1.0 \text{ pixel}$ (rất quan trọng trong kiểm tra kích thước sản phẩm công nghiệp và đo lường y tế).

---

### 4. Tăng tốc Phần cứng & Tối ưu Thời gian thực (Hardware Acceleration)

- **Vấn đề:** Thuật toán Canny tính toán 5 bước liên tiếp trên CPU có thể bị nghẽn cổ chai khi xử lý video 4K hoặc ứng dụng xe tự lái thời gian thực.
- **Giải pháp cải tiến:**
  1. **Song song hóa trên GPU (OpenCV CUDA Canny):**
     Đẩy các bước Gaussian Blur, Sobel Gradient và NMS lên GPU với hàng ngàn nhân xử lý song song thông qua hàm `cv2.cuda.createCannyEdgeDetector()`, giúp tăng tốc độ lên $5\times - 20\times$.
  2. **Tối ưu hóa bảng tra (LUT) & Số nguyên (Fixed-point Arithmetic):** Thay thế các phép tính số thực chấm động (floating-point) bằng số nguyên và bảng tra trước (Look-Up Table) để tối ưu trên hệ thống nhúng (Embedded systems/ARM).

---

### 5. Kết hợp Học sâu (Deep Learning Hybrid Approaches)

- **Cải tiến:** Kết hợp các mạng thần kinh học sâu nhẹ (như HED - Holistically-Nested Edge Detection, BDCN) để nhận biết các đường biên mang ý nghĩa ngữ nghĩa (semantic edges), loại bỏ hoa văn nhiễu nền, sau đó dùng bước NMS và Hysteresis của Canny để trích xuất đường viền sắc nét 1-pixel.

---

## 📊 BẢNG TỔNG HỢP SO SÁNH NÂNG CAO HIỆU SUẤT CANNY

| Phương pháp cải tiến | Mục tiêu chính | Ưu điểm vượt trội | Phạm vi ứng dụng |
| :--- | :--- | :--- | :--- |
| **Otsu / Median Canny** | Tự động hóa tham số | Không cần chỉnh ngưỡng thủ công, thích ứng tốt | Hệ thống xử lý ảnh tự động |
| **Bilateral Filter + Canny** | Bảo toàn biên & Khử nhiễu | Biên sắc nét, không bị xê dịch vị trí | Xử lý ảnh y tế (MRI/X-ray), OCR |
| **Sub-pixel Interpolation** | Tăng độ chính xác vị trí | Độ chính xác $< 0.1 \text{ pixel}$ | Đo lường công nghiệp, thị giác máy |
| **OpenCV CUDA Canny** | Tăng tốc độ tính toán | Đạt $60+ \text{ FPS}$ ở độ phân giải 4K | Xe tự lái, Giám sát giao thông Video |

---
