import math

import noise
import numpy as np
from PIL import Image

# base = 2
# max_value_rond = 10000
# size = 1000
# octaves=8
# persistence=0.6
# lacunarity=6.0
# scalex=200
# scaley=400
# binaryLevel = 0.3

base = 2
max_value_rond = 750
size = 750
octaves = 8
persistence = 0.2
lacunarity = 2.0
scalex = 50
scaley = 100
binaryLevel = 0.3




def show_world(world, grens):
    min = np.amin(world)
    print(min)
    print(np.amax(world))
    # factor = 255 / (np.amax(world) - min)
    # world_wolk = (world - min) * factor
    # Image.fromarray(np.uint8(world_wolk)).show()
    world_grens = np.where(world > grens, 255, 0)
    Image.fromarray(np.uint8(world_grens)).show()


for i in range(100):
    world_vlak = np.zeros((size - i, size - i))
    base = base + 1
    for x in range(size -i):
        for y in range(size -i):
            world_vlak[x][y] = noise.pnoise2(x / scalex,
                                             y / scaley,
                                             octaves=octaves,
                                             persistence=persistence,
                                             lacunarity=lacunarity,
                                             repeatx=size / scalex + 1,
                                             repeaty=size / scaley + 1,
                                             base=base)

    world_rond = (world_vlak - np.amin(world_vlak)) / (np.amax(world_vlak) - np.amin(world_vlak))
    print(np.amin(world_vlak), np.amax(world_vlak))
    print(np.amin(world_rond), np.amax(world_rond))
    print('base ', base)

    for x in range(size - i):
        for y in range(size - i):
            midden = (size - i) // 2
            afstand_kwadraad = ((x - midden) ** 2 + (y - midden) ** 2)
            vermenigvuldinging = max(0,
                                     1 - (afstand_kwadraad / (midden ** 2)))
            world_rond[x][y] = vermenigvuldinging * world_rond[x][y]

    world_rond = (world_rond - np.amin(world_rond)) / (np.amax(world_rond) - np.amin(world_rond))

    # show_world(world_vlak, binaryLevel)

    show_world(world_rond, binaryLevel)
