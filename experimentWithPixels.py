shade = 20
numColors = 10

from PIL import Image, ImageCms
#import skimage
#from colormath.color_objects import XYZColor, sRGBColor,LabColor
#from colormath.color_conversions import convert_color
import numpy
from matplotlib import pyplot as plt

def hexencode(rgb):
    r=rgb[0]
    g=rgb[1]
    b=rgb[2]
    return '#%02x%02x%02x' % (r,g,b)

im = Image.open("WIJMF_180128_085454_00133.JPG")
if im.mode != "RGB":
  im = im.convert("RGB")

srgb_profile = ImageCms.createProfile("sRGB")
lab_profile  = ImageCms.createProfile("LAB")

rgb2lab_transform = ImageCms.buildTransformFromOpenProfiles(srgb_profile, lab_profile, "RGB", "LAB")
lab_im = ImageCms.applyTransform(im, rgb2lab_transform)
w, h = lab_im.size
labColors = lab_im.getcolors(w*h)  #Returns a list [(pixel_count, (R, G, B))]
# now getting the ab only to have only the cromatic component
abColors = {} # we change to dictionaire to make computation easier
for labColor in labColors:
    if (abColors.get((labColor[1][1],labColor[1][2]))) == None:
        abColors[(labColor[1][1],labColor[1][2])] = labColor[0]
    else:
        abColors[(labColor[1][1], labColor[1][2])] = abColors[(labColor[1][1], labColor[1][2])] + labColor[0]
















#pix = im.load()
#pixLab = skimage.color.rgb2lab(pix)


colors = im.getcolors(w*h)  #Returns a list [(pixel_count, (R, G, B))]
CieLabColors = []
for clr in colors:
    clc = []
    clc.append(clr[0])
    x = list(clr[1])
    clc.append(skimage.color.rgb2lab(x))
    CieLabColors.append(clc)
colorsCielab = convert_color(colors,LabColor)

# reduce colors
# voting with nabors until 10 ramain
def colorDistance(colorA, colorB):
    #color is three tuple
    return numpy.linalg.norm(numpy.subtract(colorA, colorB))

def votingWithNabors(colorsIn, minColorDistance):
    newColors = []
    for i in range(len(colorsIn)):
        currentCol = colorsIn[i]
        count =  currentCol[0]
        for j in range(len(colorsIn)):
            if (i != j):
                if (colorDistance( currentCol[1],colors[j][1]) <= minColorDistance):
                    if  currentCol[0] >= colors[j][0]:
                        count = count + colors[j][0]
                    elif  currentCol[0] < colors[j][0]:
                        count = 0
                        break
        if count > 0:
             col = (count , currentCol[1])
             newColors.append(col)
    return newColors


for i in range(4,255):
    colors = votingWithNabors(colors, 2**(i/2))
    if len(colors) <10:
        break

for idx, c in enumerate(colors):
    plt.bar(idx, c[0], color=hexencode(c[1]))

plt.show()