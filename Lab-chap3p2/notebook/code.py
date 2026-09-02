# -*- coding: utf-8 -*-
"""
MÃ NGUỒN TỔNG HỢP VÀ THỰC THI CHO LAB-CHAP3P2
SO SÁNH SỰ TƯƠNG ĐỒNG CỦA CÁC HÌNH ẢNH SỬ DỤNG WAVELET HASH (wHash)

Bao gồm phần làm việc của 7 thành viên theo đúng thứ tự 1 -> 7:
- Member 1: Thông (Phần I + II.1 + II.2 - Chuẩn bị dữ liệu & Trích xuất Wavelet 2D)
- Member 2: Đức (Phần II.3 + II.4 - Lượng tử hóa & Khoảng cách Hamming)
- Member 3: Duy (Phần II.5 - Đánh giá chỉ số & Biểu đồ ROC)
- Member 4: Thọ (Phần IV - Pipeline 3 bước baseline OpenCV/PIL)
- Member 5: Vinh (Phần V - Cải tiến wHash & Khảo sát 4 họ Wavelet)
- Member 6: Huy (Phần III.1 - Khảo sát 3 phương pháp băm Wavelet)
- Member 7: Phước (Phần III.2 - Ứng dụng Tìm kiếm Hình ảnh Top-K)
"""

import os
import glob
import time
import json
import cv2
import numpy as np
import pywt
import matplotlib.pyplot as plt
from PIL import Image

# Tự động xác định thư mục gốc của bài tập (Lab-chap3p2)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SCRIPT_DIR)
DATA_DIR = os.path.join(BASE_DIR, "data")
INPUT_DIR = os.path.join(DATA_DIR, "input")
OUTPUT_DIR = os.path.join(DATA_DIR, "output")

os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==============================================================================
# 🛠️ UTILITY FUNCTIONS: GIẢI QUYẾT ĐƯỜNG DẪN AN TOÀN
# ==============================================================================
def resolve_path(image_path):
    """
    Hỗ trợ đường dẫn tuyệt đối hoặc tương đối tính từ BASE_DIR (Lab-chap3p2).
    """
    if os.path.isabs(image_path) and os.path.exists(image_path):
        return image_path
    if os.path.exists(image_path):
        return image_path
    alt_path = os.path.join(BASE_DIR, image_path)
    if os.path.exists(alt_path):
        return alt_path
    alt_input = os.path.join(INPUT_DIR, image_path)
    if os.path.exists(alt_input):
        return alt_input
    raise FileNotFoundError(f"Không tìm thấy file ảnh tại: '{image_path}'")


# ==============================================================================
# 📌 MEMBER 1: THÔNG (PHẦN I + II.1 + II.2)
# Chuẩn bị dữ liệu & Trích xuất Wavelet đặc trưng 2D
# ==============================================================================
def preprocess_image_cv2(image_path, target_size=(256, 256)):
    """
    1. Đọc ảnh bằng OpenCV qua np.fromfile + cv2.imdecode (hỗ trợ Unicode tiếng Việt).
    2. Chuyển sang ảnh mức xám (Grayscale).
    3. Resize về target_size.
    """
    full_path = resolve_path(image_path)
    img_array = np.fromfile(full_path, dtype=np.uint8)
    img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError(f"Không thể đọc ảnh: {full_path}")
    if len(img.shape) == 3 and img.shape[2] == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img
    return cv2.resize(gray, target_size, interpolation=cv2.INTER_AREA)


def preprocess_image_pil(image_path, target_size=(256, 256)):
    """
    Đọc ảnh bằng thư viện PIL (Image.open), chuyển sang mức xám và resize.
    """
    full_path = resolve_path(image_path)
    img = Image.open(full_path)
    gray = img.convert('L')
    resized = gray.resize(target_size, Image.Resampling.LANCZOS)
    return np.array(resized)


def extract_wavelet_subbands(img_array, wavelet='haar', level=3):
    """
    Phân tách 2D DWT qua pywt.wavedec2.
    Trả về tuple coeffs: (cA, (cH3, cV3, cD3), ...)
    """
    return pywt.wavedec2(img_array, wavelet=wavelet, level=level)


# ==============================================================================
# 📌 MEMBER 2: ĐỨC (PHẦN II.3 + II.4)
# Quá trình Lượng tử hóa & So sánh Khoảng cách Hamming
# ==============================================================================
def wavelet_hash(img_array, wavelet='haar', level=3, hash_size=8, method='median'):
    """
    Tạo mã băm Wavelet Hash (wHash):
    - Bước 1: 2D DWT trích xuất băng tần LL.
    - Bước 2: Lượng tử hóa theo Median hoặc Mean.
    - Bước 3: Chuỗi bit 64-bit và mã Hex.
    """
    coeffs = pywt.wavedec2(img_array, wavelet=wavelet, level=level)
    ll_coeffs = coeffs[0]
    ll_resized = cv2.resize(ll_coeffs, (hash_size, hash_size), interpolation=cv2.INTER_AREA)

    if method == 'median':
        thresh = np.median(ll_resized)
    else:
        thresh = np.mean(ll_resized)

    quantized_matrix = (ll_resized >= thresh).astype(int)
    binary_hash = quantized_matrix.flatten()

    hex_hash = ""
    for i in range(0, len(binary_hash), 4):
        chunk = binary_hash[i:i + 4]
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
    Tính Khoảng cách Hamming = sum(b1 != b2)
    """
    b1 = hash1["binary_hash"] if isinstance(hash1, dict) else hash1
    b2 = hash2["binary_hash"] if isinstance(hash2, dict) else hash2
    if len(b1) != len(b2):
        raise ValueError("Hai mã băm phải có cùng độ dài bit!")
    diff_bits = int(np.count_nonzero(b1 != b2))
    similarity_pct = (1.0 - diff_bits / len(b1)) * 100.0
    return diff_bits, similarity_pct


def compare_image_pairs_demo():
    """
    Minh họa so sánh 3 cặp ảnh thực nghiệm.
    """
    img1_path = os.path.join(INPUT_DIR, "meme.jpg")
    img2_path = os.path.join(INPUT_DIR, "similar", "similar_meme_blur.png")
    img3_path = os.path.join(INPUT_DIR, "memetest.jpg")

    img1 = preprocess_image_cv2(img1_path)
    img2 = preprocess_image_cv2(img2_path) if os.path.exists(img2_path) else cv2.GaussianBlur(img1, (7, 7), 1.5)
    img3 = preprocess_image_cv2(img3_path)

    h1 = wavelet_hash(img1)
    h2 = wavelet_hash(img2)
    h3 = wavelet_hash(img3)

    d12, s12 = hamming_distance(h1, h2)
    d13, s13 = hamming_distance(h1, h3)

    print("\n--- MEMBER 2: SO SÁNH CÁC CẶP ẢNH MẪU ---")
    print(f"Cặp 1: meme.jpg vs meme.jpg            | Hamming: 0 / 64 bit  | Sim: 100.00% | Match")
    print(f"Cặp 2: meme.jpg vs similar_meme_blur   | Hamming: {d12:>2} / 64 bit | Sim: {s12:6.2f}% | {'Match' if d12 <= 10 else 'Mismatch'}")
    print(f"Cặp 3: meme.jpg vs memetest.jpg        | Hamming: {d13:>2} / 64 bit | Sim: {s13:6.2f}% | {'Match' if d13 <= 10 else 'Mismatch'}")


# ==============================================================================
# 📌 MEMBER 3: DUY (PHẦN II.5)
# Đánh giá các Chỉ số Hiệu suất & Đường cong ROC / AUC
# ==============================================================================
def evaluate_performance_and_roc(hamming_threshold=10):
    """
    Lập Confusion Matrix, tính Accuracy, Sensitivity, Specificity.
    Vẽ đường cong ROC và tính AUC bằng sklearn.metrics.
    """
    from sklearn.metrics import confusion_matrix, roc_curve, auc

    target_img_path = os.path.join(INPUT_DIR, "meme.jpg")
    target_img = preprocess_image_cv2(target_img_path)
    target_hash = wavelet_hash(target_img)

    similar_dir = os.path.join(INPUT_DIR, "similar")
    different_dir = os.path.join(INPUT_DIR, "different")

    y_true = []
    y_scores = []
    y_preds = []

    # Cặp ảnh Similar (Positive - 1)
    if os.path.exists(similar_dir):
        for f in os.listdir(similar_dir):
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                img = preprocess_image_cv2(os.path.join(similar_dir, f))
                h = wavelet_hash(img)
                dist, _ = hamming_distance(target_hash, h)
                score = 1.0 - (dist / 64.0)
                pred = 1 if dist <= hamming_threshold else 0
                y_true.append(1)
                y_scores.append(score)
                y_preds.append(pred)

    # Cặp ảnh Different (Negative - 0)
    diff_hashes = []
    if os.path.exists(different_dir):
        for f in os.listdir(different_dir):
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                img = preprocess_image_cv2(os.path.join(different_dir, f))
                h = wavelet_hash(img)
                diff_hashes.append(h)
                dist, _ = hamming_distance(target_hash, h)
                score = 1.0 - (dist / 64.0)
                pred = 1 if dist <= hamming_threshold else 0
                y_true.append(0)
                y_scores.append(score)
                y_preds.append(pred)

    for i in range(len(diff_hashes)):
        for j in range(i + 1, len(diff_hashes)):
            dist_ij, _ = hamming_distance(diff_hashes[i], diff_hashes[j])
            score_ij = 1.0 - (dist_ij / 64.0)
            pred_ij = 1 if dist_ij <= hamming_threshold else 0
            y_true.append(0)
            y_scores.append(score_ij)
            y_preds.append(pred_ij)

    y_true = np.array(y_true)
    y_scores = np.array(y_scores)
    y_preds = np.array(y_preds)

    cm = confusion_matrix(y_true, y_preds)
    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()
    else:
        tn = cm[0, 0] if len(cm) > 0 else 0
        fp, fn, tp = 0, 0, 0

    total = len(y_true)
    accuracy = (tp + tn) / total if total > 0 else 0.0
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    recall = sensitivity
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0

    fpr, tpr, _ = roc_curve(y_true, y_scores)
    roc_auc = auc(fpr, tpr)

    print("\n--- MEMBER 3: ĐÁNH GIÁ HIỆU SUẤT & ROC/AUC ---")
    print(f"Confusion Matrix            : TP={tp}, FP={fp}, FN={fn}, TN={tn}")
    print(f"Độ chính xác (Accuracy)     : {accuracy * 100:.2f}%")
    print(f"Độ nhạy (Recall/Sensitivity): {recall * 100:.2f}%")
    print(f"Độ đặc hiệu (Specificity)   : {specificity * 100:.2f}%")
    print(f"Precision (Độ xác thực)     : {precision * 100:.2f}%")
    print(f"ROC AUC                     : {roc_auc:.4f}")

    # Vẽ biểu đồ ROC
    plt.figure(figsize=(7, 5))
    plt.plot(fpr, tpr, color='darkorange', lw=2.5, label=f'ROC curve (AUC = {roc_auc:.4f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Random Chance')
    plt.xlim([-0.02, 1.02])
    plt.ylim([-0.02, 1.05])
    plt.xlabel('False Positive Rate (1 - Specificity)')
    plt.ylabel('True Positive Rate (Sensitivity)')
    plt.title('ĐƯỜNG CONG ROC - WAVELET HASH EVALUATION')
    plt.legend(loc="lower right")
    plt.grid(True, linestyle=':', alpha=0.6)
    roc_out = os.path.join(OUTPUT_DIR, "roc_curve_evaluation.png")
    plt.savefig(roc_out, dpi=150)
    plt.close()
    return accuracy, sensitivity, specificity, roc_auc


# ==============================================================================
# 📌 MEMBER 4: THỌ (PHẦN IV)
# Baseline 3-Step Pipeline với OpenCV & PIL & Code mẫu Slide 17
# ==============================================================================
def wavelet_hash_slide_baseline(image_path, wavelet='db4', level=3):
    """
    Code mẫu từ Slide 17 (Phần IV - Tham khảo):
    Sử dụng 2D DWT pywt.wavedec2, lượng tử hóa hệ số và gom nhị phân % 2.
    """
    full_path = resolve_path(image_path)
    img = preprocess_image_cv2(full_path)
    coeffs = pywt.wavedec2(img, wavelet=wavelet, level=level)
    coeffs_quant = [np.floor(np.abs(c) / 2.0).astype(int) for c in coeffs]
    flattened = np.concatenate([c.flatten() for c in coeffs_quant])
    hash_code = [int(bit) % 2 for bit in flattened]
    return hash_code


def baseline_3step_pipeline(img_path1, img_path2):
    """
    Quy trình 3 bước hoàn chỉnh: 2D-DWT -> Quantize -> Binary Hash.
    So sánh ảnh đọc bằng OpenCV và PIL.
    """
    gray_cv1 = preprocess_image_cv2(img_path1)
    gray_cv2_img = preprocess_image_cv2(img_path2)
    gray_pil1 = preprocess_image_pil(img_path1)
    gray_pil2 = preprocess_image_pil(img_path2)

    h_cv1 = wavelet_hash(gray_cv1)
    h_cv2 = wavelet_hash(gray_cv2_img)
    h_pil1 = preprocess_image_pil(img_path1)
    h_pil2 = preprocess_image_pil(img_path2)

    d_cv, _ = hamming_distance(h_cv1, h_cv2)

    # Thử nghiệm code slide mẫu
    hash_slide1 = wavelet_hash_slide_baseline(img_path1)
    hash_slide2 = wavelet_hash_slide_baseline(img_path2)
    dist_slide = sum(abs(a - b) for a, b in zip(hash_slide1, hash_slide2))

    print("\n--- MEMBER 4: PIPELINE BASELINE OPENCV VS PIL VS SLIDE MẪU ---")
    print(f"OpenCV Hash 1 : {h_cv1['hex_hash']} | Hash 2: {h_cv2['hex_hash']} | Dist: {d_cv}")
    print(f"Slide Sample  : Hash length {len(hash_slide1)} bits | Slide Hamming Dist: {dist_slide}")


# ==============================================================================
# 📌 MEMBER 5: VINH (PHẦN V)
# Cải tiến wHash & Khảo sát So sánh 4 họ Wavelet
# ==============================================================================
def wavelet_hash_enhanced(img_array, wavelet='haar', level=3, hash_size=8, normalize=True):
    """
    Cải tiến wHash: Chuẩn hóa Min-Max, xử lý exception, hash_size tùy chỉnh.
    """
    try:
        coeffs = pywt.wavedec2(img_array, wavelet=wavelet, level=level)
        ll = coeffs[0]
        ll_small = cv2.resize(ll, (hash_size, hash_size), interpolation=cv2.INTER_AREA)

        if normalize:
            ll_min, ll_max = ll_small.min(), ll_small.max()
            if ll_max > ll_min:
                ll_small = (ll_small - ll_min) / (ll_max - ll_min)

        med = np.median(ll_small)
        bit_arr = (ll_small >= med).astype(np.uint8).flatten()
        return bit_arr
    except Exception as e:
        print(f"[!] Lỗi wavelet_hash_enhanced: {e}")
        return np.zeros(hash_size * hash_size, dtype=np.uint8)


def benchmark_wavelet_families():
    """
    Khảo sát so sánh haar, db4, sym4, coif2 về Accuracy và Tốc độ.
    """
    target_img = preprocess_image_cv2(os.path.join(INPUT_DIR, "meme.jpg"))
    similar_dir = os.path.join(INPUT_DIR, "similar")
    diff_dir = os.path.join(INPUT_DIR, "different")

    wavelets = ['haar', 'db4', 'sym4', 'coif2']
    print("\n--- MEMBER 5: KHẢO SÁT SO SÁNH 4 HỌ WAVELET ---")
    print(f"{'Wavelet':<10} | {'Accuracy':<10} | {'Tốc độ (ms/ảnh)':<15}")
    print("-" * 42)

    for w in wavelets:
        t0 = time.time()
        target_h = wavelet_hash_enhanced(target_img, wavelet=w)

        correct = 0
        total = 0

        if os.path.exists(similar_dir):
            for f in os.listdir(similar_dir):
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                    img = preprocess_image_cv2(os.path.join(similar_dir, f))
                    h = wavelet_hash_enhanced(img, wavelet=w)
                    d = np.count_nonzero(target_h != h)
                    if d <= 10:
                        correct += 1
                    total += 1

        if os.path.exists(diff_dir):
            for f in os.listdir(diff_dir):
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                    img = preprocess_image_cv2(os.path.join(diff_dir, f))
                    h = wavelet_hash_enhanced(img, wavelet=w)
                    d = np.count_nonzero(target_h != h)
                    if d > 10:
                        correct += 1
                    total += 1

        elapsed = (time.time() - t0) * 1000 / max(1, total)
        acc = (correct / total) * 100 if total > 0 else 0
        print(f"{w:<10} | {acc:>8.1f}% | {elapsed:>12.3f} ms")


# ==============================================================================
# 📌 MEMBER 6: HUY (PHẦN III.1)
# Khảo sát 3 Phương pháp Băm Wavelet (LL vs Detail Energy vs Combined)
# ==============================================================================
def hash_ll(img_array):
    """PP1: Băm dựa trên băng tần LL."""
    LL, _ = pywt.dwt2(img_array, "haar")
    ll_sub = cv2.resize(LL, (8, 8), interpolation=cv2.INTER_AREA)
    med = np.median(ll_sub)
    return (ll_sub > med).astype(int).flatten()


def hash_energy(img_array):
    """PP2: Băm dựa trên Năng lượng hệ số chi tiết (LH, HL, HH)."""
    _, (LH, HL, HH) = pywt.dwt2(img_array, "haar")
    energies = []
    for band in [LH, HL, HH]:
        h, w = band.shape
        bh, bw = max(1, h // 8), max(1, w // 8)
        for i in range(8):
            for j in range(8):
                block = band[i * bh:(i + 1) * bh, j * bw:(j + 1) * bw]
                energies.append(np.sum(block ** 2))
    energies = np.array(energies)
    med = np.median(energies)
    return (energies > med).astype(int).flatten()


def hash_combined(img_array):
    """PP3: Kết hợp 45 bit LL + 19 bit Detail Energy."""
    h1 = hash_ll(img_array)
    h2 = hash_energy(img_array)
    return np.concatenate([h1[:45], h2[:19]])


def benchmark_hashing_methods():
    """
    So sánh 3 phương pháp băm trên cùng tập dữ liệu.
    """
    target_img = preprocess_image_cv2(os.path.join(INPUT_DIR, "meme.jpg"))
    similar_dir = os.path.join(INPUT_DIR, "similar")
    diff_dir = os.path.join(INPUT_DIR, "different")

    methods = {
        "PP1 (LL Hash)": hash_ll,
        "PP2 (Detail Energy)": hash_energy,
        "PP3 (Combined)": hash_combined
    }

    print("\n--- MEMBER 6: KHẢO SÁT 3 PHƯƠNG PHÁP BĂM WAVELET ---")
    print(f"{'Phương pháp':<20} | {'Accuracy':<10} | {'Thời gian (ms)':<14} | {'Độ phân biệt (Avg Diff)'}")
    print("-" * 65)

    for name, func in methods.items():
        t0 = time.time()
        target_h = func(target_img)
        correct = 0
        total = 0
        diff_dists = []

        if os.path.exists(similar_dir):
            for f in os.listdir(similar_dir):
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                    img = preprocess_image_cv2(os.path.join(similar_dir, f))
                    h = func(img)
                    d = np.sum(target_h != h)
                    if d <= 15:
                        correct += 1
                    total += 1

        if os.path.exists(diff_dir):
            for f in os.listdir(diff_dir):
                if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                    img = preprocess_image_cv2(os.path.join(diff_dir, f))
                    h = func(img)
                    d = np.sum(target_h != h)
                    diff_dists.append(d)
                    if d > 15:
                        correct += 1
                    total += 1

        elapsed = (time.time() - t0) * 1000 / max(1, total)
        acc = (correct / total) * 100 if total > 0 else 0
        avg_diff = np.mean(diff_dists) if diff_dists else 0
        print(f"{name:<20} | {acc:>8.1f}% | {elapsed:>11.3f} ms | {avg_diff:>12.2f} bits")


# ==============================================================================
# 📌 MEMBER 7: PHƯỚC (PHẦN III.2)
# Ứng dụng Tìm kiếm Hình ảnh Dựa trên Wavelet Hash
# ==============================================================================
def build_image_database(image_dir=INPUT_DIR, db_path=None):
    """
    Duyệt thư mục ảnh và tạo database JSON lưu mã băm.
    """
    if db_path is None:
        db_path = os.path.join(OUTPUT_DIR, "image_hashes.json")

    database = {}
    t0 = time.time()

    for root, _, files in os.walk(image_dir):
        for f in files:
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                full_path = os.path.join(root, f)
                try:
                    img = preprocess_image_cv2(full_path)
                    h_res = wavelet_hash(img)
                    rel_path = os.path.relpath(full_path, BASE_DIR)
                    database[rel_path] = {
                        "hex_hash": h_res["hex_hash"],
                        "binary_hash": h_res["binary_hash"].tolist()
                    }
                except Exception as e:
                    pass

    with open(db_path, "w", encoding="utf-8") as f:
        json.dump(database, f, indent=2)

    elapsed = time.time() - t0
    print(f"\n--- MEMBER 7: ĐÃ TẠO DATABASE TÌM KIẾM ---")
    print(f"[+] Số lượng ảnh indexed: {len(database)} | Thời gian: {elapsed:.3f}s | Lưu tại: {db_path}")
    return database, db_path


def search_similar_images(query_path, db_path=None, top_k=5):
    """
    Tìm kiếm Top K ảnh tương đồng nhất với ảnh Query.
    """
    if db_path is None:
        db_path = os.path.join(OUTPUT_DIR, "image_hashes.json")

    if not os.path.exists(db_path):
        build_image_database(INPUT_DIR, db_path)

    with open(db_path, "r", encoding="utf-8") as f:
        database = json.load(f)

    query_img = preprocess_image_cv2(query_path)
    query_hash = wavelet_hash(query_img)["binary_hash"]

    t0 = time.time()
    results = []

    for rel_path, item in database.items():
        db_bits = np.array(item["binary_hash"], dtype=int)
        dist = int(np.count_nonzero(query_hash != db_bits))
        sim = (1.0 - dist / len(query_hash)) * 100.0
        results.append((rel_path, dist, sim))

    results.sort(key=lambda x: x[1])
    elapsed_ms = (time.time() - t0) * 1000

    print(f"\n--- KẾT QUẢ TÌM KIẾM TOP {top_k} CHO QUERY: '{os.path.basename(query_path)}' (Thời gian: {elapsed_ms:.2f} ms) ---")
    for rank, (p, d, s) in enumerate(results[:top_k], 1):
        print(f"Top {rank}: {p:<45} | Hamming: {d:>2} | Similarity: {s:6.2f}%")

    return results[:top_k]


# ==============================================================================
# 🚀 MAIN EXECUTION FLOW
# ==============================================================================
if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    print("=" * 70)
    print("THỰC HÀNH BĂM HÌNH ẢNH WAVELET (LAB-CHAP3P2) - CODE.PY")
    print("=" * 70)

    # Member 1 & 2 Demo
    compare_image_pairs_demo()

    # Member 3 Demo
    evaluate_performance_and_roc()

    # Member 4 Demo
    img1 = os.path.join(INPUT_DIR, "meme.jpg")
    img2 = os.path.join(INPUT_DIR, "memetest.jpg")
    baseline_3step_pipeline(img1, img2)

    # Member 5 Demo
    benchmark_wavelet_families()

    # Member 6 Demo
    benchmark_hashing_methods()

    # Member 7 Demo
    db, db_file = build_image_database()
    search_similar_images(img1, db_file, top_k=5)

    print("\n" + "=" * 70)
    print("HOÀN THÀNH CHẠY THỰC THI TOÀN BỘ CÁC PHẦN (MEMBERS 1 - 7)")
    print("=" * 70)
