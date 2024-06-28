import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2


class Image_Seg:
    def __init__(self, image_path, marker_list):
        self.image_path = image_path
        self.marker_list = marker_list
        self.width=0
        self.height=0
        self.parent = np.full(
            self.width * self.height, -3
        )  # creating a self.parent numpy 2d array with initial value being -3 indicating that the pixel is not yet processed
        self.image = np.full(self.width * self.height, 0)
        self.final_gradient_image = np.full(self.width * self.height, 0)
        self.final_segmented_image = plt.imread(self.image_path).copy()

    def convert_to_gradient_image(self, image_path):
        # Read the self.image
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

    def UNION(self, p, r):
        if self.parent[p] == -1 and self.parent[r] == -2:
            self.parent[p] = -2
        self.parent[r] = p

    def MARKER(self, p, p1):
        if (
            p1 >= 0 and p1 <= self.width * self.height - 1
        ):  # check if the neighbour is a valid neighbour
            if self.parent[p1] != -3:  # check if its processed or not
                root = self.FIND(p1)
                if root != p:
                    self.UNION(p, root)

    def NON_MARKER(self, p, p1):
        if (
            p1 >= 0 and p1 <= self.width * self.height - 1
        ):  # check if the neighbour is a valid neighbour
            if self.parent[p1] != -3:  # check if its processed or not
                root = self.FIND(p1)
                if root != p:
                    if self.parent[root] == -1 or self.parent[p] == -1:
                        self.UNION(p, root)

    def HIGHLIGHT(self, p, p1):
        if p1 >= 0 and p1 <= self.width * self.height - 1:
            if self.parent[p] > self.parent[p1]:
                i=int(p / self.width)
                j=p % self.width
                self.final_segmented_image[i][j] = [255,0,0]
                self.final_segmented_image[i-1][j-1] = [255,0,0]
                self.final_segmented_image[i-2][j-2] = [255,0,0]

                self.final_gradient_image[p] = 255

    def FIND(self, p):
        if self.parent[p] >= 0:
            self.parent[p] = self.FIND(self.parent[p])
            return self.parent[p]
        else:
            return p

    def seg(self):

        gradient_image = self.convert_to_gradient_image(
            self.image_path
        )  # self.image obtained on segmentation
        cv2.imwrite(
            self.image_path + "_gradient.jpg", gradient_image
        )  # saving the self.image obtained
        ndimg = mpimg.imread(self.image_path + "_gradient.jpg").astype(
            int
        )  # 2d array of pixels of gradient self.image
        ndimg = ndimg.copy()
        # note:astype(int) converts the type of numpy array(returned from .imread) from uint to int
        # org_image_with_markers = mpimg.imread("cart.jpg")

        org_image_with_markers = mpimg.imread(self.image_path).copy()
        self.width = len(ndimg[0])
        self.height = len(ndimg)
        self.parent = np.full(
            self.width * self.height, -3
        )  # creating a self.parent numpy 2d array with initial value being -3 indicating that the pixel is not yet processed
        self.image = np.full(self.width * self.height, 0)
        self.final_gradient_image = np.full(self.width * self.height, 0)


        for marker in self.marker_list:
            # temp = [[x1, y1], [x2, y2], [x3, y3], [x4, y4]]
            # list.append(temp)
            tempy1 = marker[0]
            tempx1 = marker[1]
            tempy2 = marker[2]
            tempx2 = marker[3]
            y1 = min(tempy1, tempy2)
            y2 = max(tempy1, tempy2)
            x1 = min(tempx1, tempx2)
            x2 = max(tempx1, tempx2)
            for j in range(x1, x2 + 1):
                ndimg[y1][j] = -1
                ndimg[y2][j] = -1
                org_image_with_markers[y1][j] = [255, 0, 0]
                org_image_with_markers[y2][j] = [255, 0, 0]

            for i in range(y1, y2 + 1):
                ndimg[i][x1] = -1
                ndimg[i][x2] = -1
                org_image_with_markers[i][x1] = [255, 0, 0]
                org_image_with_markers[i][x2] = [255, 0, 0]

        dict = {}
        for i in range(self.height):
            for j in range(self.width):
                if ndimg[i][j] not in dict:
                    list = []
                    list.append(i * self.width + j)
                    dict[ndimg[i][j]] = list
                else:
                    dict[ndimg[i][j]].append(i * self.width + j)

        mykeys = []
        for key in dict.keys():
            mykeys.append(key)
        mykeys.sort()
        i = 0
        for key in mykeys:
            for pixel in dict[key]:
                self.image[i] = pixel
                i = i + 1

        for pixel in self.image:
            if ndimg[int(pixel / self.width)][pixel % self.width] == -1:
                self.parent[pixel] = -2
                # check all neighbours
                self.MARKER(pixel, pixel - self.width - 1)
                self.MARKER(pixel, pixel - self.width)
                self.MARKER(pixel, pixel - self.width + 1)
                self.MARKER(pixel, pixel - 1)
                self.MARKER(pixel, pixel + 1)
                self.MARKER(pixel, pixel + self.width - 1)
                self.MARKER(pixel, pixel + self.width)
                self.MARKER(pixel, pixel + self.width + 1)
            else:
                self.parent[pixel] = -1
                # check all neighbours
                self.NON_MARKER(pixel, pixel - self.width - 1)
                self.NON_MARKER(pixel, pixel - self.width)
                self.NON_MARKER(pixel, pixel - self.width + 1)
                self.NON_MARKER(pixel, pixel - 1)
                self.NON_MARKER(pixel, pixel + 1)
                self.NON_MARKER(pixel, pixel + self.width - 1)
                self.NON_MARKER(pixel, pixel + self.width)
                self.NON_MARKER(pixel, pixel + self.width + 1)

        # RESOLVING THE IMAGE
        group = 1
        for i in range(0, self.width * self.height):
            j = self.width * self.height - 1 - i
            if self.parent[self.image[j]] < 0:
                self.parent[self.image[j]] = group
                group = group + 1
            else:
                self.parent[self.image[j]] = self.parent[self.parent[self.image[j]]]
        # HIGHLIGHTING THE MARKERS
        self.final_segmented_image = plt.imread(self.image_path).copy()
        for pixel in self.image:
            self.HIGHLIGHT(pixel, pixel - self.width - 1)
            self.HIGHLIGHT(pixel, pixel - self.width)
            self.HIGHLIGHT(pixel, pixel - self.width + 1)
            self.HIGHLIGHT(pixel, pixel - 1)
            self.HIGHLIGHT(pixel, pixel + 1)
            self.HIGHLIGHT(pixel, pixel + self.width - 1)
            self.HIGHLIGHT(pixel, pixel + self.width)
            self.HIGHLIGHT(pixel, pixel + self.width + 1)

        for i in range(0, self.height):
            for j in range(0, self.width):
                ndimg[i][j] = self.final_gradient_image[i * self.width + j]
        # plt.imshow(ndimg)
        # plt.show()
        # plt.imshow(self.final_segmented_image)
        # plt.show()
        return self.final_segmented_image

    # seg function ended here
