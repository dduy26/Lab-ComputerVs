import os
import cv2
import numpy as np
import pywt
import matplotlib.pyplot as plt
from PIL import Image

# Xác định thư mục gốc của bài tập (Lab-chap3p2) tính từ tệp notebook/code.py
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)

def resolve_path(image_path):
    """
    Tự động giải quyết đường dẫn ảnh thông minh:
    Hỗ trợ cả đường dẫn tuyệt đối lẫn đường dẫn tương đối tính từ BASE_DIR (Lab-chap3p2).
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
    1. Đọc ảnh bằng OpenCV (Hỗ trợ đường dẫn tiếng Việt Unicode trên Windows qua np.fromfile + cv2.imdecode).
    2. Chuyển đổi sang ảnh mức xám (Grayscale) nếu là ảnh màu (cv2.cvtColor).
    3. Chuẩn hóa kích thước (Resize) về target_size (cv2.resize).
    """
    full_path = resolve_path(image_path)
    
    # Đọc ảnh an toàn với đường dẫn tiếng Việt
    img_array = np.fromfile(full_path, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    
    if img is None:
        raise ValueError(f"Không thể đọc ảnh từ đường dẫn: {full_path}")
        
    # Chuyển sang mức xám nếu là ảnh màu BGR
    if len(img.shape) == 3 and img.shape[2] == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
        
    # Chuẩn hóa kích thước cố định
    resized = cv2.resize(gray, target_size, interpolation=cv2.INTER_AREA)
    return resized

def preprocess_image_pil(image_path, target_size=(256, 256)):
    """
    1. Đọc ảnh bằng thư viện PIL (Image.open).
    2. Chuyển sang mức xám (img.convert('L')).
    3. Chuẩn hóa kích thước (img.resize).
    """
    full_path = resolve_path(image_path)
    img = Image.open(full_path)
    gray = img.convert('L')
    resized = gray.resize(target_size, Image.Resampling.LANCZOS)
    return np.array(resized)

def wavelet_hash(img_array, wavelet='haar', level=3, hash_size=8):
    """
    Thuật toán Băm hình ảnh dựa trên Wavelet (Wavelet Hash / wHash):
    - Bước 1: Khử nhiễu & phân tách tần số 2D Wavelet DWT (pywt.wavedec2).
    - Bước 2: Trích xuất băng tần tần số thấp LL (Approximation).
    - Bước 3: Lượng tử hóa các hệ số bằng giá trị Trung vị (np.median).
    - Bước 4: Tạo mã băm nhị phân (Binary Hash) và chuỗi Hexadecimal.
    """
    # Bước 1: Biến đổi 2D Wavelet DWT (Phân tách tần số)
    coeffs = pywt.wavedec2(img_array, wavelet=wavelet, level=level)
    
    # Băng tần LL (Low-Low) chứa năng lượng & cấu trúc hình học chính
    ll_coeffs = coeffs[0]
    
    # Resize ma trận LL về kích thước hash_size x hash_size (8x8 = 64 bits)
    ll_resized = cv2.resize(ll_coeffs, (hash_size, hash_size), interpolation=cv2.INTER_AREA)
    
    # Bước 2: Lượng tử hóa hệ số (Quantization) bằng Trung vị (Median)
    median_val = np.median(ll_resized)
    quantized_matrix = (ll_resized >= median_val).astype(int)
    
    # Bước 3: Tạo mã băm nhị phân (Binary hash vector)
    binary_hash = quantized_matrix.flatten()
    
    # Chuyển mã nhị phân thành chuỗi Hexadecimal
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
    Tính Khoảng cách Hamming giữa 2 mã băm nhị phân (np.count_nonzero(b1 != b2)).
    """
    b1 = hash1["binary_hash"]
    b2 = hash2["binary_hash"]
    if len(b1) != len(b2):
        raise ValueError("Hai mã băm phải có cùng độ dài bit!")
        
    diff_bits = np.count_nonzero(b1 != b2)
    similarity_pct = (1.0 - diff_bits / len(b1)) * 100.0
    return diff_bits, similarity_pct

def visualize_wavelet_hash(image_path, lib_type="cv2"):
    """
    Trực quan hóa quy trình Wavelet Hash và lưu đồ thị vào data/output/.
    """
    if lib_type == "cv2":
        img_gray = preprocess_image_cv2(image_path, target_size=(256, 256))
    else:
        img_gray = preprocess_image_pil(image_path, target_size=(256, 256))
        
    hash_result = wavelet_hash(img_gray, wavelet='haar', level=3, hash_size=8)
    
    # Biến đổi DWT 2D level 1 (pywt.dwt2) để vẽ 4 băng tần LL, LH, HL, HH
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
# CHƯƠNG TRÌNH THỰC THI (MAIN EXECUTION)
# ==============================================================================
if __name__ == "__main__":
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 70)
    print("THỰC HÀNH BĂM HÌNH ẢNH WAVELET (WAVELET HASHING) - NOTEBOOK/CODE.PY")
    print("=" * 70)
    
    img1_path = os.path.join(BASE_DIR, "data", "input", "meme.jpg")
    img2_path = os.path.join(BASE_DIR, "data", "input", "memetest.jpg")
    
    # 1. Tiền xử lý bằng OpenCV và PIL
    print("\n[1] XỬ LÝ ẢNH ĐẦU VÀO BẰNG OPENCV (preprocess_image_cv2)...")
    gray_cv2_1 = preprocess_image_cv2(img1_path, target_size=(256, 256))
    gray_cv2_2 = preprocess_image_cv2(img2_path, target_size=(256, 256))
    
    print("[2] XỬ LÝ ẢNH ĐẦU VÀO BẰNG PIL (preprocess_image_pil)...")
    gray_pil_1 = preprocess_image_pil(img1_path, target_size=(256, 256))
    gray_pil_2 = preprocess_image_pil(img2_path, target_size=(256, 256))
    
    # 2. Biến đổi Wavelet & Tính mã băm (wavelet_hash)
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
    
    # 3. So sánh khoảng cách Hamming (hamming_distance)
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
        
    print("\n[3] TRỰC QUAN HÓA TOÀN BỘ BẰNG BIỂU ĐỒ (visualize_wavelet_hash)...")
    visualize_wavelet_hash(img1_path, lib_type="cv2")

# ---
# PHẦN XÂY DỰNG ỨNG DỤNG TÌM KIẾM HÌNH ẢNH (III.2)
import json
import time
import argparse
from typing import Dict, List, Tuple


def build_database(image_dir: str, db_path: str, wavelet: str = 'haar', level: int = 3, hash_size: int = 8) -> None:
    """
    Xây dựng cơ sở dữ liệu mã băm wavelet cho tất cả ảnh trong thư mục.
    
    Args:
        image_dir: Đường dẫn thư mục chứa ảnh (duyệt đệ quy).
        db_path: Đường dẫn file JSON để lưu database.
        wavelet: Loại wavelet (mặc định 'haar').
        level: Số cấp phân tách Wavelet.
        hash_size: Kích thước mã băm (8 → 64 bit).
    """
    db = {}
    supported_ext = ('.jpg', '.jpeg', '.png', '.bmp', '.webp')
    
    print(f"[*] Đang duyệt thư mục: {image_dir}")
    start_time = time.time()
    count = 0
    
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.lower().endswith(supported_ext):
                full_path = os.path.join(root, file)
                try:
                    # Tiền xử lý ảnh
                    img_array = preprocess_image_cv2(full_path, target_size=(256, 256))
                    # Tính hash
                    hash_result = wavelet_hash(img_array, wavelet=wavelet, level=level, hash_size=hash_size)
                    db[full_path] = hash_result['hex_hash']
                    count += 1
                    if count % 10 == 0:
                        print(f"  Đã xử lý {count} ảnh...")
                except Exception as e:
                    print(f"  [!] Lỗi với file {full_path}: {e}")
    
    # Lưu database
    with open(db_path, 'w', encoding='utf-8') as f:
        json.dump(db, f, indent=2, ensure_ascii=False)
    
    elapsed = time.time() - start_time
    print(f"[✓] Đã xây dựng database với {count} ảnh trong {elapsed:.2f} giây.")
    print(f"[✓] Lưu tại: {db_path}")


def load_database(db_path: str) -> Dict[str, str]:
    """Tải database từ file JSON."""
    with open(db_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def search(query_path: str, db_path: str, top_k: int = 5, wavelet: str = 'haar', level: int = 3, hash_size: int = 8) -> List[Tuple[str, int, float]]:
    """
    Tìm kiếm ảnh tương tự với ảnh truy vấn.
    
    Returns:
        List of tuples (image_path, hamming_distance, similarity_percent)
    """
    # 1. Tính hash cho ảnh query
    img_query = preprocess_image_cv2(query_path, target_size=(256, 256))
    hash_query = wavelet_hash(img_query, wavelet=wavelet, level=level, hash_size=hash_size)
    hex_query = hash_query['hex_hash']
    bin_query = hash_query['binary_hash']
    
    # 2. Tải database
    db = load_database(db_path)
    
    # 3. Tính khoảng cách Hamming với từng ảnh
    results = []
    for path, hex_hash in db.items():
        # Chuyển hex sang binary để so sánh (có thể tối ưu bằng cách lưu sẵn binary)
        # Ở đây ta chuyển hex sang binary mỗi lần để đơn giản
        # Có thể cải tiến bằng cách lưu binary trong DB
        bin_db = wavelet_hash(preprocess_image_cv2(path), wavelet=wavelet, level=level, hash_size=hash_size)['binary_hash']
        # Nếu muốn nhanh hơn, có thể lưu cả binary trong DB, nhưng ở đây làm lại để minh họa
        # Hoặc ta có thể chuyển hex sang binary:
        # bin_db = bytes.fromhex(hex_hash)  # nhưng cần chuyển sang bit
        # Ta dùng lại hàm wavelet_hash để nhất quán
        # Tuy nhiên, để tăng tốc, ta có thể cache binary trong DB
        # Ở đây, vì số lượng ảnh nhỏ, ta tính lại.
        # Có thể cải tiến bằng cách lưu binary trong DB.
        # Tạm thời, ta dùng cách này:
        hamming_dist, similarity = hamming_distance(
            {'binary_hash': bin_query, 'hex_hash': hex_query},
            {'binary_hash': bin_db, 'hex_hash': ''}
        )
        results.append((path, hamming_dist, similarity))
    
    # 4. Sắp xếp theo khoảng cách tăng dần (giống nhất)
    results.sort(key=lambda x: x[1])
    
    return results[:top_k]


def cli():
    """Giao diện dòng lệnh cho ứng dụng tìm kiếm."""
    parser = argparse.ArgumentParser(description='Ứng dụng tìm kiếm ảnh bằng Wavelet Hash')
    subparsers = parser.add_subparsers(dest='command', required=True, help='Lệnh cần thực hiện')
    
    # Lệnh build
    parser_build = subparsers.add_parser('build', help='Xây dựng database từ thư mục ảnh')
    parser_build.add_argument('--image-dir', required=True, help='Thư mục chứa ảnh')
    parser_build.add_argument('--db', default='wavelet_db.json', help='Đường dẫn file database (JSON)')
    parser_build.add_argument('--wavelet', default='haar', help='Loại wavelet')
    parser_build.add_argument('--level', type=int, default=3, help='Số cấp phân tách')
    parser_build.add_argument('--hash-size', type=int, default=8, help='Kích thước hash (8 → 64 bit)')
    
    # Lệnh search
    parser_search = subparsers.add_parser('search', help='Tìm kiếm ảnh tương tự')
    parser_search.add_argument('--query', required=True, help='Đường dẫn ảnh truy vấn')
    parser_search.add_argument('--db', default='wavelet_db.json', help='Đường dẫn file database')
    parser_search.add_argument('--top-k', type=int, default=5, help='Số lượng kết quả trả về')
    parser_search.add_argument('--wavelet', default='haar', help='Loại wavelet')
    parser_search.add_argument('--level', type=int, default=3, help='Số cấp phân tách')
    parser_search.add_argument('--hash-size', type=int, default=8, help='Kích thước hash')
    
    args = parser.parse_args()
    
    if args.command == 'build':
        build_database(args.image_dir, args.db, args.wavelet, args.level, args.hash_size)
    
    elif args.command == 'search':
        # Kiểm tra database tồn tại
        if not os.path.exists(args.db):
            print(f"[!] Database {args.db} không tồn tại. Hãy chạy lệnh build trước.")
            return
        
        start_time = time.time()
        results = search(args.query, args.db, args.top_k, args.wavelet, args.level, args.hash_size)
        elapsed = time.time() - start_time
        
        print(f"\n[Kết quả tìm kiếm] (thời gian: {elapsed*1000:.2f} ms)")
        print(f"Top {len(results)} ảnh giống nhất:")
        for idx, (path, dist, sim) in enumerate(results, 1):
            print(f"{idx}. {os.path.basename(path)} | Hamming: {dist}/64 | Độ tương đồng: {sim:.2f}%")
            print(f"   {path}")
    else:
        parser.print_help()


# Thêm vào main hiện tại để gọi CLI khi chạy trực tiếp
if __name__ == "__main__":
    # Nếu có đối số dòng lệnh, chạy CLI, ngược lại chạy demo cũ
    if len(sys.argv) > 1:
        cli()
    else:
        # ... (giữ nguyên phần demo cũ)
        pass
