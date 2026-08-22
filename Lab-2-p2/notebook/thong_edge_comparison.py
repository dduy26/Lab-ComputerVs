import cv2
import numpy as np

SRC = r"E:/ThiGiacMayTinh/Lab-ComputerVs/Lab-2-p2/data/input/meme.jpg"
DST = r"E:/ThiGiacMayTinh/Lab-ComputerVs/Lab-2-p2/data/output/thong_edge_comparison.png"

img = cv2.imread(SRC)
assert img is not None, f"Cannot read {SRC}"
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ---- Edge detectors on the same grayscale image ----
# Sobel: first derivative, magnitude
sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
sobel = cv2.magnitude(sobelx, sobely)
sobel = cv2.convertScaleAbs(sobel)

# Laplacian: second derivative
lap = cv2.Laplacian(gray, cv2.CV_64F)
lap = cv2.convertScaleAbs(lap)

# Canny: multi-stage, binary edge map
canny = cv2.Canny(gray, 100, 200)

# ---- Build labelled 2x2 grid (titles ASCII-only for cv2.putText) ----
panels = [
    (gray, "Original"),
    (sobel, "Sobel"),
    (lap, "Laplacian"),
    (canny, "Canny"),
]

H, W = gray.shape
scale = 900 / H
W2, H2 = int(W * scale), 900
cell = np.zeros((H2 + 40, W2 + 40), dtype=np.uint8)
grid = np.zeros((H2 + 40, W2 + 40), dtype=np.uint8)
grid = cv2.resize(gray, (W2, H2))
grid = cv2.copyMakeBorder(grid, 0, 0, 0, 0, cv2.BORDER_CONSTANT, value=255)

rows = []
for i in range(0, 4, 2):
    row = []
    for j in range(2):
        panel, title = panels[i + j]
        scaled = cv2.resize(panel, (W2, H2))
        cell_img = np.full((H2 + 40, W2 + 40), 255, dtype=np.uint8)
        cell_img[:H2, :W2] = scaled
        cv2.putText(cell_img, title, (10, H2 + 28),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, 0, 2, cv2.LINE_AA)
        row.append(cell_img)
    rows.append(np.hstack(row))

combo = np.vstack(rows)
cv2.imwrite(DST, combo)
print(f"Saved: {DST}")
print(f"Grid size: {combo.shape}")
