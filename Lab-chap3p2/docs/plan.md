# KẾ HOẠCH THỰC HIỆN & PHÂN CÔNG — LAB-CHAP3P2 (WAVELET HASHING)

## 📌 BẢNG PHÂN CÔNG

| STT | Thành viên | Phần phụ trách | Nhiệm vụ chính | Tệp tin |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Thông** | **Phần I + II.1 + II.2** | Mục tiêu bài tập; chuẩn bị dataset 20–30 ảnh (giống/khác); giải thích 2D-DWT (`pywt.wavedec2`), băng tần LL/LH/HL/HH, cách chọn wavelet. | `docs/thong-I-II12.md`, `notebook/prepare_dataset.py`, `notebook/verify_wavelet_hash.py` |
| 2 | _(chờ bổ sung)_ | Phần II.3 + II.4 | Tạo hash wavelet, so sánh Hamming, đánh giá. | `notebook/` |
| 3 | _(chờ bổ sung)_ | Phần nâng cao III.1 + III.2 | Khảo sát các phương pháp wHash; ứng dụng tìm kiếm ảnh. | `notebook/` |

## 🚀 TIẾN ĐỘ

| Giai đoạn | Nội dung | Trạng thái |
|---|---|---|
| 1. Lý thuyết | Mục tiêu, khái niệm wavelet, 2D-DWT, băng tần | ✅ Đã xong (Thông) |
| 2. Dữ liệu | Sinh dataset 22 ảnh (similar/different) | ✅ Đã xong (Thông) |
| 3. Trích xuất wavelet | Kiểm chứng haar/db4/sym2 trên cặp ảnh | ✅ Đã xong (Thông) |
| 4. Hashing & so sánh | Tạo hash, Hamming, đánh giá | ⏳ Chờ |
| 5. Nâng cao | Khảo sát phương pháp, tìm kiếm ảnh | ⏳ Chờ |
