import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

def add_gaussian_noise(image, mean=0, std=60):
    """Thêm nhiễu Gaussian vào ảnh."""
    noise = np.random.normal(mean, std, image.shape).astype(np.float32)
    noisy_img = cv2.add(image.astype(np.float32), noise)
    return np.clip(noisy_img, 0, 255).astype(np.uint8)

def reduce_contrast(image, factor=0.2):
    """Giảm độ tương phản của ảnh."""
    return np.clip((image.astype(np.float32) - 128) * factor + 128, 0, 255).astype(np.uint8)

def main():
    # 1. Đọc ảnh gốc (thử nhiều đường dẫn để đảm bảo chạy được mọi nơi)
    img_paths = ["anh1.jpg", "data/input/meme.jpg", "../data/input/meme.jpg", "Lab-2-p2/data/input/meme.jpg"]
    img = None
    for p in img_paths:
        if os.path.exists(p):
            img = cv2.imread(p, cv2.IMREAD_GRAYSCALE)
            if img is not None:
                break
    
    if img is None:
        print("Khong tim thay anh, dung anh tao ngau nhien.")
        img = np.tile(np.linspace(0, 255, 300, dtype=np.uint8), (300, 1))

    # Resize để quan sát rõ hơn
    img = cv2.resize(img, (400, 400))

    # ==========================================
    # PHẦN II.3: CÁC LOẠI ẢNH KHÁC NHAU (VINH)
    # ==========================================

    # a) Ảnh có nhiều nhiễu
    img_noisy = add_gaussian_noise(img, std=60)
    
    # b) Ảnh có độ tương phản thấp
    img_low_contrast = reduce_contrast(img, factor=0.2)
    
    # c) Ảnh có nhiều chi tiết (dùng bộ lọc làm sắc nét để tăng chi tiết)
    kernel_sharpening = np.array([[-1,-1,-1], 
                                  [-1, 9,-1],
                                  [-1,-1,-1]])
    img_detailed = cv2.filter2D(img, -1, kernel_sharpening)

    # 2. Áp dụng Canny Edge Detector cho từng loại
    
    # -> Canny cho ảnh nhiễu: 
    # Bắt buộc phải làm mờ mạnh hơn để giảm nhiễu (dùng kernel 7x7 và sigma lớn), nếu không sẽ ra vô số cạnh giả
    blur_noisy = cv2.GaussianBlur(img_noisy, (7, 7), 2.5)
    edges_noisy = cv2.Canny(blur_noisy, 50, 150)
    
    # -> Canny cho ảnh tương phản thấp: 
    # Cần bộ ngưỡng (threshold) cực kỳ thấp để bắt được cạnh vì gradient nhỏ
    blur_lc = cv2.GaussianBlur(img_low_contrast, (5, 5), 1.0)
    edges_low_contrast = cv2.Canny(blur_lc, 15, 40)
    
    # -> Canny cho ảnh nhiều chi tiết: 
    # Cần bộ ngưỡng cao để lọc bớt nhiễu dăm/chi tiết nhỏ không mong muốn
    blur_det = cv2.GaussianBlur(img_detailed, (3, 3), 1.0)
    edges_detailed = cv2.Canny(blur_det, 150, 250)

    # 3. Trực quan hóa và Đánh giá kết quả
    plt.figure(figsize=(15, 10))
    
    # ----- Ảnh nhiễu -----
    plt.subplot(3, 2, 1)
    plt.title("1a. Anh nhieu (Noisy Gaussian)")
    plt.imshow(img_noisy, cmap="gray")
    plt.axis("off")
    
    plt.subplot(3, 2, 2)
    plt.title("1b. Canny - Anh nhieu\n(Blur manh: kernel=7x7, sigma=2.5, thresh=50,150)")
    plt.imshow(edges_noisy, cmap="gray")
    plt.axis("off")

    # ----- Ảnh tương phản thấp -----
    plt.subplot(3, 2, 3)
    plt.title("2a. Anh tuong phan thap (Low Contrast)")
    # Giữ vmin=0, vmax=255 để thấy rõ ảnh bị tối và nhạt đi so với khoảng màu chuẩn
    plt.imshow(img_low_contrast, cmap="gray", vmin=0, vmax=255)
    plt.axis("off")
    
    plt.subplot(3, 2, 4)
    plt.title("2b. Canny - Tuong phan thap\n(Thresh rat thap: 15, 40)")
    plt.imshow(edges_low_contrast, cmap="gray")
    plt.axis("off")
    
    # ----- Ảnh nhiều chi tiết -----
    plt.subplot(3, 2, 5)
    plt.title("3a. Anh nhieu chi tiet (Sharpened)")
    plt.imshow(img_detailed, cmap="gray")
    plt.axis("off")
    
    plt.subplot(3, 2, 6)
    plt.title("3b. Canny - Nhieu chi tiet\n(Thresh cao: 150, 250 de loc chi tiet nho)")
    plt.imshow(edges_detailed, cmap="gray")
    plt.axis("off")

    plt.suptitle("THUC HANH II.3: CANNY TREN CAC LOAI ANH KHAC NHAU (THANH VIEN 6: VINH)", fontsize=16, fontweight="bold")
    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.show()

    # In kết luận ra màn hình Console
    print("=" * 70)
    print("ĐÁNH GIÁ VÀ KẾT LUẬN (PHẦN II.3) - THÀNH VIÊN 6: VINH")
    print("=" * 70)
    print("1. Ảnh có nhiều nhiễu (Noisy Image):")
    print("   - Vấn đề: Canny rất nhạy cảm với nhiễu vì nó sử dụng đạo hàm để tìm gradient.")
    print("     Nhiễu làm tăng gradient đột biến, tạo ra vô số cạnh giả.")
    print("   - Giải pháp: Cần áp dụng bộ lọc Gaussian (làm mờ) mạnh hơn (kernel kích thước lớn, ")
    print("     sigma lớn) trước khi tính Canny để khử bớt nhiễu hạt.")
    print()
    print("2. Ảnh có độ tương phản thấp (Low Contrast Image):")
    print("   - Vấn đề: Cường độ sáng giữa các vùng thay đổi rất ít, dẫn đến gradient rất yếu.")
    print("     Nếu dùng ngưỡng mặc định (VD: 100-200), Canny sẽ bỏ qua hoàn toàn các cạnh.")
    print("   - Giải pháp: Bắt buộc phải hạ thấp bộ ngưỡng Low Threshold và High Threshold ")
    print("     (VD: 15-40) để thuật toán có thể bắt được các cạnh mờ nhạt đó.")
    print()
    print("3. Ảnh có nhiều chi tiết (High Detail Image):")
    print("   - Vấn đề: Thuật toán Canny sẽ trả về cực kỳ nhiều cạnh vụn vặt, các chi tiết nhỏ")
    print("     lẻ (như kết cấu bề mặt, tóc) khiến hình ảnh bị rối rắm, nhiễu loạn thông tin.")
    print("   - Giải pháp: Cần tăng giá trị High Threshold (VD: 150-250) để lọc bớt những cạnh ")
    print("     không quan trọng (gradient yếu) và chỉ giữ lại cấu trúc chính của đối tượng.")
    print("=" * 70)

if __name__ == "__main__":
    main()
