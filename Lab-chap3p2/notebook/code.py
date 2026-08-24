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

def evaluate_performance_and_roc(hamming_threshold=10):
    """
    Phần II.5 (Thành viên 3: Duy - random):
    - Đánh giá các chỉ số hiệu suất:
      + Accuracy = (TP + TN) / (TP + TN + FP + FN)
      + Sensitivity (Recall) = TP / (TP + FN)
      + Specificity = TN / (TN + FP)
    - Giải thích ý nghĩa AUC và vẽ đường cong ROC bằng sklearn.metrics.roc_curve và matplotlib.
    - Lưu biểu đồ đồ họa tại data/output/roc_curve_evaluation.png.
    """
    from sklearn.metrics import confusion_matrix, roc_curve, auc

    print("\n" + "=" * 70)
    print("PHẦN II.5: ĐÁNH GIÁ HIỆU SUẤT VÀ VẼ ĐƯỜNG CONG ROC (EVALUATION & ROC CURVE)")
    print("=" * 70)

    # 1. Thu thập dữ liệu thực nghiệm (Cặp ảnh tương đồng vs Cặp ảnh khác biệt)
    input_dir = os.path.join(BASE_DIR, "data", "input")
    target_img_path = os.path.join(input_dir, "meme.jpg")
    target_img = preprocess_image_cv2(target_img_path)
    target_hash = wavelet_hash(target_img)

    similar_dir = os.path.join(input_dir, "similar")
    different_dir = os.path.join(input_dir, "different")

    y_true = []      # 1: Tương đồng (Positive), 0: Khác biệt (Negative)
    y_scores = []    # Điểm tương đồng Similarity Score = (1 - dist / 64.0)
    y_preds = []     # Nhãn dự đoán nhị phân (dist <= hamming_threshold -> 1, nguoc lai -> 0)

    # Tập Cặp Ảnh TƯƠNG ĐỒNG (Positive Pairs)
    if os.path.exists(similar_dir):
        for f in os.listdir(similar_dir):
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                img_p = os.path.join(similar_dir, f)
                img = preprocess_image_cv2(img_p)
                h = wavelet_hash(img)
                dist, _ = hamming_distance(target_hash, h)
                score = 1.0 - (dist / 64.0)
                pred = 1 if dist <= hamming_threshold else 0
                
                y_true.append(1)
                y_scores.append(score)
                y_preds.append(pred)

    # Thêm cặp memetest.jpg (tương đồng)
    memetest_path = os.path.join(input_dir, "memetest.jpg")
    if os.path.exists(memetest_path):
        img_m = preprocess_image_cv2(memetest_path)
        h_m = wavelet_hash(img_m)
        dist_m, _ = hamming_distance(target_hash, h_m)
        score_m = 1.0 - (dist_m / 64.0)
        pred_m = 1 if dist_m <= hamming_threshold else 0
        y_true.append(1)
        y_scores.append(score_m)
        y_preds.append(pred_m)

    # Tập Cặp Ảnh KHÁC BIỆT (Negative Pairs)
    diff_images = []
    if os.path.exists(different_dir):
        for f in os.listdir(different_dir):
            if f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                img_p = os.path.join(different_dir, f)
                img = preprocess_image_cv2(img_p)
                h = wavelet_hash(img)
                diff_images.append(h)
                
                dist, _ = hamming_distance(target_hash, h)
                score = 1.0 - (dist / 64.0)
                pred = 1 if dist <= hamming_threshold else 0
                
                y_true.append(0)
                y_scores.append(score)
                y_preds.append(pred)

    # Thêm các cặp so sánh giữa các ảnh khác biệt với nhau để làm phong phú dữ liệu âm tính
    for i in range(len(diff_images)):
        for j in range(i + 1, len(diff_images)):
            dist_ij, _ = hamming_distance(diff_images[i], diff_images[j])
            score_ij = 1.0 - (dist_ij / 64.0)
            pred_ij = 1 if dist_ij <= hamming_threshold else 0
            y_true.append(0)
            y_scores.append(score_ij)
            y_preds.append(pred_ij)

    y_true = np.array(y_true)
    y_scores = np.array(y_scores)
    y_preds = np.array(y_preds)

    # 2. Tính Ma trận Nhầm lẫn & Chỉ số đánh giá
    cm = confusion_matrix(y_true, y_preds)
    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()
    else:
        tn = cm[0, 0] if len(cm) > 0 else 0
        fp, fn, tp = 0, 0, 0

    total = len(y_true)
    accuracy = (tp + tn) / total if total > 0 else 0.0
    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0.0

    print(f"Tổng số cặp ảnh thực nghiệm : {total} cặp ({np.sum(y_true==1)} Tương đồng, {np.sum(y_true==0)} Khác biệt)")
    print(f"Ngưỡng khoảng cách Hamming : <= {hamming_threshold} bits (Similarity Score >= {(1.0 - hamming_threshold/64.0)*100:.2f}%)")
    print("-" * 50)
    print("MA TRẬN NHẦM LẪN (CONFUSION MATRIX):")
    print(f"  True Positive  (TP) : {tp:<4} | False Positive (FP) : {fp:<4}")
    print(f"  False Negative (FN) : {fn:<4} | True Negative  (TN) : {tn:<4}")
    print("-" * 50)
    print(f"1. Độ chính xác (Accuracy)    : {accuracy * 100:.2f}%  ((TP + TN) / Tổng số)")
    print(f"2. Độ nhạy (Sensitivity/Recall): {sensitivity * 100:.2f}%  (TP / (TP + FN))")
    print(f"3. Độ đặc hiệu (Specificity)  : {specificity * 100:.2f}%  (TN / (TN + FP))")

    # 3. Tính toán đường cong ROC và diện tích AUC bằng sklearn.metrics
    fpr, tpr, thresholds = roc_curve(y_true, y_scores)
    roc_auc = auc(fpr, tpr)
    print(f"4. Diện tích dưới đường ROC (AUC): {roc_auc:.4f}")

    # 4. Vẽ đường cong ROC bằng matplotlib
    plt.figure(figsize=(8, 6))
    plt.plot(fpr, tpr, color='darkorange', lw=2.5, label=f'Đường cong ROC (AUC = {roc_auc:.4f})')
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label='Phân loại ngẫu nhiên (AUC = 0.5)')
    
    plt.xlim([-0.02, 1.02])
    plt.ylim([-0.02, 1.05])
    plt.xlabel('False Positive Rate (1 - Specificity)', fontsize=11, fontweight='bold')
    plt.ylabel('True Positive Rate (Sensitivity / Recall)', fontsize=11, fontweight='bold')
    plt.title('ĐƯỜNG CONG ROC VÀ ĐÁNH GIÁ HIỆU SUẤT WAVELET HASH (wHash)', fontsize=12, fontweight='bold')
    plt.legend(loc="lower right", fontsize=11)
    plt.grid(True, linestyle=':', alpha=0.6)

    output_dir = os.path.join(BASE_DIR, "data", "output")
    os.makedirs(output_dir, exist_ok=True)
    roc_out_file = os.path.join(output_dir, "roc_curve_evaluation.png")
    plt.savefig(roc_out_file, dpi=150)
    print(f"[+] Đã xuất biểu đồ đường cong ROC thành công tại: {roc_out_file}")
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

# ==========================================================================
    # [4] PHẦN THÊM MỚI: MỞ RỘNG ĐỦ 3 CẶP ẢNH ĐỂ LẤY SỐ LIỆU CHO BÁO CÁO
    # ==========================================================================
    print("\n" + "=" * 70)
    print("[4] BẢNG TỔNG HỢP KẾT QUẢ THỰC NGHIỆM ĐỦ 3 CẶP ẢNH:")
    print("=" * 70)


    # 1. Tạo Cặp 2: Biến thể bị làm mờ Gaussian và thêm nhiễu hạt từ ảnh gốc
    img_blurred = cv2.GaussianBlur(gray_cv2_1, (7, 7), 1.5)
    noise = np.random.normal(0, 10, gray_cv2_1.shape).astype(np.uint8)
    img_noisy = cv2.add(img_blurred, noise)
    hash_noisy = wavelet_hash(img_noisy, wavelet='haar', level=3, hash_size=8)


    # 2. Tạo Cặp 3: Ảnh đối chứng hoàn toàn khác (sử dụng mẫu gradient nhân tạo)
    img_different = np.tile(np.linspace(0, 255, 256, dtype=np.uint8), (256, 1))
    hash_diff = wavelet_hash(img_different, wavelet='haar', level=3, hash_size=8)


    # 3. Tính khoảng cách Hamming cho 2 cặp mở rộng
    dist_pair2, sim_pair2 = hamming_distance(hash1_cv, hash_noisy)
    dist_pair3, sim_pair3 = hamming_distance(hash1_cv, hash_diff)


    # 4. Đánh giá theo ngưỡng <= 10 bits
    eval_pair1 = "TƯƠNG ĐỒNG (Match)" if dist_cv <= 10 else "KHÁC NHAU (Mismatch)"
    eval_pair2 = "TƯƠNG ĐỒNG (Match)" if dist_pair2 <= 10 else "KHÁC NHAU (Mismatch)"
    eval_pair3 = "TƯƠNG ĐỒNG (Match)" if dist_pair3 <= 10 else "KHÁC NHAU (Mismatch)"


    # 5. In bảng tổng hợp số liệu
    print(f"\n| {'Phép thử':<36} | {'Hamming':<10} | {'Tương đồng':<12} | {'Đánh giá'}")
    print("| " + "-" * 36 + " | " + "-" * 10 + " | " + "-" * 12 + " | " + "-" * 22)
    print(f"| {'Cặp 1: Gốc vs memetest.jpg':<36} | {dist_cv:>2}/64 bit | {sim_cv:>6.2f}%     | {eval_pair1}")
    print(f"| {'Cặp 2: Gốc vs Làm mờ + Nhiễu':<36} | {dist_pair2:>2}/64 bit | {sim_pair2:>6.2f}%     | {eval_pair2}")
    print(f"| {'Cặp 3: Gốc vs Ảnh khác loại':<36} | {dist_pair3:>2}/64 bit | {sim_pair3:>6.2f}%     | {eval_pair3}")

    # ==========================================================================
    # [5] PHẦN II.5 (THÀNH VIÊN 3: DUY) - ĐÁNH GIÁ CÁC CHỈ SỐ & VẼ ĐƯỜNG CONG ROC
    # ==========================================================================
    evaluate_performance_and_roc()


