# YÊU CẦU DỰ ÁN (REQUIREMENTS) - BÀI TẬP CUỐI KỲ (LAB-END)

## 1. Tổng Quan Dự Án
- **Tên bài lab**: Nhận diện khuôn mặt thời gian thực với FaceNet & MTCNN (Real-time Face Recognition).
- **Mục tiêu**: Xây dựng ứng dụng nhận diện khuôn mặt trực tiếp từ Webcam/Video/Hình ảnh bằng cách kết hợp thuật toán phát hiện khuôn mặt **MTCNN** (Multi-task Cascaded Convolutional Networks) và thuật toán trích xuất đặc trưng **FaceNet** (InceptionResnetV1).
- **Môi trường hoạt động**: Python 3.x, PyTorch, OpenCV, `facenet-pytorch`, NumPy, Matplotlib, PIL.

---

## 2. Yêu Cầu Chức Năng (Functional Requirements)

### 2.1. Quản Lý & Thu Thập Luồng Dữ Liệu (Data Stream & Webcam Integration)
- Khởi tạo và đọc luồng video từ Webcam thiết bị bằng OpenCV (`cv2.VideoCapture`).
- Hỗ trợ xử lý ảnh tĩnh (`.jpg`, `.png`) từ thư mục `data/input/` để phục vụ thử nghiệm và kiểm thử offline.
- Cấu hình kích thước khung hình chuẩn và quản lý vòng lặp xử lý từng frame theo thời gian thực.

### 2.2. Phát Hiện & Cắt Khuôn Mặt (Face Detection with MTCNN)
- Sử dụng mô hình **MTCNN** để phát hiện vị trí các khuôn mặt xuất hiện trong khung hình.
- Trả về tọa độ Bounding Box `(x1, y1, x2, y2)`, điểm tin cậy (Confidence Score) và các vị trí đặc trưng Landmarks (mắt trái, mắt phải, mũi, khóe miệng trái, khóe miệng phải).
- Tự động cắt (crop) và chuẩn hóa kích thước khuôn mặt về dạng tensor `(3, 160, 160)` phù hợp làm đầu vào cho mô hình FaceNet.

### 2.3. Trích Xuất Vector Đặc Trưng (Feature Extraction with FaceNet)
- Sử dụng mô hình **FaceNet** (chế độ Pre-trained trên dataset `vggface2` hoặc `casia-webface`).
- Chuyển đổi mỗi khuôn mặt đã cắt thành một Vector Embedding 512 chiều trong không gian vector (Vector Space).
- Chuẩn hóa L2 vector đặc trưng để đảm bảo tính nhất quán khi tính khoảng cách và độ tương đồng.

### 2.4. So Sánh & Phân Loại Khuôn Mặt (Face Matching & Thresholding)
- Kho cơ sở dữ liệu khuôn mặt tham chiếu (Reference Face Database): Đăng ký và lưu giữ embeddings khuôn mặt chuẩn (ví dụ: ảnh mẫu `meme.jpg` hoặc ảnh chụp từ webcam).
- Tính độ tương đồng **Cosine Similarity** giữa vector thu được từ khung hình hiện tại và vector mẫu trong CSDL.
  $$\text{Similarity}(A, B) = \frac{A \cdot B}{\|A\|_2 \|B\|_2}$$
- **Quy tắc phân loại & Ngưỡng quyết định (Decision Thresholding)**:
  - Nếu $\text{Similarity} > 0.7$: Xác định là khuôn mặt khớp, hiển thị nhãn **"Matched"** (hoặc Tên nhân vật tương ứng) cùng thông số similarity.
  - Nếu $\text{Similarity} \le 0.7$: Xác định là khuôn mặt lạ, hiển thị nhãn **"Unknown"**.

### 2.5. Trực Quan Hóa & Giao Diện (Visual Interface)
- Vẽ Bounding Box xung quanh khuôn mặt trên khung hình:
  - Khung màu xanh lá (Green): Trường hợp **Matched** ($\text{Similarity} > 0.7$).
  - Khung màu đỏ (Red): Trường hợp **Unknown** ($\text{Similarity} \le 0.7$).
- Hiển thị nhãn text thông tin (`Matched - Score: 0.85` / `Unknown - Score: 0.42`) rõ ràng phía trên Bounding Box.
- Phím tắt tương tác: Nhấn phím `'q'` để thoát ứng dụng webcam, phím `'s'` để lưu ảnh chụp màn hình nhận diện.

### 2.6. Xuất Kết Quả & Lưu Trữ (Output Generation)
- Lưu ảnh kết quả nhận diện đã vẽ Bounding Box và label vào thư mục `data/output/` để phục vụ báo cáo.

---

## 3. Yêu Cầu Phi Chức Năng (Non-functional Requirements)
- **Hiệu năng & Tốc độ (Performance)**: Tốc độ nhận diện thời gian thực (FPS $\ge 15$-20 FPS khi chạy với Webcam trên GPU/CPU).
- **Độ chính xác (Accuracy)**: Hoạt động ổn định ngay cả khi khuôn mặt nghiêng nhẹ, có sự thay đổi ánh sáng hoặc biểu cảm.
- **Tính Mô-đun (Modularity)**: Đóng gói mã nguồn theo hướng đối tượng (OOP) trong file `notebook/labend.py` giúp dễ dàng tái sử dụng và mở rộng.
- **Tính Trực quan (Visualization)**: Notebook `notebook/lab-end.ipynb` trình bày từng bước rõ ràng kèm giải thích lý thuyết và hiển thị kết quả kiểm thử.