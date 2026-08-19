import cv2
import numpy as np
import matplotlib.pyplot as plt

# 1. Doc anh va tien xu ly
img = cv2.imread('anh1.jpg') 
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 0)

# Trich xuat canh bang Canny
canny_edges = cv2.Canny(blurred, 50, 150)

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
circles = cv2.HoughCircles(blurred, cv2.HOUGH_GRADIENT, dp=1, minDist=50, param1=150, param2=30, minRadius=20, maxRadius=100)
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
