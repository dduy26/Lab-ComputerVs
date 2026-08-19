import cv2
from PIL import Image
import numpy as np
import os

def process_image():
    # 1. Cài đặt thư viện: Đã giả định người dùng đã cài đặt bằng pip install opencv-python Pillow

    # Đường dẫn đến file ảnh mẫu
    # Đảm bảo bạn có một file ảnh trong thư mục này, ví dụ: 'sample.jpg' hoặc 'sample.png'
    image_path = 'D:\\Xử Lí Ảnh\\Lab\\Lab 1\\sample.jpg' # Hoặc 'sample.png'

    # Tạo thư mục output_images nếu chưa tồn tại
    output_dir = 'D:\\Xử Lí Ảnh\\Lab\\Lab 1\\output_images'
    os.makedirs(output_dir, exist_ok=True)

    if not os.path.exists(image_path):
        print(f"Lỗi: Không tìm thấy file ảnh tại đường dẫn {image_path}")
        print("Vui lòng đảm bảo có một file ảnh (ví dụ: sample.jpg) trong thư mục này.")
        
        # Tạo một ảnh trống để tiếp tục các bước khác nếu không tìm thấy ảnh
        img_cv_color = np.zeros((300, 500, 3), dtype=np.uint8)
        img_cv_color[:] = (100, 50, 200) # Màu tím
        cv2.putText(img_cv_color, "No image found! Using blank.", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        print("Đang tạo một ảnh trống để minh họa các bước tiếp theo.")
        
        # Để đảm bảo các bước tiếp theo có thể chạy với ảnh trống này,
        # chúng ta sẽ lưu nó như ảnh gốc giả định
        cv2.imwrite(os.path.join(output_dir, 'blank_sample.jpg'), img_cv_color)
        image_path = os.path.join(output_dir, 'blank_sample.jpg')
        
    # 2. Đọc và hiển thị ảnh
    print(f"\n--- Phần 1: Đọc, Hiển thị và Lưu ảnh cơ bản ---")
    print(f"Đang đọc ảnh từ: {image_path}")
    
    # Đọc ảnh bằng OpenCV (mặc định BGR)
    original_image_cv = cv2.imread(image_path)
    if original_image_cv is None:
        print(f"Lỗi: Không thể đọc file ảnh {image_path} bằng OpenCV. Kiểm tra định dạng hoặc tính hợp lệ của ảnh.")
        return # Dừng nếu không thể đọc ảnh gốc
    else:
        print("Đọc ảnh thành công bằng OpenCV.")
        cv2.imshow("Original Image (OpenCV) - Press any key to close", original_image_cv)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # Đọc ảnh bằng Pillow (mặc định RGB)
    try:
        img_pil = Image.open(image_path)
        print("Đọc ảnh thành công bằng Pillow.")
        # Pillow không có hàm imshow trực tiếp, thường dùng để xử lý và lưu hoặc hiển thị qua thư viện khác (như matplotlib)
        # img_pil.show() # Hàm này sẽ mở ảnh bằng trình xem ảnh mặc định của hệ thống
    except Exception as e:
        print(f"Lỗi khi đọc ảnh bằng Pillow: {e}")
        img_pil = Image.fromarray(cv2.cvtColor(original_image_cv, cv2.COLOR_BGR2RGB)) # Dùng ảnh từ OpenCV nếu Pillow lỗi
        print("Đã tạo ảnh PIL từ ảnh OpenCV để tiếp tục.")


    # 3. Lưu hình ảnh đã xử lý lại dưới các định dạng và mức nén khác nhau.
    print("\nĐang lưu ảnh dưới các định dạng khác nhau...")

    # Lưu bằng OpenCV (original_image_cv)
    cv2.imwrite(os.path.join(output_dir, 'output_cv_default.png'), original_image_cv)
    print(f"Đã lưu ảnh PNG (OpenCV) tại: {os.path.join(output_dir, 'output_cv_default.png')}")

    # Lưu ảnh JPEG với chất lượng khác nhau (OpenCV)
    cv2.imwrite(os.path.join(output_dir, 'output_cv_high_quality.jpg'), original_image_cv, [cv2.IMWRITE_JPEG_QUALITY, 95])
    print(f"Đã lưu ảnh JPG chất lượng cao (OpenCV) tại: {os.path.join(output_dir, 'output_cv_high_quality.jpg')}")

    cv2.imwrite(os.path.join(output_dir, 'output_cv_low_quality.jpg'), original_image_cv, [cv2.IMWRITE_JPEG_QUALITY, 30])
    print(f"Đã lưu ảnh JPG chất lượng thấp (OpenCV) tại: {os.path.join(output_dir, 'output_cv_low_quality.jpg')}")

    # Chuyển đổi từ OpenCV BGR sang PIL RGB để lưu bằng Pillow
    img_pil_from_cv = Image.fromarray(cv2.cvtColor(original_image_cv, cv2.COLOR_BGR2RGB))
    img_pil_from_cv.save(os.path.join(output_dir, 'output_pil_default.png'))
    print(f"Đã lưu ảnh PNG (Pillow) tại: {os.path.join(output_dir, 'output_pil_default.png')}")

    img_pil_from_cv.save(os.path.join(output_dir, 'output_pil_high_quality.jpg'), quality=95)
    print(f"Đã lưu ảnh JPG chất lượng cao (Pillow) tại: {os.path.join(output_dir, 'output_pil_high_quality.jpg')}")

    img_pil_from_cv.save(os.path.join(output_dir, 'output_pil_low_quality.jpg'), quality=30)
    print(f"Đã lưu ảnh JPG chất lượng thấp (Pillow) tại: {os.path.join(output_dir, 'output_pil_low_quality.jpg')}")
    
    print("\n--- Hoàn thành phần 1 ---")

    # --- Phần 2: Chuyển đổi không gian màu ---
    print(f"\n--- Phần 2: Chuyển đổi không gian màu ---")

    # 1. Chuyển đổi sang Grayscale
    gray_image = cv2.cvtColor(original_image_cv, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Anh Xam (Grayscale) - Press any key to close", gray_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite(os.path.join(output_dir, "gray_image.jpg"), gray_image)
    print(f"Đã chuyển đổi và lưu ảnh Grayscale tại: {os.path.join(output_dir, 'gray_image.jpg')}")

    # 2. Chuyển đổi sang HSV
    hsv_image = cv2.cvtColor(original_image_cv, cv2.COLOR_BGR2HSV)
    cv2.imshow("Anh HSV - Press any key to close", hsv_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite(os.path.join(output_dir, "hsv_image.png"), hsv_image) # HSV thường được lưu dưới dạng PNG để tránh mất mát dữ liệu
    print(f"Đã chuyển đổi và lưu ảnh HSV tại: {os.path.join(output_dir, 'hsv_image.png')}")

    # 3. Chuyển đổi sang LAB
    lab_image = cv2.cvtColor(original_image_cv, cv2.COLOR_BGR2LAB)
    cv2.imshow("Anh LAB - Press any key to close", lab_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite(os.path.join(output_dir, "lab_image.png"), lab_image) # LAB thường được lưu dưới dạng PNG để tránh mất mát dữ liệu
    print(f"Đã chuyển đổi và lưu ảnh LAB tại: {os.path.join(output_dir, 'lab_image.png')}")

    print("\n--- Hoàn thành phần 2: Các chuyển đổi không gian màu ---")
    print(f"Tất cả các ảnh đầu ra được lưu trong thư mục: {output_dir}")

if __name__ == "__main__":
    process_image()
