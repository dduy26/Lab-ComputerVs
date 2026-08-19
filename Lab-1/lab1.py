import cv2
from PIL import Image

# 1. Đọc và hiển thị ảnh bằng OpenCV
img_path = 'meme.jpg'
image = cv2.imread(img_path)

if image is None:
    print("Không tìm thấy ảnh! Hãy kiểm tra lại tên file.")
else:
    print("Đọc ảnh thành công!")

    # 2. Chuyển đổi không gian màu (RGB sang Grayscale và HSV)[cite: 2]
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # 3. Thay đổi kích thước (Resize) và Cắt xén (Crop) ảnh[cite: 2]
    # Resize về kích thước cố định 300x300
    resized_image = cv2.resize(image, (300, 300))
    
    # Cắt ảnh (Crop vùng từ y: 50->200, x: 50->200)
    cropped_image = image[50:200, 50:200]

    # 4. Vẽ hình cơ bản và thêm văn bản lên ảnh[cite: 2]
    # Vẽ hình chữ nhật (ảnh, điểm đầu, điểm cuối, màu BGR, độ dày)
    cv2.rectangle(image, (50, 50), (200, 200), (0, 255, 0), 2)
    # Thêm chữ lên ảnh
    cv2.putText(image, 'Lab 1 OpenCV', (50, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # 5. Lưu hình ảnh đã xử lý lại với định dạng/tên mới[cite: 2]
    cv2.imwrite('output_gray.jpg', gray_image)
    cv2.imwrite('output_processed.jpg', image)
    print("Đã xử lý và lưu các file ảnh thành công!")