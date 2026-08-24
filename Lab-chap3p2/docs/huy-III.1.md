1. Khái niệm Biến đổi Wavelet (Discrete Wavelet Transform - DWT)
Nguyên lý: Phân rã ảnh thành 4 băng tần tần số ở cấp độ 1:
LL (Low-Low): Băng tần xấp xỉ tần số thấp, chứa hầu hết năng lượng và khung bố cục chính của ảnh.
LH (Low-High): Bắt các chi tiết đường biên ngang.
HL (High-Low): Bắt các chi tiết đường biên dọc.
HH (High-High): Bắt các chi tiết đường chéo và nhiễu.
2. Khái niệm Mã băm ảnh (Perceptual Image Hashing)
Khác với mã băm mật mã (như MD5, SHA-256 - chỉ cần đổi 1 bit là mã thay đổi hoàn toàn), Perceptual Hash tạo ra chuỗi bit đại diện cho "cảm nhận trực quan" của ảnh. Hai ảnh có nội dung tương tự nhau sẽ cho hai chuỗi mã băm gần giống nhau (khoảng cách Hamming nhỏ).
3. Nguyên lý 3 phương pháp khảo sát
Phương pháp 1 (LL Hash): Rút gọn băng tần $LL$ về kích thước cố định (ví dụ $8 \times 8$). So sánh giá trị từng phần tử với giá trị trung vị (median) để tạo chuỗi bit 0/1.
Phương pháp 2 (Detail Energy Hash): Chia các băng tần $LH, HL, HH$ thành các ô nhỏ (blocks), tính tổng năng lượng $E = \sum I_{ij}^2$ trên từng ô để đại diện cho mật độ kết cấu, sau đó nhị phân hóa chuỗi năng lượng này.
Phương pháp 3 (Combined Hash): Ghép nối chuỗi bit từ $LL$ (giữ cấu trúc tổng thể) và chuỗi bit từ $Energy$ (giữ độ sắc nét/chi tiết bề mặt) theo tỷ lệ trọng số nhất định (ví dụ 70% - 30%).
4. Các chỉ số đánh giá hiệu suất (Performance Metrics)
Khoảng cách Hamming: Số lượng bit khác nhau giữa 2 chuỗi mã băm.
Độ chính xác (Accuracy): Tỷ lệ dự đoán đúng cặp ảnh "Tương tự" hay "Khác nhau".
Khả năng phân biệt (Discrimination): Khoảng cách Hamming chuẩn hóa giữa 2 ảnh hoàn toàn khác nhau (giá trị lý tưởng tiến sát $0.5$).
