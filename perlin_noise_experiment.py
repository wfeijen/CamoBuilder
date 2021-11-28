import math

import noise
import numpy as np
from PIL import Image

base = 2
max_value_rond = 10000
size = 1000
octaves=10
persistence=0.4
lacunarity=4.0
scalex=200
scaley=400
binaryLevel = 0.2

midden = size / 2

def show_world(world, grens):
    min = np.amin(world)
    print(min)
    print(np.amax(world))
    #factor = 255 / (np.amax(world) - min)
    #world_wolk = (world - min) * factor
    # Image.fromarray(np.uint8(world_wolk)).show()
    world_grens = np.where(world > grens, 255, 0)
    Image.fromarray(np.uint8(world_grens)).show()

for i in range(3):
    world_vlak = np.zeros((size, size))
    for x in range(size):
        for y in range(size):
            world_vlak[x][y] = noise.pnoise2(x / scalex,
                                        y / scaley,
                                        octaves=octaves,
                                        persistence=persistence,
                                        lacunarity=lacunarity,
                                        repeatx=size / scalex + 1,
                                        repeaty=size / scaley + 1,
                                        base=base + i)

    world_rond = (world_vlak - np.amin(world_vlak))

    for x in range(size):
        for y in range(size):
            afstand_kwadraad = ((x - midden) ** 2 + (y - midden) ** 2)
            vermenigvuldinging = max(0,
                                     1 - (afstand_kwadraad / (midden ** 2)))
            world_rond[x][y] = vermenigvuldinging * world_rond[x][y]

    #show_world(world_vlak, binaryLevel)

    show_world(world_rond, binaryLevel)

