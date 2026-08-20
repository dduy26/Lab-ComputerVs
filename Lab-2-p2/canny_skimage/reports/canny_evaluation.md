# Canny Edge Detection – Scikit‑image

## Mục tiêu
Đánh giá ảnh hưởng của các tham số sigma, low_threshold, high_threshold lên chất lượng phát hiện cạnh.

## Dữ liệu
Hai ảnh: meme.jpg, memetest.jpg (chuyển grayscale).

## Phương pháp
Sử dụng `skimage.feature.canny`. Chạy với 4 bộ tham số (mặc định + 3 bộ tùy chỉnh). Lưu ảnh kết quả và bảng so sánh.

## Kết quả nhận xét
- **Default (sigma=1, auto threshold)**: kết quả cân bằng, phù hợp ảnh ít nhiễu.
- **Tăng sigma (2)**: làm mờ nhiều, giảm cạnh giả, ít nhiễu hơn.
- **Giảm low_threshold (10)**: xuất hiện nhiều cạnh yếu, tăng độ nhạy.
- **Tăng high_threshold (150)**: chỉ giữ cạnh mạnh, bỏ qua cạnh yếu.

## So sánh với mặc định
Mặc định là lựa chọn tốt cho ảnh tổng quát, nhưng với ảnh nhiễu (memetest) nên tăng sigma và điều chỉnh ngưỡng.

## Kết luận
Không có tham số cố định cho mọi ảnh; cần thử nghiệm để chọn bộ phù hợp.