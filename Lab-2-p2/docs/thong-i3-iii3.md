# Thành viên 3 — Thông

## Phạm vi phụ trách

- **Phần I.3:** Ưu điểm, nhược điểm và ứng dụng thực tế của Canny Edge Detector.
    - **I.3.a:** So sánh Canny với Sobel và Laplacian theo độ chính xác, tốc độ và khả năng xử lý nhiễu.
    - **I.3.b:** Những lĩnh vực sử dụng Canny phổ biến.
    - **I.3.c:** Các ví dụ ứng dụng cụ thể.
- **Phần III.3:** Canny có thể phát hiện cạnh trong ảnh màu không? Nếu có thì thực hiện như thế nào?

---

# 1. Phân tích yêu cầu (Refine Requirement)

## 1.1. Mục tiêu

Nội dung cần giúp người đọc trả lời được bốn câu hỏi:

1. Canny có ưu điểm và nhược điểm gì?
2. Khi so với Sobel và Laplacian, Canny chính xác hơn hay nhanh hơn, và chịu nhiễu tốt hơn ở điểm nào?
3. Canny được dùng trong lĩnh vực nào và dùng để làm gì?
4. Canny xử lý ảnh màu bằng cách nào, vì `cv2.Canny` thường nhận ảnh một kênh?

## 1.2. Đầu ra cần nộp

- Một mục báo cáo Markdown có đủ **I.3.a + I.3.b + I.3.c + III.3**.
- Một bảng so sánh **Canny — Sobel — Laplacian**.
- Ít nhất 4–6 ví dụ ứng dụng cụ thể.
- Một sơ đồ hoặc đoạn giải thích quy trình xử lý ảnh màu.
- Tài liệu tham khảo được ghi trong `docs/reference.md`.

## 1.3. Tiêu chí hoàn thành

- Không chỉ nói “Canny tốt hơn”; phải giải thích **vì sao**: Gaussian giảm nhiễu, non-maximum suppression làm mảnh cạnh, ngưỡng kép và hysteresis giữ cạnh liên tục.[1][2][3]
- Không khẳng định tuyệt đối “Canny luôn chính xác nhất”; kết quả phụ thuộc ảnh, nhiễu, độ tương phản và tham số ngưỡng.
- Phân biệt rõ:
    - **Sobel/Laplacian:** chủ yếu tạo đáp ứng gradient/đạo hàm.
    - **Canny:** là một quy trình phát hiện cạnh nhiều bước và cho ảnh cạnh nhị phân cuối cùng.[1][2]
- Phần ảnh màu phải nêu ít nhất hai cách xử lý và trade-off của mỗi cách.

---

# 2. Hiểu dữ liệu (Data Understanding)

Phần của Thông không cần một dataset huấn luyện. Dữ liệu được xét là **ảnh số** dùng để phát hiện cạnh.

## 2.1. Các kiểu ảnh cần hiểu

| Kiểu dữ liệu | Đặc điểm | Ảnh hưởng đến Canny |
|---|---|---|
| Ảnh xám | Một kênh cường độ | Có thể đưa trực tiếp vào Canny |
| Ảnh màu BGR/RGB | Ba kênh màu | Thường phải chuyển sang ảnh xám hoặc xử lý từng kênh |
| Ảnh nhiễu | Có biến đổi cường độ ngẫu nhiên | Có thể sinh nhiều cạnh giả |
| Ảnh tương phản thấp | Chênh lệch sáng tối nhỏ | Cạnh yếu dễ bị loại bởi ngưỡng cao |
| Ảnh nhiều chi tiết | Nhiều thay đổi cường độ nhỏ | Có thể tạo bản đồ cạnh dày và rối |

## 2.2. Điểm kỹ thuật quan trọng

- OpenCV đọc ảnh màu theo thứ tự **BGR**, không phải RGB.
- `cv2.Canny` thường được áp dụng lên ảnh 8-bit một kênh; tài liệu scikit-image cũng mô tả đầu vào Canny chuẩn là ảnh grayscale.[1][2]
- Chuyển ảnh màu sang grayscale làm giảm dữ liệu từ ba kênh xuống một kênh; cách này nhanh nhưng có thể bỏ sót biên chỉ khác nhau về màu mà có độ sáng gần giống nhau.

---

# 3. Xác định tính năng/nội dung (Feature)

Với phần lý thuyết, “feature” được hiểu là các khối nội dung báo cáo phải có:

1. **Khối ưu điểm của Canny.**
2. **Khối nhược điểm của Canny.**
3. **Bảng so sánh Canny, Sobel và Laplacian.**
4. **Danh sách lĩnh vực sử dụng phổ biến.**
5. **Các tình huống ứng dụng cụ thể.**
6. **Giải thích Canny trên ảnh màu.**
7. **Kết luận lựa chọn thuật toán theo nhu cầu.**

Không cần tạo UI, backend, API hoặc mô hình học sâu cho phần này.

---

# 4. Giải pháp kỹ thuật (Technical Solution)

## 4.1. Phần logic

Luồng trình bày nên đi theo thứ tự:

```text
Bản chất Canny
    → Ưu điểm / nhược điểm
    → So sánh với Sobel và Laplacian
    → Lĩnh vực sử dụng
    → Ví dụ ứng dụng
    → Canny trên ảnh màu
    → Kết luận
```

## 4.2. Phần AI

- **Không có mô hình AI cần huấn luyện.**
- Canny là thuật toán xử lý ảnh cổ điển, dựa trên Gaussian, gradient, non-maximum suppression, ngưỡng kép và hysteresis.
- Nếu Canny nằm trong một hệ thống AI, nó thường đóng vai trò **tiền xử lý hoặc trích xuất đặc trưng**, không phải mô hình dự đoán cuối cùng.

---

# 5. Nội dung cần trình bày

## 5.1. Ưu điểm của Canny

- **Khả năng định vị cạnh tốt:** Cạnh phát hiện được thường nằm gần vị trí biên thật của đối tượng.
- **Cạnh mảnh:** Non-maximum suppression loại các đáp ứng không cực đại, giúp đường cạnh thường chỉ dày khoảng một pixel.
- **Giảm cạnh giả do nhiễu tốt hơn các toán tử đạo hàm đơn giản:** Canny có bước làm mịn Gaussian trước khi tính gradient.
- **Giữ cạnh liên tục tốt:** Ngưỡng kép phân loại cạnh mạnh/cạnh yếu; hysteresis giữ cạnh yếu nếu chúng liên kết với cạnh mạnh.
- **Đầu ra dễ dùng cho bước sau:** Ảnh cạnh nhị phân phù hợp với tìm contour, Hough Transform, phân đoạn và nhận dạng hình dạng.

## 5.2. Nhược điểm của Canny

- **Chậm hơn Sobel và Laplacian:** Canny phải thực hiện nhiều bước thay vì chỉ tính đạo hàm/tích chập.
- **Nhạy với tham số:** Sigma, ngưỡng thấp và ngưỡng cao không phù hợp có thể làm mất cạnh thật hoặc giữ quá nhiều cạnh giả.
- **Không có một bộ tham số tối ưu cho mọi ảnh:** Ảnh tối, ảnh nhiễu và ảnh nhiều chi tiết cần cách chỉnh khác nhau.
- **Có thể mất chi tiết nhỏ:** Gaussian blur mạnh hoặc ngưỡng cao sẽ loại cả cạnh yếu có ý nghĩa.
- **Canny chuẩn chủ yếu dựa trên cường độ sáng:** Nếu chuyển ảnh màu sang grayscale, các biên màu có độ sáng gần nhau có thể biến mất.
- **Không hiểu ngữ nghĩa:** Thuật toán chỉ biết nơi cường độ thay đổi mạnh, không biết cạnh nào thuộc vật thể quan trọng.

## 5.3. So sánh Canny với Sobel và Laplacian

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

## 5.4. Lĩnh vực Canny được sử dụng phổ biến

Canny phổ biến nhất trong **thị giác máy tính và xử lý ảnh**, đặc biệt ở các bài toán cần lấy đường biên hình học trước khi phân tích vật thể.

Các lĩnh vực thường gặp:

1. **Giao thông thông minh và xe tự hành.**
2. **Kiểm tra chất lượng trong công nghiệp.**
3. **Xử lý ảnh y tế.**
4. **Robot và định vị.**
5. **Xử lý tài liệu và OCR.**
6. **Giám sát, an ninh và phân tích video.**
7. **Viễn thám và ảnh vệ tinh.**

> Không nên khẳng định một lĩnh vực duy nhất là “phổ biến nhất” nếu không có số liệu thống kê. Cách viết an toàn: Canny được dùng rộng rãi nhất như một bước tiền xử lý trong thị giác máy tính; các ví dụ điển hình gồm giao thông, công nghiệp, y tế và tài liệu.

## 5.5. Ví dụ ứng dụng cụ thể

- **Phát hiện làn đường:** Canny lấy các vạch biên trên mặt đường; Hough Transform tìm các đoạn thẳng biểu diễn làn xe.
- **Nhận dạng biển báo hoặc biển số:** Canny hỗ trợ tìm contour, hình chữ nhật hoặc vùng ký tự trước bước OCR.
- **Kiểm tra linh kiện:** Phát hiện đường viền, vết nứt, cạnh thiếu hoặc sai hình dạng của sản phẩm trên dây chuyền.
- **Đo kích thước vật thể:** Tách đường biên rồi tính chiều dài, diện tích, chu vi hoặc đường kính.
- **Ảnh y tế:** Hỗ trợ làm nổi ranh giới mô, xương hoặc tổn thương; kết quả vẫn cần chuyên gia hay phương pháp phân đoạn khác xác nhận.
- **Quét tài liệu:** Tìm bốn cạnh của tờ giấy, sau đó hiệu chỉnh phối cảnh để tạo ảnh scan thẳng.
- **Robot:** Trích xuất biên của chướng ngại vật hoặc đặc trưng hình học để hỗ trợ điều hướng.
- **Phân tích ảnh vệ tinh:** Tìm ranh giới đường, công trình, sông hoặc khu vực sử dụng đất khi tương phản phù hợp.

## 5.6. Canny trên ảnh màu

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

# 6. Kiểm thử và đánh giá (Testing & Evaluation)

Phần của Thông là lý thuyết nên không cần unit test cho mô hình. Nếu có chạy code minh họa, đánh giá ở hai tầng như sau.

## 6.1. Tầng 1 — Mức thuật toán

Kiểm tra Canny trên cùng một ảnh và so sánh với Sobel/Laplacian:

- Cạnh có mảnh không?
- Cạnh thật có liên tục không?
- Có nhiều điểm nhiễu/cạnh giả không?
- Có bỏ mất cạnh yếu không?
- Thời gian xử lý tương đối giữa ba thuật toán như thế nào?

Không cần dựng benchmark phức tạp nếu đề chỉ yêu cầu lý thuyết; bảng so sánh và một ảnh minh họa là đủ.

## 6.2. Tầng 2 — Toàn bộ luồng

Nếu dùng Canny làm tiền xử lý cho một ứng dụng, cần kiểm tra đầu ra cuối:

- Tìm làn đường: có xác định đúng hai biên làn không?
- Quét tài liệu: có tìm đúng bốn góc tờ giấy không?
- Tìm contour: có bao đúng đối tượng không?
- Nhận dạng hình dạng: Hough/contour có nhận đúng hình sau Canny không?

Canny đẹp về mặt thị giác chưa chắc làm hệ thống cuối tốt hơn; kết luận phải dựa trên mục tiêu cuối của luồng.

---

# 7. Kết luận

Canny thường cho cạnh mảnh, liên tục và chống nhiễu tốt hơn Sobel hoặc Laplacian nhờ quy trình nhiều bước. Đổi lại, nó chậm hơn và phụ thuộc nhiều vào sigma cùng hai ngưỡng. Trong thực tế, Canny phù hợp làm bước tiền xử lý cho tìm contour, Hough Transform, phân đoạn và nhận dạng hình dạng. Với ảnh màu, cách đơn giản nhất là chuyển sang grayscale; khi biên màu quan trọng, có thể xử lý từng kênh hoặc sử dụng HSV/Lab rồi hợp nhất kết quả.

---

# Workflow làm và trình bày trên Git

## Cấu trúc giữ nguyên

```text
Lab-2-p2/
├── data/input/                    # Ảnh dùng chung của nhóm
├── docs/
│   ├── thong-i3-iii3.md           # File này: phần của Thông
│   ├── reference.md               # Nguồn tham khảo chung
│   ├── require.md                 # Yêu cầu tổng của nhóm
│   ├── flow.md                    # Workflow tổng
│   ├── plan.md                    # Phân công
│   └── status.md                  # Tiến độ
└── notebook/                      # Code thực hành của thành viên khác
```

## Luồng Git đề xuất

```bash
cd E:/ThiGiacMayTinh/Lab-ComputerVs
git switch -c feature/thong-canny-i3-iii3
git add
  Lab-2-p2/docs/thong-i3-iii3.md
  Lab-2-p2/docs/reference.md
  Lab-2-p2/docs/status.md
git commit -m "docs: add Thong Canny theory and color edge analysis"
git push -u origin feature/thong-canny-i3-iii3
```

Sau đó tạo Pull Request vào `main` với nội dung:

```markdown
## Phạm vi
- Hoàn thành I.3.a: so sánh Canny, Sobel và Laplacian.
- Hoàn thành I.3.b: lĩnh vực sử dụng Canny.
- Hoàn thành I.3.c: ví dụ ứng dụng.
- Hoàn thành III.3: Canny trên ảnh màu.

## Kiểm tra
- [x] Đúng phạm vi Thành viên 3 — Thông.
- [x] Có bảng so sánh theo độ chính xác, tốc độ, xử lý nhiễu.
- [x] Có ưu điểm và nhược điểm.
- [x] Có ví dụ ứng dụng cụ thể.
- [x] Có giải thích và code minh họa ảnh màu.
- [ ] Đã được một thành viên khác review.
```

## Quy tắc trình bày trên GitHub

- Mỗi thành viên làm trên một branch; không commit trực tiếp vào `main`.
- Một commit chỉ chứa đúng một phần việc để dễ review.
- Tên file không dùng khoảng trắng hoặc dấu tiếng Việt.
- Markdown dùng heading rõ ràng, bảng cho nội dung so sánh, code block có ngôn ngữ `python`.
- Ảnh kết quả nếu có đặt trong `data/output/thong/`, không nhét ảnh trực tiếp vào `docs/`.
- Sau khi merge, cập nhật `docs/status.md` từ `[TESTING]` sang `[DONE]`.

## Checklist trước khi nộp

- Đọc lại đúng I.3(a+b+c) và III.3 trong slide.
- Không lấn sang phần 5 bước Canny hoặc phân tích tham số của thành viên khác.
- Không gọi Canny là mô hình AI.
- Không nói Canny luôn tốt nhất trong mọi trường hợp.
- Kiểm tra code dùng đúng BGR → Gray của OpenCV.
- Thêm nguồn vào `reference.md`.
- Mở file trên GitHub và kiểm tra bảng/code render đúng.
- Có Pull Request và ít nhất một người review trước khi merge.