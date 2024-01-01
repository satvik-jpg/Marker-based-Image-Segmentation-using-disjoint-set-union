import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2


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
gradient_image = convert_to_gradient_image(
    input_image_path
)  # image obtained on segmentation
cv2.imwrite(
    input_image_path + "_gradient.jpg", gradient_image
)  # saving the image obtained
ndimg = mpimg.imread(input_image_path + "_gradient.jpg").astype(
    int
)  # 2d array of pixels of gradient image
ndimg = ndimg.copy()
# note:astype(int) converts the type of numpy array(returned from .imread) from uint to int
# org_image_with_markers = mpimg.imread("cart.jpg")


org_image_with_markers = mpimg.imread("cart.jpg").copy()
width = len(ndimg[0])
height = len(ndimg)
parent = np.full(
    width * height, -3
)  # creating a parent numpy 2d array with initial value being -3 indicating that the pixel is not yet processed
image = np.full(width * height, 0)
final_gradient_image = np.full(width * height, 0)


print(
    "Enter the number of markers and then enter four integers corresponding to each marker"
)
print(
    "The four numbers represent the two x and y coordinates of the opposite vertices of the rectangular marker"
)
print(
    "The first and third is the y coordinate while the second and the fourth is x coordinate"
)
print(
    "Note that the image on which segmentation is applied will be displayed and you will need it for choosing the markers."
)
print(
    "Till the image is being displayed,the input that you will give to the program wouldn't be displayed, but dont worry your input is being recorded. Hence,keep this in mind while giving the input"
)
print(
    "Once you close the image,your input will be displayed.I am still working on how to take input in a more user-friendly manner,any suggestions are welcome"
)

plt.imshow(org_image_with_markers)
plt.show()
N = int(input())
for i in range(N):
    # temp = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
    # list.append(temp)
    tempy1 = int(input())
    tempx1 = int(input())
    tempy2 = int(input())
    tempx2 = int(input())
    y1 = min(tempy1, tempy2)
    y2 = max(tempy1, tempy2)
    x1 = min(tempx1, tempx2)
    x2 = max(tempx1, tempx2)
    for j in range(x1, x2 + 1):
        ndimg[y1][j] = -1
        ndimg[y2][j] = -1
        org_image_with_markers[y1][i] = [255, 0, 0]
        org_image_with_markers[y2][i] = [255, 0, 0]

    for i in range(y1, y2 + 1):
        ndimg[i][x1] = -1
        ndimg[i][x2] = -1
        org_image_with_markers[i][x1] = [255, 0, 0]
        org_image_with_markers[i][x2] = [255, 0, 0]

dict = {}
for i in range(height):
    for j in range(width):
        if ndimg[i][j] not in dict:
            list = []
            list.append(i * width + j)
            dict[ndimg[i][j]] = list
        else:
            dict[ndimg[i][j]].append(i * width + j)

mykeys = []
for key in dict.keys():
    mykeys.append(key)
mykeys.sort()
i = 0
for key in mykeys:
    for pixel in dict[key]:
        image[i] = pixel
        i = i + 1


def FIND(p):
    if parent[p] >= 0:
        parent[p] = FIND(parent[p])
        return parent[p]
    else:
        return p


def UNION(p, r):
    if parent[p] == -1 and parent[r] == -2:
        parent[p] = -2
    parent[r] = p


def MARKER(p, p1):
    if (
        p1 >= 0 and p1 <= width * height - 1
    ):  # check if the neighbour is a valid neighbour
        if parent[p1] != -3:  # check if its processed or not
            root = FIND(p1)
            if root != p:
                UNION(p, root)


def NON_MARKER(p, p1):
    if (
        p1 >= 0 and p1 <= width * height - 1
    ):  # check if the neighbour is a valid neighbour
        if parent[p1] != -3:  # check if its processed or not
            root = FIND(p1)
            if root != p:
                if parent[root] == -1 or parent[p] == -1:
                    UNION(p, root)


for pixel in image:
    if ndimg[int(pixel / width)][pixel % width] == -1:
        parent[pixel] = -2
        # check all neighbours
        MARKER(pixel, pixel - width - 1)
        MARKER(pixel, pixel - width)
        MARKER(pixel, pixel - width + 1)
        MARKER(pixel, pixel - 1)
        MARKER(pixel, pixel + 1)
        MARKER(pixel, pixel + width - 1)
        MARKER(pixel, pixel + width)
        MARKER(pixel, pixel + width + 1)
    else:
        parent[pixel] = -1
        # check all neighbours
        NON_MARKER(pixel, pixel - width - 1)
        NON_MARKER(pixel, pixel - width)
        NON_MARKER(pixel, pixel - width + 1)
        NON_MARKER(pixel, pixel - 1)
        NON_MARKER(pixel, pixel + 1)
        NON_MARKER(pixel, pixel + width - 1)
        NON_MARKER(pixel, pixel + width)
        NON_MARKER(pixel, pixel + width + 1)

# RESOLVING THE IMAGE
group = 1
for i in range(0, width * height):
    j = width * height - 1 - i
    if parent[image[j]] < 0:
        parent[image[j]] = group
        group = group + 1
    else:
        parent[image[j]] = parent[parent[image[j]]]
# HIGHLIGHTING THE MARKERS
final_segmented_image = plt.imread(input_image_path).copy()


def HIGHLIGHT(p, p1):
    if p1 >= 0 and p1 <= width * height - 1:
        if parent[p] > parent[p1]:
            final_segmented_image[int(p / width)][p % width] = [255, 0, 0]
            final_gradient_image[p] = 255


for pixel in image:
    HIGHLIGHT(pixel, pixel - width - 1)
    HIGHLIGHT(pixel, pixel - width)
    HIGHLIGHT(pixel, pixel - width + 1)
    HIGHLIGHT(pixel, pixel - 1)
    HIGHLIGHT(pixel, pixel + 1)
    HIGHLIGHT(pixel, pixel + width - 1)
    HIGHLIGHT(pixel, pixel + width)
    HIGHLIGHT(pixel, pixel + width + 1)

for i in range(0, height):
    for j in range(0, width):
        ndimg[i][j] = final_gradient_image[i * width + j]
plt.imshow(ndimg)
plt.show()
plt.imshow(final_segmented_image)
plt.show()
