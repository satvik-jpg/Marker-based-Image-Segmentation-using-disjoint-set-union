import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import numpy as np


def convert_to_gradient_image(image_path):
    # Read the image
    original_image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply the Sobel operator for gradient computation
    gradient_x = cv2.Sobel(original_image, cv2.CV_64F, 1, 0, ksize=3)
    gradient_y = cv2.Sobel(original_image, cv2.CV_64F, 0, 1, ksize=3)

    # Calculate the magnitude of the gradients
    gradient_magnitude = np.sqrt(gradient_x**2 + gradient_y**2)

    # Normalize the gradient magnitude to the range [0, 255]
    gradient_magnitude = cv2.normalize(
        gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX
    )

    # Convert to uint8 for display
    gradient_image = np.uint8(gradient_magnitude)

    return gradient_image


input_image_path = "cart.jpg"
result_image = convert_to_gradient_image(input_image_path)
cv2.imwrite(input_image_path + "_gradient.jpg", result_image)
img2 = mpimg.imread(input_image_path + "_gradient.jpg")
np.savetxt("data2.txt", img2)
plt.imshow(img2)
plt.show()
