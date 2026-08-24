import glob
import time
import cv2
import numpy as np
import pywt


# 1. CAC PHUONG PHAP BAM 
# PP1: Bam theo he so LL
def hash_ll(img):
    gray = (
        cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    )
    LL, _ = pywt.dwt2(gray, "haar")
    ll_sub = cv2.resize(LL, (8, 8))
    med = np.median(ll_sub)
    return (ll_sub > med).astype(int).flatten()

# PP2: Bam theo nang luong chi tiet (LH, HL, HH)
def hash_energy(img):
    gray = (
        cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    )
    _, (LH, HL, HH) = pywt.dwt2(gray, "haar")

    energies = []
    for band in [LH, HL, HH]:
        h, w = band.shape
        bh, bw = max(1, h // 8), max(1, w // 8)
        for i in range(8):
            for j in range(8):
                block = band[i * bh : (i + 1) * bh, j * bw : (j + 1) * bw]
                energies.append(np.sum(block**2))

    energies = np.array(energies)
    med = np.median(energies)
    return (energies > med).astype(int).flatten()

# PP3: Kết hop LL va Chi tiet
def hash_combined(img):
    h1 = hash_ll(img)
    h2 = hash_energy(img)
    # Lay 45 bit dau cua LL va 19 bit cua Energy cho du 64 bit
    return np.concatenate([h1[:45], h2[:19]])

# Tinh khoang cach Hamming
def hamming_dist(h1, h2):
    return np.sum(h1 != h2) / len(h1)

# 2. MAIN CHUYEN CHAY BAI THUCNHANH

# Doc anh tu thu muc data
paths = sorted(glob.glob("data/*.jpg") + glob.glob("data/*.png"))
imgs = [cv2.imread(p) for p in paths if cv2.imread(p) is not None]

if len(imgs) < 2:
    print("Vui long chep it nhat 2-4 file anh (.jpg hoac .png) vao thu muc data!")
else:
    # Tao tap cap anh: Cap giong/tuong tu (label 1) va Cap khac nhau (label 0)
    pairs = []
    for i in range(0, len(imgs) - 1, 2):
        pairs.append((imgs[i], imgs[i + 1], 1))
    for i in range(0, len(imgs) - 2, 2):
        pairs.append((imgs[i], imgs[i + 2], 0))

    methods = {
        "PP1 (LL)": hash_ll,
        "PP2 (Energy)": hash_energy,
        "PP3 (Combined)": hash_combined,
    }

    print(" KET QUA SO SANH CUA BAI THUC HANH ")
    print(
        f"{'Phuong phap':<18} | {'Accuracy':<10} | {'Time (ms)':<10} | {'Do phan biet':<12}"
    )
    print("-" * 60)

    for name, func in methods.items():
        correct = 0
        t_start = time.time()
        diff_dists = []

        for img1, img2, label in pairs:
            h1 = func(img1)
            h2 = func(img2)
            d = hamming_dist(h1, h2)

            # Ngung 0.25: neu dist <= 0.25 la 1 (giong), nguoc lai la 0 (khac)
            pred = 1 if d <= 0.25 else 0
            if pred == label:
                correct += 1

            if label == 0:
                diff_dists.append(d)

        t_total = (time.time() - t_start) * 1000 / (len(pairs) * 2)
        acc = (correct / len(pairs)) * 100
        avg_diff = np.mean(diff_dists) if diff_dists else 0

        print(
            f"{name:<18} | {acc:>8.1f}% | {t_total:>8.3f}ms | {avg_diff:>12.4f}"
        )
      
