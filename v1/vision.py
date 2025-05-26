import cv2
import numpy as np

# Convert to HSV color space (good for color filtering)
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define range of the color you want to detect (e.g., red)
lower_red = np.array([0, 120, 70])
upper_red = np.array([10, 255, 255])

# Create mask to isolate the color
mask = cv2.inRange(hsv, lower_red, upper_red)

# Bitwise-AND mask and original image to extract the color area
res = cv2.bitwise_and(image, image, mask=mask)

cv2.imshow('Red Areas', res)
cv2.waitKey(0)
cv2.destroyAllWindows()