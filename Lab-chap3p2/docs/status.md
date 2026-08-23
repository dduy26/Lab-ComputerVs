# TIẾN ĐỘ THỰC HIỆN & STATUS PROJECT - LAB-CHAP3P2

Theo dõi tiến độ hoàn thành các hạng mục công việc trong dự án **Lab-chap3p2: So sánh sự tương đồng của các hình ảnh sử dụng Wavelet**.

---

## 📌 DANH SÁCH TIẾN ĐỘ CÁC HẠNG MỤC

### 📖 Phần IV: Tham khảo Wavelet Hash & Code Thực hành
- [DONE] **Giải thích chi tiết 3 bước Wavelet Hash**:
  - *Bước 1:* Biến đổi Wavelet 2D (phân tích tần số & không gian, trích xuất băng tần LL).
  - *Bước 2:* Lượng tử hóa hệ số (giảm độ chính xác bằng giá trị Trung vị - Median).
  - *Bước 3:* Tạo mã băm nhị phân & Hex, so sánh khoảng cách Hamming.
  - *Tệp tài liệu:* [`docs/IV_Wavelet_Hash.md`](file:///d:/X%E1%BB%AD%20l%C3%AD%20%E1%BA%A3nh/FileGit/Lab-ComputerVs/Lab-chap3p2/docs/IV_Wavelet_Hash.md)

- [DONE] **Viết code hoàn chỉnh xử lý ảnh đầu vào**:
  - Đọc ảnh bằng cả OpenCV (`cv2.imread`) và PIL (`Image.open`).
  - Chuyển sang ảnh mức xám (Grayscale).
  - Resize ảnh về kích thước chuẩn hóa ($256 \times 256$).
  - Tính mã băm Wavelet 64-bit, tính khoảng cách Hamming và tỷ lệ tương đồng.
  - Trực quan hóa 6 bước bằng Matplotlib và lưu kết quả vào `data/output/`.
  - *Tệp thực thi:* [`notebook/wavelet_hash.py`](file:///d:/X%E1%BB%AD%20l%C3%AD%20%E1%BA%A3nh/FileGit/Lab-ComputerVs/Lab-chap3p2/notebook/wavelet_hash.py)

---

## 📊 TRẠNG THÁI CÁC NHÓM TRẠNG THÁI

- **[DONE]**: Đã hoàn thành phần IV (Lý thuyết 3 bước & Code hoàn chỉnh Python OpenCV/PIL).