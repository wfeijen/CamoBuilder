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
pixLab = lab_im.load()
for x in range(0,im.width//2):
    for y in range(0,im.height):
        (L,A,B)= pixLab[x,y]
        pixLab[x,y]=(int(y*255/im.height),A,B)
lab2rgb_transform = ImageCms.buildTransformFromOpenProfiles(lab_profile, srgb_profile, "LAB", "RGB")
im2 = ImageCms.applyTransform(lab_im,lab2rgb_transform)
im2.save("WIJMF_180128_085454_00133_L128.JPG")

lab_im = ImageCms.applyTransform(im, rgb2lab_transform)
pixLab = lab_im.load()
for x in range(0,im.width//2):
    for y in range(0,im.height):
        (L,A,B)= pixLab[x,y]
        pixLab[x,y]=(L,128,128)
lab2rgb_transform = ImageCms.buildTransformFromOpenProfiles(lab_profile, srgb_profile, "LAB", "RGB")
im2 = ImageCms.applyTransform(lab_im,lab2rgb_transform)
im2.save("WIJMF_180128_085454_00133_AB128.JPG")

lab_im = ImageCms.applyTransform(im, rgb2lab_transform)
pixLab = lab_im.load()
for L in range(0, im.width):
    for A in range(0, 64):
        for B in range(0, 64):
            for Y in range(0, 10):
                pixLab[A+(64*B),L]=(int(L*255/im.width) ,A*8,B*8)
lab2rgb_transform = ImageCms.buildTransformFromOpenProfiles(lab_profile, srgb_profile, "LAB", "RGB")
im2 = ImageCms.applyTransform(lab_im,lab2rgb_transform)
im2.save("WIJMF_180128_085454_00133_Palet.JPG")