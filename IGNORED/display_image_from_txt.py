import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

file_path = "output.txt"
data_array = np.loadtxt(file_path)

# img = plt.imread(data_array.astype(int))
plt.imshow(data_array)
plt.show()
