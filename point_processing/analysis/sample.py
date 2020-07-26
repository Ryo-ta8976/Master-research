import cv2
import numpy as np
import math

img = cv2.imread('img/mountain.jpg')

h, w, c = img.shape
print(h, w, c)

mat = cv2.getRotationMatrix2D((w / 2, h / 2), 45, 0.5)
print(mat)

print(img.shape)
affine_img = cv2.warpAffine(img, mat, (w, h))
cv2.imwrite('img/opencv_affine.jpg', affine_img)