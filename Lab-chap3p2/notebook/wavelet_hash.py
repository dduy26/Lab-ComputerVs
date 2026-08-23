import os
import cv2
import numpy as np
import pywt
import matplotlib.pyplot as plt
from PIL import Image

# Xác định thư mục gốc của phân đoạn bài tập (Lab-chap3p2)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

def resolve_path(image_path):
    """
    Tự động giải quyết đường dẫn ảnh thông minh:
    Nếu đường dẫn truyền vào chưa tuyệt đối và không tồn tại theo CWD hiện tại,
    sẽ tìm kiếm đường dẫn tương đối tính từ BASE_DIR (Lab-chap3p2).
    """
    if os.path.isabs(image_path) and os.path.exists(image_path):
        return image_path
    if os.path.exists(image_path):
        return image_path
        
    alt_path = os.path.join(BASE_DIR, image_path)
    if os.path.exists(alt_path):
        return alt_path
        
    raise FileNotFoundError(f"Không tìm thấy file ảnh tại: '{image_path}' hoặc '{alt_path}'")

def preprocess_image_cv2(image_path, target_size=(256, 256)):
    """
    Tiền xử lý ảnh sử dụng thư viện OpenCV:
    1. Đọc ảnh từ file (Hỗ trợ đường dẫn Unicode tiếng Việt).
    2. Chuyển đổi sang mức xám (Grayscale) nếu là ảnh màu.
    3. Chuẩn hóa kích thước (Resize) về target_size.
    """
    full_path = resolve_path(image_path)
    
    # Sử dụng np.fromfile và cv2.imdecode để tránh lỗi Unicode path trên Windows (ví dụ: 'Xử lí ảnh')
    img_array = np.fromfile(full_path, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError(f"Không thể đọc ảnh từ đường dẫn: {full_path}")
        
    # Chuyển sang ảnh mức xám nếu là ảnh màu (3 kênh BGR)
    if len(img.shape) == 3 and img.shape[2] == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
        
    # Resize ảnh về kích thước cố định để chuẩn hóa
    resized = cv2.resize(gray, target_size, interpolation=cv2.INTER_AREA)
    return resized

def preprocess_image_pil(image_path, target_size=(256, 256)):
    """
    Tiền xử lý ảnh sử dụng thư viện PIL (Pillow):
    1. Đọc ảnh từ file.
    2. Chuyển đổi sang mức xám (Grayscale).
    3. Chuẩn hóa kích thước (Resize) về target_size.
    """
    full_path = resolve_path(image_path)
    img = Image.open(full_path)
    # Chuyển sang mức xám ('L' mode)
    gray = img.convert('L')
    # Resize ảnh về kích thước cố định
    resized = gray.resize(target_size, Image.Resampling.LANCZOS)
    return np.array(resized)

def wavelet_hash(img_array, wavelet='haar', level=3, hash_size=8):
    """
    Tính mã băm Wavelet (wHash / Wavelet Hash) cho mảng ảnh xám:
    - Bước 1: Biến đổi Wavelet 2D nhiều cấp (pywt.wavedec2).
    - Bước 2: Trích xuất băng tần tần số thấp LL (Approximation).
    - Bước 3: Lượng tử hóa các hệ số bằng giá trị Trung vị (Median).
    - Bước 4: Tạo mã băm nhị phân (Binary Hash) và chuỗi Hex.
    """
    # Bước 1: Biến đổi Wavelet 2D
    coeffs = pywt.wavedec2(img_array, wavelet=wavelet, level=level)
    
    # Băng tần LL (Low-Low frequency approximation) nằm ở vị trí đầu tiên
    ll_coeffs = coeffs[0]
    
    # Crop hoặc resize ma trận LL về kích thước hash_size x hash_size (vd: 8x8 = 64 bits)
    ll_resized = cv2.resize(ll_coeffs, (hash_size, hash_size), interpolation=cv2.INTER_AREA)
    
    # Bước 2: Lượng tử hóa hệ số (Quantization)
    # Tính giá trị trung vị (Median) của băng tần LL
    median_val = np.median(ll_resized)
    
    # Lượng tử hóa: 1 nếu hệ số >= median, ngược lại 0
    quantized_matrix = (ll_resized >= median_val).astype(int)
    
    # Bước 3: Tạo mã băm nhị phân (Binary hash vector)
    binary_hash = quantized_matrix.flatten()
    
    # Chuyển mã nhị phân thành chuỗi Hexadecimal để dễ lưu trữ
    hex_hash = ""
    for i in range(0, len(binary_hash), 4):
        chunk = binary_hash[i:i+4]
        digit = sum(b << (3 - idx) for idx, b in enumerate(chunk))
        hex_hash += hex(digit)[2:]
        
    return {
        "binary_hash": binary_hash,
        "hex_hash": hex_hash,
        "quantized_matrix": quantized_matrix,
        "ll_coeffs": ll_coeffs,
        "full_coeffs": coeffs
    }

def hamming_distance(hash1, hash2):
    """
    Tính Khoảng cách Hamming giữa 2 mã băm nhị phân:
    Đếm số lượng bit khác biệt giữa 2 chuỗi băm.
    """
    b1 = hash1["binary_hash"]
    b2 = hash2["binary_hash"]
    if len(b1) != len(b2):
        raise ValueError("Hai mã băm phải có cùng độ dài bit!")
        
    # Tính số bit khác nhau (XOR)
    diff_bits = np.count_nonzero(b1 != b2)
    similarity_pct = (1.0 - diff_bits / len(b1)) * 100.0
    return diff_bits, similarity_pct

def visualize_wavelet_hash(image_path, lib_type="cv2"):
    """
    Trực quan hóa toàn bộ quy trình Hash Wavelet của một ảnh:
    - Ảnh gốc / Ảnh xám
    - Biến đổi Wavelet 2D Cấp 1 (LL, LH, HL, HH)
    - Băng tần LL sau biến đổi
    - Ma trận nhị phân lượng tử hóa
    """
    if lib_type == "cv2":
        img_gray = preprocess_image_cv2(image_path, target_size=(256, 256))
    else:
        img_gray = preprocess_image_pil(image_path, target_size=(256, 256))
        
    hash_result = wavelet_hash(img_gray, wavelet='haar', level=3, hash_size=8)
    
    # Biến đổi DWT level 1 để trực quan hóa 4 băng tần LL, LH, HL, HH
    coeffs_lvl1 = pywt.dwt2(img_gray, 'haar')
    LL, (LH, HL, HH) = coeffs_lvl1
    
    fig, axes = plt.subplots(2, 3, figsize=(14, 8))
    
    axes[0, 0].imshow(img_gray, cmap='gray')
    axes[0, 0].set_title(f"1. Anh xam chuan hoa (256x256)\n[{lib_type.upper()}]")
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(LL, cmap='gray')
    axes[0, 1].set_title("2. Bang tan LL (Tan so thap)")
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(LH, cmap='gray')
    axes[0, 2].set_title("3. Bang tan LH (Chi tiet ngang)")
    axes[0, 2].axis('off')
    
    axes[1, 0].imshow(HL, cmap='gray')
    axes[1, 0].set_title("4. Bang tan HL (Chi tiet doc)")
    axes[1, 0].axis('off')
    
    axes[1, 1].imshow(HH, cmap='gray')
    axes[1, 1].set_title("5. Bang tan HH (Chi tiet cheo)")
    axes[1, 1].axis('off')
    
    axes[1, 2].imshow(hash_result["quantized_matrix"], cmap='binary')
    axes[1, 2].set_title(f"6. Ma bam Nhi phan 8x8 (64-bit)\nHex: {hash_result['hex_hash']}")
    axes[1, 2].axis('off')
    
    plt.suptitle("QUY TRINH TAO MA BAM WAVELET HASH (wHash)", fontsize=14, fontweight='bold')
    plt.tight_layout()
    
    output_dir = os.path.join(BASE_DIR, "data", "output")
    os.makedirs(output_dir, exist_ok=True)
    out_file = os.path.join(output_dir, f"wavelet_hash_visualization_{lib_type}.png")
    plt.savefig(out_file, dpi=150)
    print(f"[+] Da luu bieu do truc quan hoa tai: {out_file}")
    plt.close()

# ==============================================================================
# CHƯƠNG TRÌNH CHÍNH (MAIN FUNCTION)
# ==============================================================================
if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 70)
    print("THỰC HÀNH BĂM HÌNH ẢNH WAVELET (WAVELET HASHING) - BÀI THỰC HÀNH 4")
    print("=" * 70)
    
    img1_path = os.path.join(BASE_DIR, "data", "input", "meme.jpg")
    img2_path = os.path.join(BASE_DIR, "data", "input", "memetest.jpg")
    
    # 1. Thực nghiệm đọc ảnh bằng OpenCV và PIL
    print("\n[1] XỬ LÝ ẢNH ĐẦU VÀO BẰNG OPENCV...")
    gray_cv2_1 = preprocess_image_cv2(img1_path, target_size=(256, 256))
    gray_cv2_2 = preprocess_image_cv2(img2_path, target_size=(256, 256))
    
    print("[2] XỬ LÝ ẢNH ĐẦU VÀO BẰNG PIL (PILLOW)...")
    gray_pil_1 = preprocess_image_pil(img1_path, target_size=(256, 256))
    gray_pil_2 = preprocess_image_pil(img2_path, target_size=(256, 256))
    
    # 2. Tính mã băm Wavelet Hash
    hash1_cv = wavelet_hash(gray_cv2_1, wavelet='haar', level=3, hash_size=8)
    hash2_cv = wavelet_hash(gray_cv2_2, wavelet='haar', level=3, hash_size=8)
    
    hash1_pil = wavelet_hash(gray_pil_1, wavelet='haar', level=3, hash_size=8)
    hash2_pil = wavelet_hash(gray_pil_2, wavelet='haar', level=3, hash_size=8)
    
    print("\n" + "-" * 50)
    print("KẾT QUẢ MÃ BĂM WAVELET HASH (64-BIT):")
    print("-" * 50)
    print(f"Ảnh 1 (meme.jpg) [OpenCV]: {hash1_cv['hex_hash']}")
    print(f"Ảnh 2 (memetest.jpg) [OpenCV]: {hash2_cv['hex_hash']}")
    print(f"Ảnh 1 (meme.jpg) [PIL]:    {hash1_pil['hex_hash']}")
    print(f"Ảnh 2 (memetest.jpg) [PIL]:    {hash2_pil['hex_hash']}")
    
    # 3. So sánh khoảng cách Hamming
    dist_cv, sim_cv = hamming_distance(hash1_cv, hash2_cv)
    dist_pil, sim_pil = hamming_distance(hash1_pil, hash2_pil)
    
    print("\n" + "-" * 50)
    print("KẾT QUẢ SO SÁNH SỰ TƯƠNG ĐỒNG (HAMMING DISTANCE):")
    print("-" * 50)
    print(f"[OpenCV] Khoảng cách Hamming: {dist_cv} / 64 bits | Độ tương đồng: {sim_cv:.2f}%")
    print(f"[PIL]    Khoảng cách Hamming: {dist_pil} / 64 bits | Độ tương đồng: {sim_pil:.2f}%")
    
    if dist_cv <= 10:
        print("=> ĐÁNH GIÁ: Hai hình ảnh TƯƠNG ĐỒNG / GIỐNG NHAU!")
    else:
        print("=> ĐÁNH GIÁ: Hai hình ảnh KHÁC NHAU!")
        
    print("\n[3] TRỰC QUAN HÓA TOÀN BỘ BẰNG BIỂU ĐỒ...")
    visualize_wavelet_hash(img1_path, lib_type="cv2")
