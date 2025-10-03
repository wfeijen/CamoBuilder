import noise
import numpy as np
from PIL import Image
from sklearn.preprocessing import normalize

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
        scaleY
):
    base = 2
    size = 500
    world_vlak = np.zeros((size - i, size - i))
    for x in range(size - i):
        for y in range(size - i):
            world_vlak[x][y] = noise.snoise2(x / scaleX,
                                             y / scaleY,
                                             octaves=octaves,
                                             persistence=persistence,
                                             lacunarity=lacunarity,
                                             repeatx=size / scaleX + 1,
                                             repeaty=size / scaleY + 1,
                                             base=base)
    world_vlak = normalize(world_vlak)
    world_vlak = np.power(world_vlak, 2)
    world_vlak = (world_vlak - np.amin(world_vlak)) * 255 / (np.amax(world_vlak) - np.amin(world_vlak))
    # world_vlak = np.where(world_vlak > grenswaarde, 255, 0)
    im = Image.fromarray(np.uint8(world_vlak))
    im2 = im.resize((600, 600))
    im2.show()

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
    world_vlak = (world_vlak - np.amin(world_vlak)) * 255 / (np.amax(world_vlak) - np.amin(world_vlak))
    # world_vlak = np.where(world_vlak > grenswaarde, 255, 0)
    im = Image.fromarray(np.uint8(world_vlak))
    im2 = im.resize((600, 600))
    im2.show()


for i in [1]:
    print(i)
    voer_experiment_uit(
        persistence=0,
        lacunarity=1,
        octaves=i,
        scaleX=200,
        scaleY=200
    )
