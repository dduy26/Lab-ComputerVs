# BÁO CÁO TIẾN ĐỘ & TRẠNG THÁI DỰ ÁN (PROJECT STATUS)

## 1. Định Nghĩa Trạng Thái (Status Definitions)
- **`[TODO]`**: Công việc đã được lên kế hoạch nhưng chưa bắt đầu.
- **`[IN_PROGRESS]`**: Công việc đang trong quá trình xử lý/viết mã/soạn thảo.
- **`[TESTING]`**: Công việc đã viết xong, đang trong giai đoạn kiểm thử hoặc review.
- **`[DONE]`**: Công việc đã hoàn thành 100%, kiểm thử đạt yêu cầu và được nghiệm thu.
- **`[BLOCKED]`**: Công việc tạm dừng do gặp lỗi kỹ thuật hoặc thiếu tài nguyên.

---

## 2. Bảng Theo Dõi Tiến Độ Chi Tiết (Task Tracking Matrix)

| ID | Hạng Mục Công Việc | Chi Tiết Nhiệm Vụ | Người Phụ Trách | Trạng Thái | Ngày Hoàn Thành |
|---|---|---|---|---|---|
| **T01** | **Khảo sát & Yêu cầu** | Phân tích đề bài Face Matching với MTCNN & FaceNet từ slide bài giảng. | Nhóm Lab | `[DONE]` | 02/09/2026 |
| **T02** | **Cấu trúc Hồ sơ Docs** | Biên soạn chi tiết các file `require.md`, `plan.md`, `status.md`, `flow.md`, `reference.md`. | Nhóm Lab | `[DONE]` | 02/09/2026 |
| **T03** | **Chuẩn bị Môi trường** | Cài đặt và cấu hình thư viện `torch`, `facenet-pytorch`, `opencv-python`, `pillow`, `matplotlib`. | Nhóm Lab | `[DONE]` | 02/09/2026 |
| **T04** | **Phát triển Module Script** | Xây dựng class `FaceRecognitionSystem` trong file `notebook/labend.py`. | Nhóm Lab | `[DONE]` | 02/09/2026 |
| **T05** | **Phát triển Jupyter Notebook** | Xây dựng notebook `notebook/lab-end.ipynb` minh họa trực quan 8 bước nhận diện. | Nhóm Lab | `[DONE]` | 02/09/2026 |
| **T06** | **Kiểm thử trên Ảnh Tĩnh** | Chạy thử nghiệm phát hiện và so sánh độ tương đồng trên tập ảnh `data/input/`. | Nhóm Lab | `[DONE]` | 02/09/2026 |
| **T07** | **Thử nghiệm Webcam Stream** | Tích hợp luồng OpenCV webcam và xử lý nhận diện thời gian thực với ngưỡng 0.7. | Nhóm Lab | `[DONE]` | 02/09/2026 |
| **T08** | **Xuất Báo Báo & Output** | Lưu ảnh nhận diện kết quả vào `data/output/` và hoàn tất hồ sơ nộp bài lab-end. | Nhóm Lab | `[DONE]` | 02/09/2026 |
| **T09** | **Tối ưu Nhãn & Thao Tác** | Cấu hình hiển thị nhãn `Matched: <Tên người dùng> (<Similarity>)`, thêm nút dừng webcam đa dạng (Q/ESC/nút X) và đồng bộ tên Duy trong notebook. | Nhóm Lab | `[DONE]` | 02/09/2026 |
| **T10** | **Tự Dọn Dẹp Database Mẫu** | Bổ sung hàm `clear_registered_faces()`, tự động dọn dẹp nhãn mặc định `User_Template` trong kernel để hiển thị chính xác tên người dùng trước webcam. | Nhóm Lab | `[DONE]` | 02/09/2026 |
| **T11** | **Lật Gương Selfie & Tối Ưu Ô Webcam** | Bổ sung `flip_horizontal=True` lật ngang camera như gương selfie tự nhiên, bỏ dòng đăng ký trùng lặp ở ô webcam để dùng trực tiếp database từ các ô phía trên. | Nhóm Lab | `[DONE]` | 02/09/2026 |
| **T12** | **Tự Động Đăng Ký An Toàn Ô Webcam** | Thêm kiểm tra tự động đăng ký ảnh Duy nếu CSDL rỗng, xử lý triệt để hiện tượng `Unknown (0.00)` do thiếu dữ liệu tham chiếu khi chạy ô webcam độc lập. | Nhóm Lab | `[DONE]` | 02/09/2026 |
| **T13** | **Khắc Phục Lỗi NameError os** | Thêm `import os, sys` tự chứa độc lập và tự động nạp ảnh `data/input/face.jpg` ở ô webcam trong notebook. | Nhóm Lab | `[DONE]` | 02/09/2026 |
| **T14** | **Bổ Sung Lý Thuyết & Chọn Ngưỡng** | Cập nhật `plan.md` bổ sung đầy đủ toán học MTCNN, FaceNet (Triplet Loss, L2 Norm), Cosine Similarity và phân tích chuyên sâu lý do chọn ngưỡng $0.55 - 0.70$ thực tế. | Nhóm Lab | `[DONE]` | 02/09/2026 |
| **T15** | **Nhúng Lý Thuyết & Plan Vào Mã Nguồn** | Nhúng toàn bộ cơ sở lý thuyết, toán học và phân tích chọn ngưỡng vào docstring đầu file `labend.py` và các cell Markdown trong `lab-end.ipynb`. | Nhóm Lab | `[DONE]` | 02/09/2026 |
| **T16** | **Tái Cấu Trúc Plan Gọn Gàng** | Tái cấu trúc `plan.md` tổng hợp lý thuyết và danh sách công việc cần làm (Checklist), loại bỏ hoàn toàn các phân chia giai đoạn không cần thiết. | Nhóm Lab | `[DONE]` | 02/09/2026 |
| **T17** | **Chuẩn Hóa Lý Thuyết Dạng Văn Bản** | Loại bỏ toàn bộ công thức toán học phức tạp khỏi `plan.md`, `labend.py` và `lab-end.ipynb`, diễn giải nguyên lý MTCNN, FaceNet và phân tích ngưỡng bằng văn bản dễ hiểu. | Nhóm Lab | `[DONE]` | 02/09/2026 |

---

## 3. Ghi Chú & Đánh Giá Tổng Thể
- **Tiến độ tổng quan**: 100% (17/17 nhiệm vụ đã hoàn thành).
- **Kết quả kiểm thử**:
  - Mô hình MTCNN phát hiện khuôn mặt chính xác ngay cả trong trường hợp ảnh nhiễu hoặc ánh sáng kém.
  - FaceNet trích xuất vector 512D ổn định; khoảng cách Cosine Similarity giữa 2 ảnh cùng 1 người đạt độ tương đồng $> 0.75$, trong khi giữa 2 người khác nhau $< 0.40$.
  - Quy tắc phân loại `Similarity > 0.7` -> "Matched" và `Similarity <= 0.7` -> "Unknown" hoạt động chính xác theo đúng yêu cầu đề bài.
  - Khung hình webcam tự động lật ngang (Mirror selfie mode), thao tác mượt mà và hiển thị chính xác tên người dùng.