# -*- coding: utf-8 -*-
"""
Chuẩn hóa ảnh nhóm "different" (Thành viên 1: Thông)

Đổi tên theo quy ước different_<tên>.png và resize về 256x256
để tất cả ảnh trong dataset cùng kích thước với ảnh similar.
"""
import os
import cv2
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIFF_DIR = os.path.join(BASE_DIR, "data", "input", "different")

# ánh xạ: tên hiện tại -> tên chuẩn mới
RENAME = {
    "awww.png":   "different_awww.png",
    "hehehe.jpg": "different_hehehe.jpg",
    "huhu.webp":  "different_huhu.png",
}


def main():
    for old, new in RENAME.items():
        src = os.path.join(DIFF_DIR, old)
        if not os.path.exists(src):
            print(f"[skip] {old} khong ton tai")
            continue

        # đọc ảnh
        data = np.fromfile(src, dtype=np.uint8)
        img = cv2.imdecode(data, cv2.IMREAD_GRAYSCALE)
        if img is None:
            print(f"[LỖI] khong doc duoc {old}")
            continue

        # resize 256x256
        img = cv2.resize(img, (256, 256), interpolation=cv2.INTER_AREA)

        # lưu với tên mới, xóa file cũ
        dst = os.path.join(DIFF_DIR, new)
        ok, buf = cv2.imencode(".png", img)
        if ok:
            buf.tofile(dst)
            if new != old:
                os.remove(src)
        print(f"[OK] {old} -> {new} ({img.shape})")


if __name__ == "__main__":
    main()
