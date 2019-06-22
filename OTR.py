import numpy as np
import matplotlib.pyplot as plt
import random
import copy

from scipy.ndimage import gaussian_filter
from skimage import data, io
from skimage import img_as_float
from skimage.morphology import reconstruction
from skimage.color import rgb2gray
from scipy.signal import find_peaks
from skimage.exposure import histogram


def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

# Convert to float: Important for subtraction later which won't work with uint8
image = img_as_float(io.imread("example.png"))
image = gaussian_filter(image, 1)

(height,width, notimportant) = image.shape

dilated = img_as_float(rgb2gray(image))
hist, hist_centers = histogram(dilated)


h = 0.4



fig, (ax0, ax1, ax2) = plt.subplots(nrows=1, ncols=3, figsize=(8, 2.5))

slices = []
completelist = []
verslices = []

for index in range(0, width):
    verslices.append([])
for index in range(0, height):
    slices.append(dilated[index].tolist())
    completelist = completelist + dilated[index].tolist()
    #Vertical slices
    for index2 in range(0, width):
        verslices[index2].append(dilated[index, index2])

sums = [1.0 - (1/height)*sum(x) for x in zip(*slices)]
versums = [1.0 - (1/width)*sum(x) for x in zip(*verslices)]

potcolpeakheight = max(sums)*0.6 if max(sums)*0.6 > 0.10 else 0.10
potrowpeakheight = max(versums)*0.6 if max(versums)*0.6 > 0.10 else 0.10

colunifac = []
rowunifac = []

potcolpeaks, _ = find_peaks(sums, height = potcolpeakheight)
potrowpeaks, _ = find_peaks(versums, height = potrowpeakheight)

potcolpeaks2 = []
potrowpeaks2 = []

for index in range(len(potcolpeaks)):
    potcolpeakspeaks, _ = find_peaks(verslices[potcolpeaks[index]], height = min(verslices[potcolpeaks[index]]) + (max(verslices[potcolpeaks[index]])-min(verslices[potcolpeaks[index]]))*0.5)
    print(potcolpeakspeaks)
    if len(potcolpeakspeaks) == 0:
        potcolpeaks2.append(potcolpeaks[index])
    else:
        pass
print(potcolpeaks2)
potcolpeaks = potcolpeaks2

for index in range(len(potrowpeaks)):
    potrowpeakspeaks, _ = find_peaks(verslices[potrowpeaks[index]], height = min(slices[potrowpeaks[index]]) + (max(slices[potrowpeaks[index]])-min(slices[potrowpeaks[index]]))*0.5)
    if len(potrowpeakspeaks) == 0:
        potrowpeaks.append(potrowpeaks[index])
    else:
        pass
potrowpeaks = potrowpeaks2


for index in range(len(potcolpeaks)):
    colunifac.append(0)
    for index2 in range(height-1):
        colunifac[index] += abs(verslices[potcolpeaks[index]][index2 + 1] - verslices[potcolpeaks[index]][index2])
minimum = min(colunifac) if len(colunifac) != 0 else 0
maximum = max(colunifac) if len(colunifac) != 0 else 0
for index in range(len(colunifac)):
    colunifac[index] = (1.0 - (colunifac[index]-minimum)*(1/maximum))*5

print(colunifac)

for index in range(len(potrowpeaks)):
    rowunifac.append(0)
    for index2 in range(width-1):
        rowunifac[index] += abs(slices[potrowpeaks[index]][index2 + 1] - slices[potrowpeaks[index]][index2])
minimum = min(rowunifac) if len(rowunifac) != 0 else 0
maximum = max(rowunifac) if len(rowunifac) != 0 else 0
for index in range(len(rowunifac)):
    rowunifac[index] = (1.0 - (rowunifac[index]-minimum)*(1/maximum))*5


sums2 = copy.deepcopy(sums)
versums2 = copy.deepcopy(versums)
for index in range(len(potcolpeaks)):
    sums2[potcolpeaks[index]] = sums2[potcolpeaks[index]] * colunifac[index]
for index in range(len(potrowpeaks)):
    versums2[potrowpeaks[index]] = versums2[potrowpeaks[index]] * rowunifac[index]


colpeakheight = max(sums2)*0.4
rowpeakheight = max(versums2)*0.4

colpeaks, _ = find_peaks(sums2, height = colpeakheight)
rowpeaks, _ = find_peaks(versums2, height = rowpeakheight)
colpeaks = intersection(colpeaks, potcolpeaks)
rowpeaks = intersection(rowpeaks, potrowpeaks)
nocolpeaks = list(set(potcolpeaks)-set(colpeaks))
norowpeaks = list(set(potrowpeaks)-set(rowpeaks))

ax0.plot(verslices[colpeaks[0]], color = "black",  label="Som")
temppeaks, _ = find_peaks(verslices[colpeaks[0]], height = min(verslices[colpeaks[0]]) + (max(verslices[colpeaks[0]])-min(verslices[colpeaks[0]]))*0.5 )
for index1 in range(0, len(temppeaks)):
    ax0.plot(temppeaks[index1], verslices[colpeaks[0]][temppeaks[index1]], "x", color = "orange")
ax0.set_ylim(0, 2)
ax0.set_title('Som')
ax0.set_xticks([])
ax0.legend()

ax1.plot(verslices[330], color = "black",  label="Som")
temppeaks, _ = find_peaks(verslices[330], height = min(verslices[330]) + (max(verslices[330])-min(verslices[330]))*0.5 )
for index1 in range(0, len(temppeaks)):
    ax0.plot(temppeaks[index1], verslices[330][temppeaks[index1]], "x", color = "orange")
# for index1 in range(0, len(norowpeaks)):
#     ax1.plot(norowpeaks[index1], versums[norowpeaks[index1]], "x", color = "orange")
ax1.set_ylim(0, 2)
ax1.set_title('Som')
ax1.set_xticks([])
ax1.legend()

ax2.imshow(dilated, vmin=image.min(), vmax=image.max(), cmap='gray')
ax2.set_title('Grayscale')
for index in range(0, len(rowpeaks)):
     ax2.axhline(rowpeaks[index], color="r")
for index1 in range(0, len(colpeaks)):
    ax2.axvline(colpeaks[index1], color="r")
ax2.axis('off')

print("This is a table with Width: " + str(len(colpeaks)-1) + " and Height: " + str(len(rowpeaks)-1))

fig.tight_layout()
plt.show()
