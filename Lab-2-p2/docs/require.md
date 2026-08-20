# YÊU CẦU BÀI TẬP & CÂU HỎI - PHẦN II.1 & II.2 (OPENCV CANNY)
**Thành viên:** Duy (Thành viên 4)  
**Thư viện sử dụng:** OpenCV (`cv2`), Matplotlib  
**File code duy nhất:** `notebook/4.py`  

---

## II.1. Thực hiện thuật toán Canny bằng thư viện OpenCV

### 1. Nội dung cần làm
- Giới thiệu hàm `cv2.Canny()` của thư viện OpenCV:
  ```python
  cv2.Canny(image, threshold1, threshold2)
  ```
  - `image`: Ảnh đầu vào (ảnh xám).
  - `threshold1`: Ngưỡng thấp (Low threshold).
  - `threshold2`: Ngưỡng cao (High threshold).

### 2. Ví dụ chương trình (`notebook/4.py`)
```python
import cv2
import matplotlib.pyplot as plt

img = cv2.imread("image.jpg", 0)
edges = cv2.Canny(img, 100, 200)

plt.imshow(edges, cmap='gray')
plt.show()
```

### 3. Kết quả yêu cầu
- **Hình 1**: Ảnh gốc
- **Hình 2**: Kết quả phát hiện cạnh bằng Canny (Ngưỡng mặc định 100, 200)

---

## II.2. Thay đổi các tham số và quan sát kết quả

### 1. Thay đổi ngưỡng thấp và ngưỡng cao
- **Trường hợp 1 (`50, 150`)**: Phát hiện được nhiều cạnh hơn, có thể xuất hiện cạnh nhiễu.
- **Trường hợp 2 (`100, 200`)**: Kết quả cân bằng, loại bỏ được phần lớn nhiễu (Mặc định).
- **Trường hợp 3 (`200, 300`)**: Chỉ giữ lại các cạnh mạnh, một số chi tiết nhỏ bị mất.

### 2. Thay đổi Sigma (Gaussian Blur tiền xử lý)
> OpenCV không truyền trực tiếp tham số Sigma vào `cv2.Canny()`, cần làm mờ bằng `cv2.GaussianBlur()` trước khi gọi Canny.

- **Sigma nhỏ (`sigma = 1`)**:
  ```python
  blur = cv2.GaussianBlur(img, (5, 5), 1)
  edges = cv2.Canny(blur, 100, 200)
  ```
  *Nhận xét:* Giữ được nhiều chi tiết, còn một ít nhiễu.
- **Sigma trung bình (`sigma = 2`)**:
  ```python
  blur = cv2.GaussianBlur(img, (5, 5), 2)
  edges = cv2.Canny(blur, 100, 200)
  ```
  *Nhận xét:* Giảm nhiễu tốt, cạnh rõ ràng.
- **Sigma lớn (`sigma = 5`)**:
  ```python
  blur = cv2.GaussianBlur(img, (5, 5), 5)
  edges = cv2.Canny(blur, 100, 200)
  ```
  *Nhận xét:* Nhiễu giảm mạnh, một số cạnh mảnh bị mất.

### 3. Bảng so sánh với giá trị mặc định

| Trường hợp | Threshold Low | Threshold High | Kết quả nhận xét |
| :--- | :---: | :---: | :--- |
| **Mặc định** | 100 | 200 | Cân bằng giữa nhiễu và chi tiết |
| **Thấp** | 50 | 150 | Nhiều cạnh, nhiều nhiễu |
| **Cao** | 200 | 300 | Ít nhiễu nhưng mất chi tiết |