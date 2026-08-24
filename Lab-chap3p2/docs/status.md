# TIẾN ĐỘ THỰC HIỆN & STATUS DỰ ÁN - LAB-CHAP3P2

Theo dõi tiến độ hoàn thành và cập nhật trạng thái chi tiết cho dự án **Lab-chap3p2: So sánh sự tương đồng của các hình ảnh sử dụng Wavelet Hash (wHash)**.

---

## 📌 ROADMAP TIẾN ĐỘ VÀ CÁC FILE ĐÃ TẠO

### 📖 Phần IV: Băm Hình Ảnh Wavelet (Wavelet Hash)

- [DONE] **Mã nguồn thực thi Python (`code.py`)**:
  - Đã cài đặt hoàn chỉnh tệp mã nguồn [`notebook/code.py`](file:///d:/X%E1%BB%AD%20l%C3%AD%20%E1%BA%A3nh/FileGit/Lab-ComputerVs/Lab-chap3p2/notebook/code.py).
  - Đọc ảnh bằng cả OpenCV (`cv2.imread` / `cv2.imdecode` hỗ trợ tiếng Việt Unicode) và PIL (`Image.open`).
  - Chuyển màu mức xám (Grayscale) và Resize chuẩn hóa kích thước cố định ($256 \times 256$).
  - Khử nhiễu & Phân tách tần số Wavelet 2D (`pywt.wavedec2`), lượng tử hóa theo giá trị Trung vị (`np.median`), tạo mã băm nhị phân 64-bit và mã Hex.
  - So sánh độ tương đồng bằng Khoảng cách Hamming (`np.count_nonzero(b1 != b2)`).
  - Trực quan hóa 6 bước bằng Matplotlib và lưu kết quả tự động tại `data/output/wavelet_hash_visualization_cv2.png`.

- [DONE] **Báo cáo Lý thuyết (`docs/lythuyet.md`)**:
  - Đã soạn thảo đầy đủ tệp lý thuyết [`docs/lythuyet.md`](file:///d:/X%E1%BB%AD%20l%C3%AD%20%E1%BA%A3nh/FileGit/Lab-ComputerVs/Lab-chap3p2/docs/lythuyet.md).
  - Giải thích toán học và nguyên lý chi tiết 3 bước của Wavelet Hash (Phân tách Wavelet 2D $\rightarrow$ Lượng tử hóa Median $\rightarrow$ Tạo mã băm nhị phân & Khoảng cách Hamming).
  - Bảng mô tả chi tiết tác dụng của từng hàm trong `code.py`.

- [DONE] **Kế hoạch Thực hiện & Áp dụng Hàm (`docs/plan.md`)**:
  - Đã soạn thảo tệp kế hoạch [`docs/plan.md`](file:///d:/X%E1%BB%AD%20l%C3%AD%20%E1%BA%A3nh/FileGit/Lab-ComputerVs/Lab-chap3p2/docs/plan.md).
  - Mô tả rõ cho từng bước: mục tiêu kỹ thuật, lý do áp dụng và **tên hàm cụ thể được dùng kèm ví dụ code minh họa** (ví dụ: Cần khử nhiễu & phân tách tần số thì dùng Wavelet `pywt.wavedec2()`, cần đọc ảnh an toàn tiếng Việt thì dùng `np.fromfile()` + `cv2.imdecode()`, cần lượng tử hóa dùng `np.median()`, v.v.).

---

## 📊 TỔNG KẾT TRẠNG THÁI (STATUS)

| Hạng mục | Tệp tương ứng | Trạng thái | Đánh giá |
| :--- | :--- | :---: | :--- |
| **Mã nguồn thực thi** | [`notebook/code.py`](file:///d:/X%E1%BB%AD%20l%C3%AD%20%E1%BA%A3nh/FileGit/Lab-ComputerVs/Lab-chap3p2/notebook/code.py) | **[DONE]** | Chạy thành công 100%, không lỗi path/encoding |
| **Báo cáo Lý thuyết** | [`docs/lythuyet.md`](file:///d:/X%E1%BB%AD%20l%C3%AD%20%E1%BA%A3nh/FileGit/Lab-ComputerVs/Lab-chap3p2/docs/lythuyet.md) | **[DONE]** | Giải thích đầy đủ 3 bước toán học |
| **Kế hoạch & Hàm áp dụng** | [`docs/plan.md`](file:///d:/X%E1%BB%AD%20l%C3%AD%20%E1%BA%A3nh/FileGit/Lab-ComputerVs/Lab-chap3p2/docs/plan.md) | **[DONE]** | Chi tiết từng bước + ví dụ hàm cụ thể |
| **Tiến độ dự án** | [`docs/status.md`](file:///d:/X%E1%BB%AD%20l%C3%AD%20%E1%BA%A3nh/FileGit/Lab-ComputerVs/Lab-chap3p2/docs/status.md) | **[DONE]** | Hoàn thành toàn bộ các yêu cầu |

---

## 📌 ROADMAP TIẾN ĐỘ – PHẦN III. 2. Xây dựng ứng dụng tìm kiếm hình ảnh dựa trên hàm băm wavelet.

- [DONE] **Phân tích yêu cầu** – Đọc flow.md, xác định chức năng cần xây dựng.
- [DONE] **Hiểu dữ liệu** – Xác định thư mục ảnh và định dạng.
- [DONE] **Xác định tính năng** – Liệt kê các chức năng build‑db, search, evaluate.
- [DONE] **Giải pháp kỹ thuật** – Chọn CLI, sử dụng JSON, tận dụng các hàm có sẵn.
- [DONE] **Hiện thực hóa** – Tạo file `notebook/search_app.py` hoàn chỉnh.
- [DONE] **Kiểm thử & Đánh giá** – Chạy thử nghiệm, đo thời gian, kiểm tra top K.
- [DONE] **Kết luận** – Ghi nhận kết quả trong báo cáo.

**Trạng thái tổng thể:** ✅ Hoàn thành.


---
## ROADMAP TIẾN ĐỘ – PHẦN II. Bài toán cụ thể: 3 & 4. Tạo mã băm Wavelet và So sánh hàm băm

- [DONE] **Giải thích quá trình lượng tử hóa** – Trình bày bản chất lượng tử hóa hệ số Wavelet, phân tích phương pháp dùng thư viện `pywt.quantize` và phương pháp lượng tử hóa nhị phân tự viết.
- [DONE] **Xác định ngưỡng lượng tử & Độ dài mã băm** – Phân tích các chiến lược chọn ngưỡng (Median, Mean, Fixed Threshold) và làm rõ mối quan hệ giữa kích thước ma trận $LL$ với độ dài chuỗi băm (64-bit).
- [DONE] **Chuyển hệ số thành mã nhị phân** – Xây dựng quy trình ánh xạ ma trận hệ số sau lượng tử hóa thành vector nhị phân (bit 0/1) và gom nhóm thành chuỗi Hexadecimal.
- [DONE] **Giải thích khoảng cách Hamming** – Trình bày bản chất phép đo khoảng cách Hamming và hiện thực hóa công thức tính toán `sum(bit1 != bit2)`.
- [DONE] **Xác lập ngưỡng quyết định tương đồng** – Thiết lập tiêu chuẩn đánh giá độ tương đồng dựa trên tỉ lệ lỗi bit (ngưỡng $\le 10\%$ độ dài hash để xác định hai ảnh tương đồng).
- [DONE] **Thực nghiệm minh họa trên các cặp ảnh** – Chạy thực nghiệm, thu thập mã băm và đo khoảng cách Hamming trên 3 cặp ảnh mẫu (Ảnh gốc vs Biến thể chỉnh sửa, vs Biến thể nhiễu/làm mờ, vs Ảnh khác loại).
- [DONE] **Tổng hợp báo cáo & Biện luận** – Lập bảng tổng hợp số liệu thực nghiệm và giải thích chi tiết kết quả vào tài liệu báo cáo `lythuyet.md`.

**Trạng thái tổng thể:** ✅ Hoàn thành.

---

## 📌 ROADMAP TIẾN ĐỘ – PHẦN II.5: Đánh giá hiệu suất & Vẽ biểu đồ ROC
> **Phụ trách:** Thành viên 3: Duy (random)

- [DONE] **Xây dựng Kế hoạch hàm áp dụng (`docs/plan.md`)**:
  - Xác định các bước và hàm sử dụng (`sklearn.metrics.confusion_matrix`, `roc_curve`, `auc`, `matplotlib.pyplot`).
  - Viết ví dụ mô tả logic áp dụng hàm cho từng bước đánh giá chỉ số và vẽ biểu đồ.

- [DONE] **Tính toán các chỉ số đánh giá cơ bản (`notebook/code.py`)**:
  - Lập Ma trận Nhầm lẫn (Confusion Matrix): $TP, TN, FP, FN$.
  - Tính Độ chính xác (Accuracy): $\text{Accuracy} = \frac{TP + TN}{TP + TN + FP + FN}$.
  - Tính Độ nhạy (Sensitivity / Recall): $\text{Sensitivity} = \frac{TP}{TP + FN}$.
  - Tính Độ đặc hiệu (Specificity): $\text{Specificity} = \frac{TN}{TN + FP}$.

- [DONE] **Vẽ đường cong ROC và tính diện tích AUC (`notebook/code.py`)**:
  - Trích xuất `fpr`, `tpr`, `thresholds` bằng `sklearn.metrics.roc_curve()`.
  - Tính diện tích $AUC$ bằng `sklearn.metrics.auc()`.
  - Trực quan hóa và xuất biểu đồ ROC chất lượng cao bằng `matplotlib.pyplot` tại `data/output/roc_curve_evaluation.png`.

- [DONE] **Soạn thảo báo cáo Lý thuyết & Đánh giá (`docs/lythuyet.md`)**:
  - Định nghĩa toán học chi tiết cho Confusion Matrix, Accuracy, Sensitivity, Specificity.
  - Giải thích bản chất đường cong ROC và ý nghĩa của chỉ số diện tích AUC.
  - Hướng dẫn từng bước cách vẽ ROC bằng `sklearn.metrics` và `matplotlib`.
  - Biện luận đánh giá hiệu suất của thuật toán Wavelet Hash dựa trên các chỉ số thực nghiệm.

**Trạng thái tổng thể:** ✅ Hoàn thành 100%.

