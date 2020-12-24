import cv2
import matplotlib.pyplot as plt
import numpy as np

scale = lambda img,divide: cv2.resize(img,((int)(img.shape[1]/divide), (int)(img.shape[0]/divide)))
disc = lambda d: cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (d, d))

def calc_energy(img):
    filter_du = np.array([
        [1.0, 2.0, 1.0],
        [0.0, 0.0, 0.0],
        [-1.0, -2.0, -1.0],
    ])

    filter_dv = np.array([
        [1.0, 0.0, -1.0],
        [2.0, 0.0, -2.0],
        [1.0, 0.0, -1.0],
    ])

    img = img.astype('float32')
    convolved = np.absolute(cv2.filter2D(img,-1,filter_du)) + np.absolute(cv2.filter2D(img,-1,filter_dv))

    energy_map = convolved.sum(axis=2)
    return energy_map

path = 'img2.jpg'

img = cv2.imread(path)
grace = cv2.imread(path, 0)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# edge detect
edge = cv2.Canny(grace, 120, 255)

# sobelx = cv2.Sobel(grace,cv2.CV_64F,1,0,ksize=5)
# sobely = cv2.Sobel(grace,cv2.CV_64F,0,1,ksize=5)
# sobel = np.clip(sobelx+sobely, 0, 255)

# _, thd = cv2.threshold(sobel, 127, 255, cv2.THRESH_BINARY)

# thd = np.where(thd > 200, 255, 0)
# thd = cv2.morphologyEx(thd, cv2.MORPH_CLOSE, disc(10))

gd = calc_energy(img)

_, gd = cv2.threshold(gd, 127, 255, cv2.THRESH_BINARY)
gd = np.uint8(gd)

gd = cv2.morphologyEx(gd, cv2.MORPH_OPEN, disc(5))
_, contours, _ = cv2.findContours(gd, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# cv2.drawContours(img, max(contours, key=cv2.contourArea), -1, (0,255,0), 2)

# cv2.drawContours(img, contours, -1, (0,255,0), 2)

plt.imshow(gd)
plt.show()

# saturation = hsv[...,1]
# mean = np.mean(saturation)
# std = np.sqrt(np.mean(abs(saturation - mean)**2))
# ret, thd = cv2.threshold(saturation, mean+2*std, 255, cv2.THRESH_BINARY)

# mask = cv2.filter2D(edge, -1, disc(20))

# im2, contours, hierarchy = cv2.findContours(edge, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# if len(contours) != 0:
    # c = max(contours, key=cv2.contourArea)
    # plt.imshow(cv2.drawContours(img,c,-1,(255,0,0),2))
    # plt.show()

# ---------------------------------------------------------------------------- #
# ------------------ khoanh vung` láng nhất (ít edge) -> nền ----------------- #
# ---------------------------------------------------------------------------- #
x,y,w,h = cv2.boundingRect(gd)
mask = np.ones(grace.shape, np.uint8) * 255
cv2.rectangle(mask, (x,y),(x+w, y+h), 0, -1)

plt.imshow(mask)
plt.show()

# thống kê phần nền
std = cv2.meanStdDev(hsv, mask=mask)
mask = np.zeros(grace.shape, np.uint8)
select = [std[0] - 6*std[1], std[0] + 6*std[1]]
mask = 255 - cv2.inRange(hsv, select[0], select[1])

mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, disc(10))
mask = cv2.merge((mask,mask,mask))

green = cv2.merge((np.zeros(grace.shape),np.zeros(grace.shape),np.ones(grace.shape)*255))
res = green * ((255 - mask)/255) + img * (mask/255)

# show
cv2.imwrite('result2.jpg', res)
