# QUY TRÌNH THỰC HIỆN DỰ ÁN XỬ LÝ ẢNH (7-STEP WORKFLOW)

---

### 🔹 Bước 1 - Phân tích yêu cầu (Refine Requirement)
Cần phải hiểu rõ và xác định chính xác các yêu cầu của bài toán trước khi bắt đầu. Xác định mục tiêu đầu vào, đầu ra, các ràng buộc kỹ thuật và phạm vi thực hiện của bài toán.

---

### 🔹 Bước 2 - Hiểu về dữ liệu (Data Understanding)
Sau khi nắm rõ yêu cầu, bắt buộc phải tìm hiểu và hiểu rõ tập dữ liệu mình đang có là gì. Phân tích cấu trúc ma trận ảnh, kiểu dữ liệu, các kênh màu, độ phân giải, dải giá trị pixel và các đặc trưng quang học/thị giác của tập ảnh thực nghiệm.

---

### 🔹 Bước 3 - Xác định Tính năng (Feature)
Từ các yêu cầu thực tế của bài toán (business/problem domain), trích xuất và định nghĩa rõ ràng danh sách các tính năng (features/functions) mà sản phẩm/pipeline xử lý ảnh cần phải có.

---

### 🔹 Bước 4 - Giải pháp Kỹ thuật (Technical Solution)
Xây dựng giải pháp toàn diện để đáp ứng các tính năng trên. Giải pháp này được chia làm hai phần:
- **Phần Logic:** Đảm nhiệm các thuật toán logic thông thường, luồng ứng dụng, quản lý I/O, tiền xử lý và cấu trúc luồng backend.
- **Phần AI / Image Processing:** Đảm nhiệm việc ứng dụng các toán tử toán học, bộ lọc xử lý ảnh số hoặc các mô hình học máy/thị giác máy tính vào bài toán.

---

### 🔹 Bước 5 - Hiện thực hóa (Implementation)
Chỉ sau khi hoàn thiện các bước thiết kế và phân tích ở trên mới tiến hành viết code và triển khai hệ thống. Xây dựng mã nguồn sạch, module hóa, dễ bảo trì và có khả năng tái sử dụng cao.

---

### 🔹 Bước 6 - Kiểm thử và Đánh giá (Testing & Evaluation)
Thực hiện các bước kiểm thử chức năng (như unit test, edge case testing). Đặc biệt, đối với các giải pháp liên quan đến AI và dữ liệu hình ảnh, hệ thống phải được đánh giá nghiêm ngặt ở hai tầng:
- **Tầng 1 (Model/Function Level):** Đánh giá ở mức mô hình hoặc từng thuật toán/toán tử đơn lẻ (đo lường độ chính xác, chất lượng lọc, bảo toàn biên, chỉ số PSNR, SSIM, sai số định lượng).
- **Tầng 2 (Full-flow Level):** Đánh giá ở mức toàn bộ luồng xử lý (tính ổn định từ khâu nạp dữ liệu đến khi xuất kết quả, thời gian đáp ứng latency, mức sử dụng tài nguyên bộ nhớ).

---

### 🔹 Bước 7 - Kết luận (Conclusion)
Phân tích toàn diện các kết quả thu được sau khi kiểm thử và đánh giá, rút ra ưu/nhược điểm của phương pháp và đưa ra kết luận, định hướng cải tiến cuối cùng.