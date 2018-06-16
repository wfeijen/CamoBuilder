shade = 20
numColors = 10

from PIL import Image
import numpy
from matplotlib import pyplot as plt

def hexencode(rgb):
    r=rgb[0]
    g=rgb[1]
    b=rgb[2]
    return '#%02x%02x%02x' % (r,g,b)

im = Image.open("WIJMF_180128_085454_00133.JPG")
pix = im.load()
w, h = im.size
colors = im.getcolors(w*h)  #Returns a list [(pixel_count, (R, G, B))]
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
        for j in range(i,len(colorsIn)):
            if (colorDistance( currentCol[1],colors[j][1]) >= minColorDistance):
                if  currentCol[0] >= colors[j][0]:
                    count = count + colors[j][0]
                elif  currentCol[0] < colors[j][0]:
                    count = 0
                    break
         if count > 0:
             col = (count , currentCol[1])
             newColors.append(col)


for i in range(1,20):
    colors = votingWithNabors(colors, i*4)
    if len(colors) <10:
        break

for idx, c in enumerate(colors):
    plt.bar(idx, c[0], color=hexencode(c[1]))

plt.show()

if im.mode == '1':
    value = int(shade >= 127) # Black-and-white (1-bit)
elif im.mode == 'L':
    value = shade # Grayscale (Luminosity)
elif im.mode == 'RGB':
    value = (shade, shade, shade)
elif im.mode == 'RGBA':
    value = (shade, shade, shade, 255)
elif im.mode == 'P':
    raise NotImplementedError("TODO: Look up nearest color in palette")
else:
    raise ValueError("Unexpected mode for PNG image: %s" % im.mode)
for x in range(0 , int(im.width/2)):
    for y in range (50, x):
        pic = tuple(numpy.subtract(pix[x, y],value))
        pix[x, y] = pic


im.save("foo_new.png")