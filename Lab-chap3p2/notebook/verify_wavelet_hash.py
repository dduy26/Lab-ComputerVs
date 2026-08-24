# -*- coding: utf-8 -*-
"""
Kiểm chứng Trích xuất Wavelet 2D (Phần II.2 — Thành viên 1: Thông)

Chạy thật để thu số liệu so sánh 3 wavelet (haar, db4, sym2):
  - Trên cặp ảnh "giống nhau" (meme.jpg vs biến thể xoay)  -> kỳ vọng Hamming NHỎ (giống)
  - Trên cặp ảnh "khác nhau" (meme.jpg vs memetest.jpg)    -> kỳ vọng Hamming LỚN (khác)

Chứng minh lý thuyết:
  - Băng tần LL giữ cấu trúc, bền vững với nhiễu/biến đổi nhẹ.
  - Wavelet khác nhau (haar/db4/sym2) cho hash và độ chính xác khác nhau.

Cách chạy:
    python notebook/verify_wavelet_hash.py
"""
import os
import cv2
import numpy as np
import pywt

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(BASE_DIR, "data", "input")


def read_gray(path, size=(256, 256)):
    """Đọc ảnh xám chuẩn 256x256 (hỗ trợ tên file tiếng Việt)."""
    data = np.fromfile(path, dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)
    return cv2.resize(img, size, interpolation=cv2.INTER_AREA)


def wavelet_hash(img, wavelet="haar", level=3, hash_size=8):
    """2D-DWT -> lấy LL -> resize 8x8 -> lượng tử hóa theo median -> chuỗi bit 64."""
    coeffs = pywt.wavedec2(img, wavelet=wavelet, level=level)
    ll = coeffs[0]
    ll_small = cv2.resize(ll, (hash_size, hash_size), interpolation=cv2.INTER_AREA)
    med = np.median(ll_small)
    return (ll_small >= med).astype(np.uint8).flatten()


def hamming(h1, h2):
    return int(np.count_nonzero(h1 != h2))


def main():
    # Ảnh gốc + các biến thể (giống nhau) + toàn bộ ảnh khác hẳn trong different/
    meme = read_gray(os.path.join(INPUT_DIR, "meme.jpg"))
    rot5 = read_gray(os.path.join(INPUT_DIR, "similar", "similar_meme_rot5.png"))
    blur = read_gray(os.path.join(INPUT_DIR, "similar", "similar_meme_blur.png"))

    diff_dir = os.path.join(INPUT_DIR, "different")
    diff_files = sorted(f for f in os.listdir(diff_dir)
                        if f.lower().endswith((".jpg", ".png", ".webp")))

    wavelets = ["haar", "db4", "sym2"]

    print("=" * 78)
    print("SO SANH 3 WAVELET TREN CAP ANH (Phan II.2)")
    print("=" * 78)

    for w in wavelets:
        h_meme = wavelet_hash(meme, w)
        h_rot5 = wavelet_hash(rot5, w)
        h_blur = wavelet_hash(blur, w)

        d_sim_rot = hamming(h_meme, h_rot5)
        d_sim_blur = hamming(h_meme, h_blur)

        sim_rot = (1 - d_sim_rot / 64) * 100
        sim_blur = (1 - d_sim_blur / 64) * 100

        print(f"\n[Wavelet: {w}]")
        print(f"  meme vs rot5    : Hamming={d_sim_rot:2d}/64 | Similarity={sim_rot:5.2f}%  (ky vong GIONG -> nho)")
        print(f"  meme vs blur    : Hamming={d_sim_blur:2d}/64 | Similarity={sim_blur:5.2f}%  (ky vong GIONG -> nho)")

        # So sánh meme với từng ảnh "khác hẳn"
        for f in diff_files:
            other = read_gray(os.path.join(diff_dir, f))
            d_diff = hamming(h_meme, wavelet_hash(other, w))
            sim_diff = (1 - d_diff / 64) * 100
            print(f"  meme vs {f:<32}: Hamming={d_diff:2d}/64 | Similarity={sim_diff:5.2f}%  (ky vong KHAC -> lon)")

    # Phân tích kích thước các băng tần sau DWT level 3
    print("\n" + "=" * 78)
    print("KICH THUOC CAC BANG TAN SAU pywt.wavedec2(level=3, haar)")
    print("=" * 78)
    coeffs = pywt.wavedec2(meme, "haar", level=3)
    print(f"  LL (xap xi)      : {coeffs[0].shape}")
    for i, detail in enumerate(coeffs[1:], start=1):
        print(f"  Level {3-i+1} chi tiet (LH/HL/HH): {detail[0].shape} / {detail[1].shape} / {detail[2].shape}")

    print("\n[DONE]")


if __name__ == "__main__":
    main()
