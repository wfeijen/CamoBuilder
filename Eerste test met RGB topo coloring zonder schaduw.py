from PIL import Image, ImageCms
from array import array
import random
import math

w, h = 1920, 1200
N =100

def makeTopoForColor(width, height, N, minImpact, maxImpact, sumTarget):
    topo = [array('f',[0.0 for y in range(height)]) for x in range(width)]
    sum = 0
    for i in range(N):
        print(str(i)+ " "+ str(sum))
        cx = random.randint(0,width)
        cy = random.randint(0,height)
        impact = random.randint(minImpact,maxImpact)
        if sum > sumTarget: impact = -impact
        for ix in range(w):
            for iy in range(h):
                change = impact / (1+ math.sqrt((cx-ix)**2 + (cy-iy)**2))
                topo[ix][iy] = topo[ix][iy] + change
                sum = sum + change

print("R")
R = makeTopoForColor(w, h, N, 100, 1000, 0)
print("G")
G = makeTopoForColor(w, h, N, 100, 1000, 10)
print("B")
B = makeTopoForColor(w, h, N, 500, 1000, 0)

img=Image.new('RGB',(1920,1200),(255,255,255))
pix = img.load()

for ix in range(w):
    for iy in range(h):
        if R[ix][iy] > G[ix][iy]:
            if R[ix][iy] > B[ix][iy]:
                pix[ix, iy]=(255,0,0)
            else:
                pix[ix, iy] = (0, 0, 255)
        else:
            if G[ix][iy] > B[ix][iy]:
                pix[ix, iy] = (0, 255, 0)
            else:
                pix[ix, iy] = (0, 0, 255)

img.save("RGB Topo 1.JPG")