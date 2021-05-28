import sys
import os
import cv2
import numpy as np


filepath = sys.argv[1]

image = cv2.imread(filepath)
gr_image = cv2.imread(filepath, 0)
blured_image = cv2.medianBlur(gr_image, 33)
reflect = cv2.copyMakeBorder(image, 30, 30, 30, 30, cv2.BORDER_REFLECT)
warm_kernel = np.array([0.9, 1, 1.1])
cold_kernel = np.array([1.1, 1, 0.9])
erosion = cv2.erode(image, (5, 5), iterations=4)

filename = os.path.split(filepath)[-1][:-4]
cv2.imwrite(os.path.join("images", f"{filename}_original.png"), image)
cv2.imwrite(os.path.join("images", f"{filename}_reflected.png"), reflect)
cv2.imwrite(os.path.join("images", f"{filename}_warm.png"), image * warm_kernel)
cv2.imwrite(os.path.join("images", f"{filename}_cold.png"), image * cold_kernel)
cv2.imwrite(os.path.join("images", f"{filename}_color_swap.png"), image[:, :, [2, 0, 1]])
cv2.imwrite(os.path.join("images", f"{filename}_erosion.png"), erosion)

try:
    circles = cv2.HoughCircles(blured_image, cv2.HOUGH_GRADIENT, 1, 100, param2=25,
                               minRadius=50, maxRadius=gr_image.shape[1] * 4)
    circles = np.uint16(np.around(circles))
    for circ in circles[0, :]:
        # draw the outer circle
        cv2.circle(image, (circ[0], circ[1]), circ[2], (0, 255, 0), 2)
# If no circles are found
except TypeError:
    pass

cv2.imwrite(os.path.join("images", f"{filename}_circles.png"), image)
