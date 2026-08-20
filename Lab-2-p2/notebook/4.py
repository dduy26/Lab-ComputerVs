import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread("anh1.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# ===== Sigma =====

blur_sigma1 = cv2.GaussianBlur(gray, (5,5), 1)
blur_sigma2 = cv2.GaussianBlur(gray, (5,5), 2)
blur_sigma5 = cv2.GaussianBlur(gray, (5,5), 5)

edge_sigma1 = cv2.Canny(blur_sigma1, 100, 200)
edge_sigma2 = cv2.Canny(blur_sigma2, 100, 200)
edge_sigma5 = cv2.Canny(blur_sigma5, 100, 200)

print("Sigma = 1 :", np.count_nonzero(edge_sigma1))
print("Sigma = 2 :", np.count_nonzero(edge_sigma2))
print("Sigma = 5 :", np.count_nonzero(edge_sigma5))

# ===== Threshold =====

blur = cv2.GaussianBlur(gray, (5,5), 2)

edge_50_150 = cv2.Canny(blur, 50, 150)
edge_100_200 = cv2.Canny(blur, 100, 200)
edge_150_300 = cv2.Canny(blur, 150, 300)

print("50-150 :", np.count_nonzero(edge_50_150))
print("100-200 :", np.count_nonzero(edge_100_200))
print("150-300 :", np.count_nonzero(edge_150_300))
plt.figure(figsize=(10,6))

plt.subplot(2,3,1)
plt.imshow(edge_sigma1, cmap='gray')
plt.title("Sigma=1")

plt.subplot(2,3,2)
plt.imshow(edge_sigma2, cmap='gray')
plt.title("Sigma=2")

plt.subplot(2,3,3)
plt.imshow(edge_sigma5, cmap='gray')
plt.title("Sigma=5")

plt.subplot(2,3,4)
plt.imshow(edge_50_150, cmap='gray')
plt.title("50-150")

plt.subplot(2,3,5)
plt.imshow(edge_100_200, cmap='gray')
plt.title("100-200")

plt.subplot(2,3,6)
plt.imshow(edge_150_300, cmap='gray')
plt.title("150-300")

plt.tight_layout()
plt.show()

# Trich xuat canh bang Canny
canny_edges = cv2.Canny(blur, 50, 150)

# 2. Phan doan vung (Find Contours & Bounding Box)
contours, _ = cv2.findContours(canny_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
img_segmentation = img.copy()

for cnt in contours:
    if cv2.contourArea(cnt) > 50:
        cv2.drawContours(img_segmentation, [cnt], -1, (0, 255, 0), 2)
        x, y, w, h = cv2.boundingRect(cnt)
        cv2.rectangle(img_segmentation, (x, y), (x + w, y + h), (0, 0, 255), 2)

# 3. Nhan dang hinh anh (Hough Transform)
img_hough = img.copy()

# Phat hien duong thang
lines = cv2.HoughLinesP(canny_edges, 1, np.pi/180, threshold=50, minLineLength=40, maxLineGap=10)
if lines is not None:
    for line in lines:
        x1, y1, x2, y2 = line.squeeze()
        cv2.line(img_hough, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2)

# Phat hien duong tron
circles = cv2.HoughCircles(blur, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=150, param2=30, minRadius=20, maxRadius=100)
if circles is not None:
    circles = np.uint16(np.around(circles))
    for i in circles[0, :]:
        cv2.circle(img_hough, (i[0], i[1]), i[2], (0, 0, 255), 2)

# 4. Hien thi ket qua
plt.figure(figsize=(12, 8))

plt.subplot(2, 2, 1)
plt.title("Anh goc")
plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

plt.subplot(2, 2, 2)
plt.title("Canh Canny")
plt.imshow(canny_edges, cmap='gray')

plt.subplot(2, 2, 3)
plt.title("Phan doan (Contour)")
plt.imshow(cv2.cvtColor(img_segmentation, cv2.COLOR_BGR2RGB))

plt.subplot(2, 2, 4)
plt.title("Nhan dang (Hough)")
plt.imshow(cv2.cvtColor(img_hough, cv2.COLOR_BGR2RGB))

plt.tight_layout()
plt.show()
