import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import numpy as np

width = 506
height = 900
input_image_path = "mount.jpg"
img = plt.imread(input_image_path).copy()

file_path = "output.txt"
data_array = np.loadtxt(file_path)

for i in range(0, height):
    for j in range(0, width - 1):
        if data_array[i][j] != data_array[i][j + 1]:
            img[i][j] = [255, 0, 0]

plt.imshow(img)
plt.show()
