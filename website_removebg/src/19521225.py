import cv2
import numpy as np
import matplotlib.pyplot as plt

# Bước 1: Đọc ảnh màu RGB
img = cv2.imread('sample.jpg')

# Bước 2: Covert sang hệ màu HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
value = hsv[:, :, 2]

# Bước 3: Cân bằng histogram cho kênh V --> V*
value_vec = value.reshape(-1)

def cal_hist(img_vec):
    hist = np.zeros(256, np.int)
    values, counts = np.unique(img_vec, return_counts=True)
    for i, val in enumerate(values):
        hist[val] = counts[i]
    return hist

hist = cal_hist(value_vec)
plt.bar(range(0,256), hist)

cdf = np.cumsum(hist)

cdf_min = np.min(cdf)
h = (cdf - cdf_min) / (cdf[-1] - cdf_min) * 255
h = h.astype(np.int)

value_eq = np.copy(value)
for v in range(256):
    value_eq[value==v] = h[v]

value_vec = value_eq.reshape(-1)
hist = cal_hist(value_vec)
plt.bar(range(0,256), hist)

# Bước 4: Ráp lại thành kênh màu HSV*
hsv[:, :, 2] = value_eq
# Bước 5: Convert về RGB
img_result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

# Bước 6: Show hàng
cv2.imshow('Input image', img)
cv2.imshow('Anh da can bang', img_result)
plt.show()
cv2.waitKey(0)
cv2.imwrite('result.jpg',img_result)
cv2.destroyAllWindows()