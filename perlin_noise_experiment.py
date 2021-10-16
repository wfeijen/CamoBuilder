import noise
import numpy as np
from PIL import Image


shape = (2000, 1500)
octaves=7
persistence=0.2
lacunarity=4.0
scalex=400
scaley=200
binaryLevel = 200.0

world = np.zeros(shape)
for i in range(shape[0]):
    for j in range(shape[1]):
        world[i][j] = noise.pnoise2(i / scaley,
                                    j / scalex,
                                    octaves=octaves,
                                    persistence=persistence,
                                    lacunarity=lacunarity,
                                    repeatx=shape[0] / scalex + 1,
                                    repeaty=shape[1] / scaley +1 ,
                                    base=54193)

min = np.amin(world)
factor = 255 / (np.amax(world) - min)
world2 = (world - min) * factor
# world3 = np.where(world2 > binaryLevel, 255, 0)


Image.fromarray(np.uint8(world2)).show()