# Thành viên 3 — Thông (I.3 a+b+c + III.3)

**Phạm vi phụ trách:** I.3 — Ưu/nhược điểm và ứng dụng thực tế của Canny Edge Detector; III.3 — Canny cho ảnh màu.

---

## 1. Ưu điểm của Canny Edge Detector

- **Khả năng định vị cạnh tốt:** Cạnh phát hiện được thường nằm gần vị trí biên thật của đối tượng.
- **Cạnh mảnh:** Non-maximum suppression loại các đáp ứng không cực đại, giúp đường cạnh thường chỉ dày khoảng một pixel.
- **Giảm cạnh giả do nhiễu tốt hơn các toán tử đạo hàm đơn giản:** Canny có bước làm mịn Gaussian trước khi tính gradient.
- **Giữ cạnh liên tục tốt:** Ngưỡng kép phân loại cạnh mạnh/cạnh yếu; hysteresis giữ cạnh yếu nếu chúng liên kết với cạnh mạnh.
- **Đầu ra dễ dùng cho bước sau:** Ảnh cạnh nhị phân phù hợp với tìm contour, Hough Transform, phân đoạn và nhận dạng hình dạng.

## 2. Nhược điểm của Canny Edge Detector

- **Chậm hơn Sobel và Laplacian:** Canny phải thực hiện nhiều bước thay vì chỉ tính đạo hàm/tích chập.
- **Nhạy với tham số:** Sigma, ngưỡng thấp và ngưỡng cao không phù hợp có thể làm mất cạnh thật hoặc giữ quá nhiều cạnh giả.
- **Không có một bộ tham số tối ưu cho mọi ảnh:** Ảnh tối, ảnh nhiễu và ảnh nhiều chi tiết cần cách chỉnh khác nhau.
- **Có thể mất chi tiết nhỏ:** Gaussian blur mạnh hoặc ngưỡng cao sẽ loại cả cạnh yếu có ý nghĩa.
- **Canny chuẩn chủ yếu dựa trên cường độ sáng:** Nếu chuyển ảnh màu sang grayscale, các biên màu có độ sáng gần nhau có thể biến mất.
- **Không hiểu ngữ nghĩa:** Thuật toán chỉ biết nơi cường độ thay đổi mạnh, không biết cạnh nào thuộc vật thể quan trọng.

---

## 3. I.3.a — So sánh Canny với Sobel và Laplacian

| Tiêu chí | Sobel | Laplacian | Canny |
|---|---|---|---|
| Nguyên lý | Đạo hàm bậc nhất theo X và Y | Đạo hàm bậc hai | Quy trình nhiều bước dựa trên gradient |
| Độ chính xác định vị | Khá, nhưng biên thường dày | Nhạy với thay đổi nhanh, có thể tạo biên kép | Tốt, cạnh mảnh và gần biên thật |
| Độ liên tục của cạnh | Không tự nối cạnh | Không tự nối cạnh | Tốt hơn nhờ ngưỡng kép và hysteresis |
| Khả năng chống nhiễu | Trung bình; Sobel có hiệu ứng làm mịn nhẹ | Kém nhất vì đạo hàm bậc hai khuếch đại nhiễu | Tốt hơn nhờ Gaussian, nhưng vẫn phụ thuộc sigma và ngưỡng |
| Tốc độ | Nhanh | Nhanh và đơn giản | Chậm hơn vì có nhiều giai đoạn |
| Đầu ra | Ảnh độ lớn/hướng gradient | Đáp ứng đạo hàm bậc hai | Bản đồ cạnh nhị phân hoàn chỉnh |
| Điều chỉnh tham số | Ít | Ít | Nhiều hơn, khó chọn hơn |
| Khi nên dùng | Cần gradient, hướng cạnh hoặc xử lý nhanh | Cần phát hiện biến đổi cường độ nhanh, ảnh ít nhiễu | Cần bản đồ cạnh sạch để contour/Hough/phân đoạn |

### Kết luận so sánh

- Chọn **Sobel** khi ưu tiên tốc độ, cần gradient theo phương X/Y hoặc hướng cạnh.
- Chọn **Laplacian** khi cần toán tử đơn giản, phát hiện thay đổi theo mọi hướng và dữ liệu đã được khử nhiễu tốt.
- Chọn **Canny** khi cần cạnh mảnh, liên tục và ít nhiễu hơn để đưa vào các bước xử lý hình học tiếp theo.

---

## 4. I.3.b — Lĩnh vực Canny được sử dụng phổ biến

Canny phổ biến nhất trong **thị giác máy tính và xử lý ảnh**, đặc biệt ở các bài toán cần lấy đường biên hình học trước khi phân tích vật thể. Các lĩnh vực thường gặp:

1. **Giao thông thông minh và xe tự hành.**
2. **Kiểm tra chất lượng trong công nghiệp.**
3. **Xử lý ảnh y tế.**
4. **Robot và định vị.**
5. **Xử lý tài liệu và OCR.**
6. **Giám sát, an ninh và phân tích video.**
7. **Viễn thám và ảnh vệ tinh.**

> Không nên khẳng định một lĩnh vực duy nhất là “phổ biến nhất” nếu không có số liệu thống kê. Cách viết an toàn: Canny được dùng rộng rãi nhất như một bước tiền xử lý trong thị giác máy tính; các ví dụ điển hình gồm giao thông, công nghiệp, y tế và tài liệu.

---

## 5. I.3.c — Ví dụ ứng dụng cụ thể

- **Phát hiện làn đường:** Canny lấy các vạch biên trên mặt đường; Hough Transform tìm các đoạn thẳng biểu diễn làn xe.
- **Nhận dạng biển báo hoặc biển số:** Canny hỗ trợ tìm contour, hình chữ nhật hoặc vùng ký tự trước bước OCR.
- **Kiểm tra linh kiện:** Phát hiện đường viền, vết nứt, cạnh thiếu hoặc sai hình dạng của sản phẩm trên dây chuyền.
- **Đo kích thước vật thể:** Tách đường biên rồi tính chiều dài, diện tích, chu vi hoặc đường kính.
- **Ảnh y tế:** Hỗ trợ làm nổi ranh giới mô, xương hoặc tổn thương; kết quả vẫn cần chuyên gia hay phương pháp phân đoạn khác xác nhận.
- **Quét tài liệu:** Tìm bốn cạnh của tờ giấy, sau đó hiệu chỉnh phối cảnh để tạo ảnh scan thẳng.
- **Robot:** Trích xuất biên của chướng ngại vật hoặc đặc trưng hình học để hỗ trợ điều hướng.
- **Phân tích ảnh vệ tinh:** Tìm ranh giới đường, công trình, sông hoặc khu vực sử dụng đất khi tương phản phù hợp.

---

## 6. III.3 — Canny trên ảnh màu

### Trả lời ngắn

**Có.** Tuy nhiên, Canny cổ điển thường hoạt động trên một ảnh cường độ/grayscale. Vì vậy phải biến đổi ảnh màu thành dữ liệu phù hợp trước khi phát hiện cạnh.[2][3]

### Cách 1 — Chuyển ảnh màu sang grayscale

```python
image = cv2.imread("data/input/meme.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 1.0)
edges = cv2.Canny(blurred, 50, 150)
```

**Ưu điểm:** đơn giản, nhanh, dễ chọn ngưỡng và là cách được sử dụng phổ biến nhất.

**Nhược điểm:** có thể mất biên giữa hai vùng khác màu nhưng có mức sáng gần nhau.

### Cách 2 — Phát hiện cạnh trên từng kênh màu rồi hợp nhất

```python
image = cv2.imread("data/input/meme.jpg")
channels = cv2.split(image)
edges = [cv2.Canny(cv2.GaussianBlur(c, (5, 5), 1.0), 50, 150)
         for c in channels]
color_edges = cv2.bitwise_or(edges[0], cv2.bitwise_or(edges[1], edges[2]))
```

**Ưu điểm:** giữ được các cạnh chỉ nổi bật ở một kênh màu.

**Nhược điểm:** dễ thu thêm cạnh nhiễu, tốn tính toán hơn và vẫn xử lý các kênh độc lập nên chưa mô tả đầy đủ quan hệ màu.

### Cách 3 — Đổi không gian màu rồi chọn kênh phù hợp

- Chuyển BGR sang **HSV** hoặc **Lab**.
- Chạy Canny trên kênh độ sáng (`V` hoặc `L`) nếu muốn giảm ảnh hưởng màu.
- Chạy thêm trên các kênh màu nếu bài toán cần phát hiện ranh giới do sắc độ tạo ra.

### Kết luận cho ảnh màu

- Dùng **grayscale** cho cách triển khai cơ bản và nhanh.
- Dùng **từng kênh hoặc Lab/HSV** khi biên màu quan trọng và grayscale làm mất cạnh.
- Luôn kiểm tra kết quả trực quan vì ngưỡng phù hợp với kênh sáng chưa chắc phù hợp với từng kênh màu.

---

## 7. Kết luận

Canny thường cho cạnh mảnh, liên tục và chống nhiễu tốt hơn Sobel hoặc Laplacian nhờ quy trình nhiều bước. Đổi lại, nó chậm hơn và phụ thuộc nhiều vào sigma cùng hai ngưỡng. Trong thực tế, Canny phù hợp làm bước tiền xử lý cho tìm contour, Hough Transform, phân đoạn và nhận dạng hình dạng. Với ảnh màu, cách đơn giản nhất là chuyển sang grayscale; khi biên màu quan trọng, có thể xử lý từng kênh hoặc sử dụng HSV/Lab rồi hợp nhất kết quả.

---

## Sources

[1] OpenCV, **Canny Edge Detection — Python Tutorials**: https://github.com/opencv/opencv/blob/4.x/doc/py_tutorials/py_imgproc/py_canny/py_canny.markdown

[2] scikit-image, **skimage.feature.canny API**: https://scikit-image.org/docs/stable/api/skimage.feature.html

[3] John Canny, **A Computational Approach to Edge Detection**, IEEE Transactions on Pattern Analysis and Machine Intelligence, 1986. DOI: https://doi.org/10.1109/TPAMI.1986.4767851

[4] Slide môn học, **Chapter 2: Image Processing Methods — Part 2**, mục “Bài thực hành chương 2 (phần 2)”.
