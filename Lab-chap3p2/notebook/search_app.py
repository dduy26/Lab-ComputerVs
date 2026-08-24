"""
Ứng dụng tìm kiếm hình ảnh bằng Wavelet Hash (Phước – III.2)
Sử dụng các hàm core từ code.py
"""
import os
import sys
import json
import time
import argparse
from typing import Dict, List, Tuple

# Import các hàm từ code.py
from code import preprocess_image_cv2, wavelet_hash, hamming_distance


def build_database(image_dir: str, db_path: str, wavelet: str = 'haar', level: int = 3, hash_size: int = 8) -> None:
    """
    Xây dựng database từ thư mục ảnh.
    
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
    
    for root, _, files in os.walk(image_dir):
        for file in files:
            if file.lower().endswith(supported_ext):
                full_path = os.path.join(root, file)
                try:
                    img_array = preprocess_image_cv2(full_path, target_size=(256, 256))
                    hash_result = wavelet_hash(img_array, wavelet=wavelet, level=level, hash_size=hash_size)
                    db[full_path] = hash_result['hex_hash']
                    count += 1
                    if count % 10 == 0:
                        print(f"  Đã xử lý {count} ảnh...")
                except Exception as e:
                    print(f"  [!] Lỗi với file {full_path}: {e}")
    
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
    bin_query = hash_query['binary_hash']
    
    # 2. Tải database
    db = load_database(db_path)
    
    results = []
    for path, hex_hash in db.items():
        # Tính hash cho từng ảnh trong DB (có thể cache để tăng tốc)
        # Với số lượng ảnh nhỏ, tính lại trực tiếp là đơn giản nhất.
        img_db = preprocess_image_cv2(path, target_size=(256, 256))
        bin_db = wavelet_hash(img_db, wavelet=wavelet, level=level, hash_size=hash_size)['binary_hash']
        
        hamming_dist, similarity = hamming_distance(
            {'binary_hash': bin_query, 'hex_hash': ''},
            {'binary_hash': bin_db, 'hex_hash': ''}
        )
        results.append((path, hamming_dist, similarity))
    
    # 4. Sắp xếp theo khoảng cách tăng dần (giống nhất)
    results.sort(key=lambda x: x[1])
    
    return results[:top_k]


def cli():
    """Giao diện dòng lệnh cho ứng dụng tìm kiếm."""
    parser = argparse.ArgumentParser(description='Tìm kiếm ảnh bằng Wavelet Hash')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # Build
    p_build = subparsers.add_parser('build', help='Xây dựng database')
    p_build.add_argument('--image-dir', required=True, help='Thư mục ảnh')
    p_build.add_argument('--db', default='wavelet_db.json', help='File database JSON')
    p_build.add_argument('--wavelet', default='haar')
    p_build.add_argument('--level', type=int, default=3)
    p_build.add_argument('--hash-size', type=int, default=8)
    
    # Search
    p_search = subparsers.add_parser('search', help='Tìm kiếm ảnh')
    p_search.add_argument('--query', required=True, help='Đường dẫn ảnh truy vấn')
    p_search.add_argument('--db', default='wavelet_db.json', help='File database')
    p_search.add_argument('--top-k', type=int, default=5)
    p_search.add_argument('--wavelet', default='haar')
    p_search.add_argument('--level', type=int, default=3)
    p_search.add_argument('--hash-size', type=int, default=8)
    
    args = parser.parse_args()
    
    if args.command == 'build':
        build_database(args.image_dir, args.db, args.wavelet, args.level, args.hash_size)
    elif args.command == 'search':
        if not os.path.exists(args.db):
            print(f"[!] Database {args.db} không tồn tại.")
            return
        start = time.time()
        results = search(args.query, args.db, args.top_k, args.wavelet, args.level, args.hash_size)
        elapsed = time.time() - start
        print(f"\n[Kết quả tìm kiếm] (thời gian: {elapsed*1000:.2f} ms)")
        print(f"Top {len(results)} ảnh giống nhất:")
        for idx, (path, dist, sim) in enumerate(results, 1):
            print(f"{idx}. {os.path.basename(path)} | Hamming: {dist}/64 | Độ tương đồng: {sim:.2f}%")
            print(f"   {path}")
    else:
        parser.print_help()


if __name__ == "__main__":
    cli()