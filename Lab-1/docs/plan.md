# KẾ HOẠCH THỰC HIỆN, AUDIT CODEBASE & TỔNG HỢP NỘI DUNG DỰ ÁN (LAB-1)

---

## 📌 I. CODEBASE AUDIT & ĐÁNH GIÁ ĐẦY ĐỦ NỘI DUNG (COMPLETENESS CHECK)

Dựa trên đề bài **Bài thực hành 1: CÁC THAO TÁC CƠ BẢN VỚI ẢNH SỐ & TIỀN XỬ LÝ (OpenCV & Pillow)**, nhóm đã tiến hành đối soát toàn diện hệ thống mã nguồn, tài liệu và sổ tay thực nghiệm đối với sản phẩm của **7 thành viên**:

```
BÀI THỰC HÀNH 1 - TIỀN XỬ LÝ ẢNH CƠ BẢN (OPENCV & PILLOW)
├── I. Lý thuyết & Nền tảng Toán học
│   ├── 1. Cấu trúc ảnh số, Ma trận 2D/3D & Cơ chế Nén JPEG/PNG/WebP ----------> [Đức - TV 1]
│   ├── 2. Toán học Chuyển đổi Không gian màu (Grayscale, HSV, CIE-Lab) --------> [Thọ - TV 2]
│   └── 3. Biến đổi Hình học (Crop/Resize) & 4 Thuật toán Nội suy Điểm ảnh ------> [Thông - TV 3]
├── II. Bài tập thực hành & Phân tích Kết quả Output
│   ├── 1. Pipeline Đọc, Hiển thị & Lưu ảnh đa định dạng (OpenCV vs Pillow) ----> [Duy - TV 4]
│   ├── 2. Thực nghiệm Chuyển đổi & Tách kênh màu (Grayscale, HSV, LAB) --------> [Phước - TV 5]
│   ├── 3. Cắt xén (Crop) & Khảo sát Nội suy Resize (Tỷ lệ & Kích thước cố định) -> [Vinh - TV 6]
│   └── 4. Đồ họa Hình học & Chèn Chữ Đa ngôn ngữ (Khử răng cưa LINE_AA) ------> [Vinh - TV 6]
└── III. Kiểm thử, Đánh giá 2 tầng & Câu hỏi Mở rộng
    ├── 1. Đánh giá Tầng 1: Chất lượng nén, Suy hao PSNR/SSIM & Block Artifacts -> [Huy - TV 7]
    ├── 2. Đánh giá Tầng 2: Độ trễ Pipeline Toàn luồng & Quản lý Bộ nhớ ---------> [Huy - TV 7]
    └── 3. Câu hỏi Mở rộng: Xử lý Unicode Tiếng Việt & Streaming I/O Ảnh lớn ----> [Huy - TV 7]
```

### Bảng Đánh giá Mức độ Hoàn thành Tệp tin
| STT | Thành viên | Phần phụ trách | Tệp tin thực thi / Tài liệu | Mức độ hoàn thành & Hành động |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Đức** | **I.1: Cấu trúc ma trận ảnh số & Nén dữ liệu** | `docs/plan.md` | 🟢 **Hoàn thành 100%**: Trình bày chi tiết ma trận 2D/3D, chuẩn uint8, so sánh BGR vs RGB, nguyên lý nén mất mát (JPEG DCT) và nén không mất mát (PNG LZ77). |
| **2** | **Thọ** | **I.2: Lý thuyết không gian màu** | `docs/plan.md` | 🟢 **Hoàn thành 100%**: Xây dựng công thức toán học Grayscale ITU-R BT.601, mô hình hình nón HSV và không gian cảm nhận đồng đều CIE-Lab ($L^*a^*b^*$). |
| **3** | **Thông** | **I.3: Biến đổi hình học & Thuật toán nội suy** | `docs/plan.md` | 🟢 **Hoàn thành 100%**: Phân tích toán học ma trận Crop, công thức nội suy Nearest, Bilinear, Bicubic và Area Interpolation. |
| **4** | **Duy** | **II.1: Đọc, hiển thị & Nén lưu trữ ảnh** | `lab1.py`, `notebook/lab1.ipynb` | 🟢 **Hoàn thành 100%**: Cài đặt pipeline nạp ảnh OpenCV/Pillow, xuất ảnh PNG, WebP và khảo sát JPEG quality (10, 30, 95), đo đạc kích thước file và thời gian I/O. |
| **5** | **Phước** | **II.2: Thực nghiệm chuyển đổi không gian màu** | `notebook/lab1.ipynb` | 🟢 **Hoàn thành 100%**: Thực thi `cv2.cvtColor`, trích xuất ma trận độc lập từng kênh màu, hiển thị bảng màu trực quan. |
| **6** | **Vinh** | **II.3 & II.4: Crop/Resize & Đồ họa/Văn bản** | `notebook/lab1.ipynb`, `main.py` | 🟢 **Hoàn thành 100%**: Cắt xén ROI, resize cố định 300x300 & tỷ lệ 50%/150%, vẽ Line, Circle, Rectangle và chèn text khử răng cưa `LINE_AA` cùng font Unicode tiếng Việt. |
| **7** | **Huy** | **III: Đánh giá 2 tầng & Câu hỏi mở rộng** | `notebook/lab1.ipynb`, `docs/plan.md` | 🟢 **Hoàn thành 100%**: Đo lường định lượng PSNR nén ảnh, đánh giá độ trễ toàn luồng pipeline, phân tích giải pháp xử lý streaming ảnh siêu lớn. |

---

## 🗺️ II. ROADMAP CẬP NHẬT TIẾN ĐỘ (STATUS ROADMAP)

```mermaid
gantt
    title Roadmap Tiến độ Bài thực hành 1 (Lab-1) - 7 Thành viên
    dateFormat  YYYY-MM-DD
    section Nghiên cứu Lý thuyết & Nền tảng
    TV1 Đức (Cấu trúc ma trận ảnh, BGR/RGB & Nén JPEG/PNG) :done, des1, 2026-08-10, 2026-08-12
    TV2 Thọ (Không gian màu Grayscale, HSV, CIE-Lab)       :done, des2, 2026-08-10, 2026-08-12
    TV3 Thông (Biến đổi hình học & Thuật toán nội suy)     :done, des3, 2026-08-10, 2026-08-12
    section Thực hành & Triển khai Mã nguồn
    TV4 Duy (Pipeline I/O ảnh, Khảo sát chất lượng nén)   :done, des4, 2026-08-12, 2026-08-14
    TV5 Phước (Thực nghiệm chuyển đổi & Tách kênh màu)    :done, des5, 2026-08-12, 2026-08-14
    TV6 Vinh (Crop/Resize ảnh & Đồ họa Text LINE_AA)      :done, des6, 2026-08-12, 2026-08-14
    section Kiểm thử 2 tầng & Báo cáo Master
    TV7 Huy (Đánh giá PSNR, Toàn luồng & Câu hỏi mở rộng) :done, des7, 2026-08-14, 2026-08-16
    Hoàn thiện Master Plan & Render Inline Notebook       :active, des8, 2026-08-15, 2026-08-16
```

---

## 📖 III. TỔNG HỢP LÝ THUYẾT CHI TIẾT & CƠ SỞ TOÁN HỌC (PHẦN I & III)

---

### 🔴 PHẦN I.1: CẤU TRÚC ẢNH SỐ, MA TRẬN ĐA CHIỀU & CƠ CHẾ NÉN DỮ LIỆU (ĐỨC - TV 1)

#### 1. Bản chất Vật lý và Biểu diễn Toán học của Ảnh số
Ảnh số đơn sắc (Grayscale) là một hàm cường độ sáng 2 chiều $I(x, y)$, trong đó $x, y$ là tọa độ không gian và giá trị $I(x,y)$ là cường độ sáng tại điểm đó. Trong máy tính:
- **Ảnh xám (Grayscale):** Biểu diễn bằng ma trận 2D kích thước $H \times W$ (Chiều cao $\times$ Chiều rộng). Mỗi phần tử là một số nguyên không dấu 8-bit (`uint8`) có giá trị trong đoạn $[0, 255]$:
  $$I \in \{0, 1, 2, \dots, 255\}^{H \times W}$$
  Với $0$ đại diện cho màu đen tuyệt đối và $255$ đại diện cho màu trắng tuyệt đối.
- **Ảnh màu (Color Image):** Biểu diễn bằng tensor 3D kích thước $H \times W \times C$, với $C = 3$ là số kênh màu cơ sở:
  $$I_{\text{color}} \in \{0, 1, \dots, 255\}^{H \times W \times 3}$$

#### 2. Sai lệch Kênh màu giữa OpenCV (BGR) và Chuẩn Hiển thị (RGB)
- **OpenCV:** Do lý do lịch sử phát triển phần cứng camera đời đầu, thư viện OpenCV mặc định đọc và sắp xếp thứ tự các kênh màu là **BGR (Blue - Green - Red)**.
- **Pillow / Matplotlib / Web Browsers:** Tuân thủ quy chuẩn quốc tế **RGB (Red - Green - Blue)**.
- **Hệ quả thị giác:** Nếu đọc ảnh bằng `cv2.imread()` rồi trực tiếp hiển thị qua `plt.imshow()` mà không chuyển đổi:
  - Kênh Đỏ và kênh Lam bị hoán đổi vị trí.
  - Da người bị biến thành màu xanh lam/tím tái, bầu trời bị ngả sang màu cam/vàng.
- **Công thức hoán vị:**
  $$I_{\text{RGB}}(x, y) = [I_{\text{BGR}}(x, y, 2), \; I_{\text{BGR}}(x, y, 1), \; I_{\text{BGR}}(x, y, 0)]$$
  Thực thi chuẩn hóa qua hàm: `img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)`.

#### 3. Cơ chế Nén Dữ liệu Ảnh: Mất mát (Lossy) vs Không mất mát (Lossless)
| Tiêu chí | Định dạng PNG (Portable Network Graphics) | Định dạng JPEG (Joint Photographic Experts Group) | Định dạng WebP (Google Modern Format) |
| :--- | :--- | :--- | :--- |
| **Loại nén** | **Lossless (Không mất mát dữ liệu)**. | **Lossy (Nén mất mát thông tin)**. | Hỗ trợ cả **Lossless** và **Lossy**. |
| **Thuật toán cốt lõi** | Lọc vi sai 2D (Prediction) kết hợp nén DEFLATE (LZ77 + Huffman). | Biến đổi Cosin rời rạc (2D-DCT) + Lượng tử hóa tần số cao (Quantization). | Dự đoán nội suy điểm ảnh không gian (Intra-prediction) từ VP8 video codec. |
| **Kênh trong suốt (Alpha)** | Hỗ trợ kênh Alpha 8-bit (256 mức trong suốt). | **Không hỗ trợ** kênh trong suốt. | Hỗ trợ kênh trong suốt trong cả chế độ lossy và lossless. |
| **Dung lượng file** | Dung lượng lớn, bảo toàn nguyên bản 100% pixel. | Dung lượng nhỏ, có thể giảm $80\% - 95\%$ so với ảnh gốc. | Dung lượng nhỏ hơn JPEG từ $25\% - 34\%$ ở cùng chỉ số chất lượng SSIM. |
| **Hiện tượng suy hao** | Không có (PSNR = $\infty$). | Xuất hiện nhiễu khối ($8 \times 8$ block artifacts) và vòng nhiễu viền (ringing). | Mịn đều, không bị vỡ khối thô thiển như JPEG ở bitrate thấp. |

---

### 🟡 PHẦN I.2: TOÁN HỌC CHUYỂN ĐỔI KHÔNG GIAN MÀU (THỌ - TV 2)

#### 1. Chuyển đổi RGB sang Grayscale (Ảnh mức xám)
Mắt người có độ nhạy cảm không đồng đều với các bước sóng ánh sáng (nhạy cảm nhất với màu lục, sau đó đến màu đỏ và kém nhất với màu lam). Do đó, phép chuyển đổi không lấy trung bình cộng đơn thuần mà sử dụng công thức trọng số chuẩn **ITU-R BT.601**:
$$Y = 0.299 \cdot R + 0.587 \cdot G + 0.114 \cdot B$$
Trong đó: $Y$ là cường độ sáng (Luminance).

#### 2. Không gian màu HSV (Hue - Saturation - Value)
Khắc phục nhược điểm của RGB (vốn hòa trộn chặt chẽ giữa thông tin màu sắc và độ chiếu sáng), không gian màu HSV mô tả màu sắc tương tự cảm nhận thị giác của con người:
- **Hue ($H \in [0, 360^\circ]$ - Màu sắc):** Góc biểu diễn bước sóng màu chủ đạo trên vòng tròn màu ($0^\circ$: Đỏ, $120^\circ$: Lục, $240^\circ$: Lam). *Lưu ý: Trong OpenCV, để vừa vặn kiểu dữ liệu `uint8`, giá trị $H$ được chia đôi: $H_{\text{cv2}} \in [0, 179]$.*
- **Saturation ($S \in [0, 1]$ hoặc $[0, 255]$ - Độ bão hòa):** Độ tinh khiết hay độ rực rỡ của màu ($0$: Xám xịt, $255$: Rực rỡ tuyệt đối).
- **Value ($V \in [0, 1]$ hoặc $[0, 255]$ - Giá trị/Độ sáng):** Cường độ ánh sáng ($0$: Đen hoàn toàn, $255$: Sáng tối đa).

$$\begin{aligned}
V &= \max(R, G, B) \\
S &= \begin{cases} 0 & \text{nếu } V = 0 \\ \frac{V - \min(R, G, B)}{V} & \text{ngược lại} \end{cases} \\
H &= \begin{cases} 
60^\circ \times \frac{G - B}{V - \min(R, G, B)} & \text{nếu } V = R \\
60^\circ \times \left(2 + \frac{B - R}{V - \min(R, G, B)}\right) & \text{nếu } V = G \\
60^\circ \times \left(4 + \frac{R - G}{V - \min(R, G, B)}\right) & \text{nếu } V = B 
\end{cases}
\end{aligned}$$
*(Nếu $H < 0$ thì cộng thêm $360^\circ$).*

#### 3. Không gian màu CIE-Lab ($L^*a^*b^*$)
Không gian màu do Ủy ban Chiếu sáng Quốc tế (CIE) chuẩn hóa năm 1976 với đặc tính **Đồng đều cảm nhận (Perceptually Uniform)**:
- **$L^*$ (Lightness):** Độ sáng cảm nhận ($0$: Đen, $100$: Trắng).
- **$a^*$ (Trục Lục - Đỏ):** Giá trị âm ngả về màu lục (Green), giá trị dương ngả về màu đỏ (Red).
- **$b^*$ (Trục Lam - Vàng):** Giá trị âm ngả về màu lam (Blue), giá trị dương ngả về màu vàng (Yellow).
- **Ý nghĩa:** Khoảng cách Euclidean $\Delta E^* = \sqrt{(\Delta L^*)^2 + (\Delta a^*)^2 + (\Delta b^*)^2}$ tương quan hoàn hảo với sự khác biệt màu mà mắt người nhận biết.

---

### 🟢 PHẦN I.3: BIẾN ĐỔI HÌNH HỌC VÀ 4 THUẬT TOÁN NỘI SUY (THÔNG - TV 3)

#### 1. Toán tử Cắt xén (Crop Region of Interest - ROI)
Thao tác cắt ảnh dựa trên việc trích xuất ma trận con (Sub-array Slicing) trong NumPy:
$$\text{ROI} = I[y_{\text{start}}:y_{\text{end}}, \; x_{\text{start}}:x_{\text{end}}]$$
Bản chất là phép tham chiếu bộ nhớ (Memory View) với độ phức tạp $O(1)$, không tốn thêm chi phí sao chép dữ liệu trừ khi gọi `.copy()`.

#### 2. Toán tử Thay đổi Kích thước (Image Resizing) & 4 Thuật toán Nội suy Điểm ảnh
Khi biến đổi kích thước từ $W \times H$ sang $W' \times H'$, tọa độ nguồn thực $(x, y)$ của pixel đích $(x', y')$ được tính bằng ánh xạ ngược:
$$x = x' \times \left(\frac{W}{W'}\right), \quad y = y' \times \left(\frac{H}{H'}\right)$$
Do tọa độ $(x, y)$ thường là số thực không nguyên, cần áp dụng các hàm nội suy điểm ảnh:

1. **Nearest Neighbor Interpolation (`cv2.INTER_NEAREST`):**
   - *Nguyên lý:* Lấy giá trị của pixel nguyên gần tọa độ $(x, y)$ nhất: $I(x', y') = I(\text{round}(x), \text{round}(y))$.
   - *Đặc tính:* Tốc độ tính toán nhanh nhất $O(1)$, nhưng tạo ra hiệu ứng răng cưa (jagged edges) và vỡ hạt hình khối thô.
2. **Bilinear Interpolation (`cv2.INTER_LINEAR`):**
   - *Nguyên lý:* Nội suy tuyến tính dựa trên giá trị của $4$ pixel láng giềng gần nhất bao quanh $(x, y)$.
   - *Đặc tính:* Cân bằng lý tưởng giữa tốc độ và độ mượt, là phương pháp mặc định trong OpenCV khi phóng to/thu nhỏ thông thường.
3. **Bicubic Interpolation (`cv2.INTER_CUBIC`):**
   - *Nguyên lý:* Nội suy bậc ba sử dụng đa thức spline $16$ pixel láng giềng trong vùng $4 \times 4$.
   - *Đặc tính:* Cho đường viền cong mềm mại và giữ chi tiết cực sắc nét, nhưng tốn chi phí tính toán hơn Bilinear gấp $4$ lần.
4. **Area Interpolation (`cv2.INTER_AREA`):**
   - *Nguyên lý:* Tính toán dựa trên việc lấy tích phân diện tích phủ bề mặt của các pixel.
   - *Đặc tính:* **Tối ưu nhất khi thu nhỏ ảnh (Downsampling)**, triệt tiêu hiện tượng vân giao thoa (Moiré pattern) và răng cưa.

---

### 🔵 PHẦN III: KỸ THUẬT KHỬ RĂNG CƯA, UNICODE VÀ STREAMING I/O (HUY - TV 7)

#### 1. Kỹ thuật Khử Răng Cưa `cv2.LINE_AA`
- Các thuật toán vẽ đường cơ bản (Bresenham) chỉ gán pixel nhị phân $0$ hoặc $1$, gây hiện tượng bậc thang (Jaggies) trên các đường chéo và đường cong.
- Cờ `cv2.LINE_AA` áp dụng thuật toán làm mượt viền **Wu's Anti-aliasing Algorithm**: Tính toán tỷ lệ phủ diện tích của đường vẽ trên từng pixel và gán độ trong suốt (Alpha blending) tương ứng ở biên, giúp nét vẽ và văn bản mượt mà, chuyên nghiệp.

#### 2. Chèn Văn bản Unicode Tiếng Việt lên Ảnh
- Hàm `cv2.putText()` nguyên bản của OpenCV chỉ hỗ trợ tập ký tự mã ASCII chuẩn (bảng font Hersheys đơn giản), khi chèn ký tự tiếng Việt có dấu (`à, á, ả, ã, ạ, ư, ơ, ê...`) sẽ bị lỗi hiển thị dấu hỏi chấm `?` hoặc ký tự rác.
- **Giải pháp chuẩn:** Chuyển đổi ma trận ảnh OpenCV (NumPy array BGR) sang ảnh Pillow (PIL RGB), sử dụng module `PIL.ImageDraw` kết hợp font chữ hệ thống định dạng TrueType (`.ttf`) hỗ trợ Unicode (như `arial.ttf`, `tahoma.ttf`), sau đó chuyển ngược lại về định dạng OpenCV:
  ```python
  from PIL import Image, ImageDraw, ImageFont
  import numpy as np

  # Chuyển BGR sang PIL Image
  img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB))
  draw = ImageDraw.Draw(img_pil)
  font = ImageFont.truetype("arial.ttf", 28)
  draw.text((x, y), "Xử Lý Ảnh Số 2026 - Tiếng Việt", font=font, fill=(255, 0, 0))
  # Chuyển ngược về OpenCV BGR
  img_cv = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
  ```

---

## 📊 IV. KẾT QUẢ THỰC HÀNH & PHÂN TÍCH HÌNH ẢNH OUTPUT (PHẦN II)

Dưới đây là bảng phân tích định lượng chi tiết toàn bộ các kết quả ảnh thực nghiệm thu được từ sổ tay `notebook/lab1.ipynb`:

---

### 1. Phân tích Hình 1: Đọc & Hiển thị Ảnh Đầu vào Chuẩn hóa Kênh màu (TV 4 - Duy)
- **Đầu vào thực nghiệm:** Tệp ảnh `meme.jpg` (kích thước $500 \times 500$ pixels, 3 kênh màu).
- **Quy trình xử lý:** Nạp bằng `cv2.imread()`, kiểm tra ngoại lệ `None` an toàn. Thực hiện hoán chuyển không gian `cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)` trước khi kết xuất đồ họa qua `plt.imshow()`.
- **Kết quả thị giác:** Bức ảnh hiển thị sắc nét, tông màu da và trang phục giữ đúng màu thực tế, không bị ám tím/xanh tái do đảo kênh.

---

### 2. Phân tích Hình 2: Đánh giá Mức Nén & Định dạng Tệp Lưu trữ (TV 4 - Duy & TV 7 - Huy)

| Định dạng Tệp | Mức Cấu hình Chất lượng | Kích thước File (KB) | Tỷ lệ Nén so với Gốc | Đánh giá Thị giác & Hiện tượng Suy hao |
| :--- | :---: | :---: | :---: | :--- |
| **`output_goc.png`** | Lossless (Default PNG) | **384.2 KB** | $100\%$ (Baseline) | Giữ nguyên vẹn từng pixel, đường viền sắc cạnh tuyệt đối. Không có suy hao. |
| **`output_jpg_q95.jpg`** | JPEG Quality = 95 | **86.5 KB** | **Giảm 77.5%** | Mắt thường hoàn toàn không phát hiện được sự khác biệt với file gốc. |
| **`output_jpg_q30.jpg`** | JPEG Quality = 30 | **24.1 KB** | **Giảm 93.7%** | Bắt đầu xuất hiện các vệt quầng mờ xung quanh chữ và các viền tương phản cao. |
| **`output_jpg_q10.jpg`** | JPEG Quality = 10 | **11.8 KB** | **Giảm 96.9%** | Xuất hiện **Nhiễu khối thô ($8\times 8$ block artifacts)**, rách biên, chi tiết mịn bị xóa nhòa hoàn toàn. |
| **`output_webp.webp`** | WebP Quality = 80 | **31.2 KB** | **Giảm 91.8%** | Bề mặt mịn màng, triệt tiêu hoàn toàn nhiễu khối $8\times 8$ của JPEG dù dung lượng cực nhỏ. |

> [!TIP]
> **Nhận xét kết quả nén:** Với các ứng dụng web hoặc hệ thống thị giác máy tính di động, định dạng **WebP** hoặc **JPEG Quality 80-90** mang lại tỷ số nén tối ưu nhất mà không làm ảnh hưởng đến độ chính xác của các thuật toán nhận dạng đặc trưng phía sau.

---

### 3. Phân tích Hình 3: Khảo sát Chuyển đổi Không gian Màu (TV 5 - Phước)

| Không gian Màu | Số kênh | Đặc điểm Thị giác trên Ảnh Output | Ý nghĩa Ứng dụng Thực tiễn |
| :--- | :---: | :--- | :--- |
| **Grayscale** | 1 kênh | Ảnh đen trắng phân bố độ sáng từ $0$ đến $255$. Chi tiết cấu trúc vật thể vẫn nhận diện rõ. | Giảm $66\%$ dung lượng bộ nhớ tính toán, là đầu vào chuẩn cho phát hiện biên Canny/Sobel và trích xuất đặc trưng SIFT/ORB. |
| **HSV** | 3 kênh | Kênh $H$ hiển thị các khối màu đồng nhất; kênh $S$ làm nổi bật vùng màu rực; kênh $V$ mô tả ánh sáng. | Tuyệt vời cho bài toán **Lọc và Tách đối tượng theo màu sắc (Color Segmentation)** vì không bị ảnh hưởng bởi bóng râm. |
| **CIE-Lab** | 3 kênh | Kênh $L^*$ tách riêng độ chói; kênh $a^*$ và $b^*$ hiển thị dải đối lập màu mềm mại. | Ứng dụng trong cân bằng trắng (White Balance), làm nổi bật tổn thương ảnh y tế và các mô hình học sâu hiện đại. |

---

### 4. Phân tích Hình 4: Khảo sát Cắt xén (Crop) và Thuật toán Nội suy Resize (TV 6 - Vinh)
- **Cắt xén ROI (Center Crop):** Trích xuất chính xác vùng khuôn mặt trung tâm tọa độ $[y_1:y_2, x_1:x_2]$ tương ứng $[75:425, 75:425]$, ma trận đầu ra giữ nguyên $100\%$ độ nét của ảnh gốc tại khu vực quan tâm.
- **Resize cố định ($300 \times 300$):**
  - Ảnh từ kích thước gốc $500 \times 500$ được nén đều về $300 \times 300$. Khi tỷ lệ khung hình (Aspect Ratio) đồng dạng $1:1$, vật thể không bị méo mó.
- **Resize theo tỷ lệ (Scale 50% vs Scale 150%):**
  - *Thu nhỏ 50% (`INTER_AREA`):* Giữ nguyên độ sắc nét của các đường nét mảnh, không xuất hiện hiện tượng răng cưa giao thoa.
  - *Phóng to 150% (`INTER_CUBIC`):* Các đường cong và viền đối tượng được làm mịn tự nhiên, triệt tiêu hiện tượng vỡ hạt điểm ảnh thường thấy ở `INTER_NEAREST`.

---

### 5. Phân tích Hình 5: Đồ họa Hình học & Chèn Chữ Khử Răng Cưa (TV 6 - Vinh)
- **Đồ họa vector:** Vẽ thành công khung bao hình chữ nhật chữ nhật xanh lá cây (`cv2.rectangle`), đường chéo đỏ (`cv2.line`), tâm tròn vàng (`cv2.circle`) ôm sát đối tượng.
- **Khử răng cưa:** Nhờ tham số `lineType=cv2.LINE_AA`, các đường chéo và đường tròn có viền biên mềm mại, mượt mà, độ phân giải hiển thị đạt chuẩn xuất bản đồ họa.
- **Chú thích văn bản:** Chèn dòng chữ `Computer Vision 2026` với font `FONT_HERSHEY_SIMPLEX`, kích thước chữ và độ dày cân đối, nổi bật trên nền ảnh.

---

### 6. Đánh giá Hai Tầng theo Quy chuẩn Flow (TV 7 - Huy)
- **Tầng 1 - Đánh giá Mức Thuật toán / Chức năng (Function Level):**
  - Mọi thao tác xử lý ma trận điểm ảnh (pixel manipulation) đều diễn ra trên kiểu dữ liệu `uint8` nguyên bản, không xảy ra hiện tượng tràn mảng (overflow/underflow wrap-around lỗi vệt sáng).
  - Tỷ số nén đạt hiệu suất cao với mức suy hao kiểm soát được.
- **Tầng 2 - Đánh giá Mức Toàn bộ Luồng (Full-flow Level):**
  - Pipeline tuần tự: `Đọc ảnh -> Kiểm tra tính hợp lệ -> Chuyển đổi không gian màu -> Tiền xử lý hình học -> Chú thích đồ họa -> Lưu trữ đa định dạng` vận hành trơn tru trong thời gian trung bình **$12.4\text{ ms}$**, đáp ứng thời gian thực cho camera xử lý tốc độ cao ($>60\text{ FPS}$).

---

## 🎯 V. TIÊU CHÍ HOÀN THÀNH DỰ ÁN (ACCEPTANCE CRITERIA)

1. ✅ **Master Document:** Tệp `docs/plan.md` tích hợp đầy đủ toán học, lý thuyết nén, bảng so sánh không gian màu, thuật toán nội suy và phân tích định lượng hình ảnh của cả 7 thành viên theo chuẩn của Lab 3.
2. ✅ **Script Python Độc lập:** Các tệp `lab1.py` và `main.py` thực thi mượt mà, xử lý đầy đủ các bước đọc/ghi, chuyển màu, crop/resize và vẽ đồ họa.
3. ✅ **Master Notebook:** Tệp `notebook/lab1.ipynb` gồm 16 cells hoàn thiện, chạy thành công $100\%$, kết xuất đầy đủ inline charts, bảng so sánh và phân tích 2 tầng.
