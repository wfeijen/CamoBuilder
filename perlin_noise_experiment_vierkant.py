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
        grenswaarde
):
    base = 2
    size = 200
    world_vlak = np.zeros((size - i, size - i))
    for x in range(size - i):
        for y in range(size - i):
            world_vlak[x][y] = noise.pnoise2(x / scaleX,
                                             y / scaleY,
                                             octaves=octaves,
                                             persistence=persistence,
                                             lacunarity=lacunarity,
                                             repeatx=size / scaleX + 1,
                                             repeaty=size / scaleY + 1,
                                             base=base)
    world_vlak = (world_vlak - np.amin(world_vlak)) / (np.amax(world_vlak) - np.amin(world_vlak))
    world_vlak = np.where(world_vlak > grenswaarde, 255, 0)
    im = Image.fromarray(np.uint8(world_vlak))
    im2 = im.resize((600, 600))
    im2.show()


for i in [2, 4, 8, 16, 32]:
    print(i)
    voer_experiment_uit(
        persistence=0.4,
        lacunarity=0,
        octaves=1,
        scaleX=32,
        scaleY=i,
        grenswaarde=0.5
    )
