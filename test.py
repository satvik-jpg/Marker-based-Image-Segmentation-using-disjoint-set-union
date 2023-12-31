# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.image as mpimg

# input_image_path = "jour.jpg"
# imgarray = mpimg.imread(input_image_path + "_gradient.jpg").astype(int)
# # note:astype(int) converts the type of numpy array(returned from .imread) from uint to int
# # org_image_with_markers = mpimg.imread("cart.jpg")
# # org_image_with_markers = mpimg.imread("cart.jpg").copy()
# arr = np.empty(1, dtype=np.ndarray)
# arr[0] = np.array([3, 456])
# # arr[1] = np.array([1, 345])
# np.append(arr, np.array([1, 345]))
# # index = np.argsort(arr)
# # arr = arr[index]
# # arr.sort()
# print(arr)


dict = {}
dict[2] = 3
dict[1] = 4
list = []
for key in dict.keys():
    list.append(key)
list.sort()
print(list)
