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

def voer_experiment_uit(
        persistence,
        lacunarity,
        octaves,
        scaleX,
        scaleY,
        grenswaarde,
        aantal = 1
):
    base = 2
    max_value_rond = 750
    size = 750
    for i in range(aantal):
        world_vlak = np.zeros((size - i, size - i))
        base = base + 1
        for x in range(size -i):
            for y in range(size -i):
                world_vlak[x][y] = noise.pnoise2(x / scaleX,
                                                 y / scaleY,
                                                 octaves=octaves,
                                                 persistence=persistence,
                                                 lacunarity=lacunarity,
                                                 repeatx=size / scaleX + 1,
                                                 repeaty=size / scaleY + 1,
                                                 base=base)

        world_rond = (world_vlak - np.amin(world_vlak)) / (np.amax(world_vlak) - np.amin(world_vlak))
        print(np.amin(world_vlak), np.amax(world_vlak))
        print(np.amin(world_rond), np.amax(world_rond))
        print('base ', base)

        for x in range(size - i):
            for y in range(size - i):
                midden = (size - i) // 2
                afstand_kwadraad = (((x - midden) / midden) ** 2 + ((y - midden) / midden) ** 2)
                vermenigvuldinging = max(0,
                                         1 - (afstand_kwadraad))
                world_rond[x][y] = vermenigvuldinging * world_rond[x][y]

        world_rond = (world_rond - np.amin(world_rond)) / (np.amax(world_rond) - np.amin(world_rond))

        # show_world(world_vlak, binaryLevel)

        show_world(world_rond, grens=grenswaarde)

def show_world(world, grens):
    min = np.amin(world)
    print(min)
    print(np.amax(world))
    # factor = 255 / (np.amax(world) - min)
    # world_wolk = (world - min) * factor
    # Image.fromarray(np.uint8(world_wolk)).show()
    world_grens = np.where(world > grens, 255, 0)
    Image.fromarray(np.uint8(world_grens)).show()

voer_experiment_uit(
    persistence=0.0,
    lacunarity=1.0,
    octaves=1,
    scaleX=300,
    scaleY=100,
    grenswaarde=0.1,
    aantal = 3
)