BÁO CÁO BÀI 4: KẾT HỢP CANNY VỚI CÁC KỸ THUẬT KHÁC
1. Phân tích yêu cầu bài toán
Đề bài yêu cầu sử dụng thuật toán Canny để trích xuất cạnh từ ảnh đầu vào.
Từ ảnh cạnh Canny thu được, thực hiện kết hợp với 2 kỹ thuật:
Phân đoạn vùng: Tìm đường bao (contours) và vẽ hộp bao (bounding box) cho các đối tượng.
Nhận dạng hình dạng: Sử dụng Biến đổi Hough để phát hiện đường thẳng và đường tròn.
2. Tìm hiểu dữ liệu
Ảnh dùng để chạy thử là ảnh định dạng .jpg / .png.
Đã chuyển ảnh về dạng ảnh xám (Grayscale) để tính toán ma trận điểm ảnh dễ dàng hơn.
Ảnh có thể có nhiễu sáng hoặc chi tiết thừa, cần dùng bộ lọc làm mịn trước khi bắt cạnh.
3. Các tính năng cần có trong code
Read & Preprocess: Đọc ảnh, chuyển ảnh xám và dùng Gaussian Blur $5 \times 5$ lọc nhiễu.
Canny Detection: Tìm biên cạnh với 2 ngưỡng $T_{low} = 50, T_{high} = 150$.
Contour & Bounding Box: Tìm viền quanh đối tượng và vẽ khung hình chữ nhật bao lại.
Hough Transform: Tìm các nét thẳng và đường tròn có trong ảnh.
Plot Result: Dùng Matplotlib hiển thị 4 ảnh kết quả lên cùng một màn hình để so sánh.
4. Giải pháp kỹ thuật
Xử lý luồng (Logic): Sử dụng các hàm xử lý ảnh cơ bản của thư viện OpenCV (cv2.imread, cv2.cvtColor, cv2.GaussianBlur, cv2.rectangle, cv2.circle).
Thuật toán thị giác máy tính:
cv2.Canny()
cv2.findContours() & cv2.boundingRect()
cv2.HoughLinesP() & cv2.HoughCircles()
5. Hiện thực hóa
import cv2
import numpy as np
import matplotlib.pyplot as plt
# 1. Đọc ảnh và tiền xử lý
img = cv2.imread('input.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)
# 2. Phát hiện cạnh bằng Canny
canny_edges = cv2.Canny(blurred, 50, 150)
# 3. Phân đoạn vùng (Contours & Bounding Box)
contours, _ = cv2.findContours(canny_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
img_segmentation = img.copy()
for cnt in contours:
    if cv2.contourArea(cnt) > 50:  # Lọc bỏ nhiễu nhỏ
        cv2.drawContours(img_segmentation, [cnt], -1, (0, 255, 0), 2)
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img_segmentation, (x, y), (x + w, y + h), (0, 0, 255), 2)
# 4. Nhận dạng hình dạng (Hough Transform)
img_hough = img.copy()
# Tìm đường thẳng
lines = cv2.HoughLinesP(canny_edges, 1, np.pi/180, threshold=50, minLineLength=40, maxLineGap=10)
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line.squeeze()
        cv2.line(img_hough, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)
# Tìm đường tròn
circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=150, param2=30, minRadius=20, maxRadius=100)
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        cv2.circle(img_hough, (i[0], i[1]), i[2], (0, 0, 255), 2)
# 5. Hiển thị kết quả ra màn hình
plt.figure(figsize=(10, 7))
plt.subplot(2, 2, 1)
plt.title("1. Anh goc")
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
plt.subplot(2, 2, 2)
plt.title("2. Canh Canny")
plt.imshow(canny_edges, cmap='gray')
plt.subplot(2, 2, 3)
plt.title("3. Phan doan vùng")
plt.imshow(cv2.cvtColor(img_segmentation, cv2.COLOR_BGR2RGB))
plt.subplot(2, 2, 4)
plt.title("4. Nhan dang Hough")
plt.imshow(cv2.cvtColor(img_hough, cv2.COLOR_BGR2RGB))
plt.tight_layout()
plt.show()
6. Kiểm thử và đánh giáĐánh giá mức thuật toán:
Canny lọc nhiễu tốt, đường biên thu được mảnh (1 pixel) và nét. Vì vậy, bước tìm Contour bắt đúng hình dạng đối tượng mà không bị vỡ nét.
Đánh giá toàn luồng: Chương trình chạy ổn định, không bị văng lỗi. Nếu chỉnh tham số $T_{low}, T_{high}$ quá cao thì ảnh Canny bị đứt nét, dẫn đến thuật toán Hough tìm thiếu đường thẳng.
7. Kết luận
Canny đóng vai trò là bước tiền xử lý quan trọng. Việc tách biên trước giúp giảm dung lượng dữ liệu cần tính toán, làm cho các thuật toán phân đoạn và nhận dạng hình dạng hoạt động chính xác và nhanh hơn nhiều so with việc xử lý trực tiếp trên ảnh gốc.
