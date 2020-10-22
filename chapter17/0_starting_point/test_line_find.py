import cv2
import numpy as np
from matplotlib import pyplot as plt

image = cv2.imread("carpet_line1 2.jpg")
assert image is not None, "Unable to read file"

resized = cv2.resize(image, (320, 240))

gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
blur = cv2.blur(gray, (5, 80))
row = blur[180].astype(np.int32)
diff = np.diff(row)

max_d = np.amax(diff, 0)
min_d = np.amin(diff, 0)

highest = np.where(diff == max_d)[0][0]
lowest = np.where(diff == min_d)[0][0]
middle = (highest + lowest) // 2

x = np.arange(len(diff))
plt.plot(x, diff)
plt.plot([lowest, lowest], [max_d, min_d], "g--")
plt.plot([middle, middle], [max_d, min_d], "r-")
plt.plot([highest, highest], [max_d, min_d], "g--")
plt.savefig("carpet_line1_2_blur580.png")
