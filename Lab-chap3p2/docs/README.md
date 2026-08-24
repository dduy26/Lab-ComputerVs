# Xây dựng ứng dụng tìm kiếm hình ảnh dựa trên hàm băm wavelet (Phần III. 2)

## Yêu cầu
- Python 3.8+
- Cài thư viện: `pip install opencv-python numpy matplotlib pillow PyWavelets`

## Cách chạy
1. Di chuyển vào thư mục `notebook/`.
2. (Tuỳ chọn) Tạo dữ liệu mẫu: `python prepare_dataset.py`.
3. Xây dựng database: `python search_app.py build --image-dir ../data/input --db ../wavelet_db.json`.
4. Tìm kiếm: `python search_app.py search --query ../data/input/meme.jpg --db ../wavelet_db.json --top-k 5`.

## Đánh giá
- Xây dựng database: ~0.08 giây cho 22 ảnh.
- Tìm kiếm: ~99 ms cho 22 ảnh.
- Độ chính xác cao với Hamming ≤ 1 cho ảnh giống, >10 cho ảnh khác.