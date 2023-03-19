# van : https://github.com/Stunkymonkey/voronoi-image/blob/master/voronoi-image.py
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
from PIL import Image, ImageDraw
import os
from datetime import datetime
from optparse import OptionParser
import random

img_path = '/media/willem/KleindSSD/machineLearningPictures/camoBuilder/camoOutput/2023-03-18 14:23:22.596954.jpg.jpg' #2023-03-18 14:34:35.572138.jpg.jpg'
schaal = 10
randomFactorX = 1
randomFactorY = 1


# parser = OptionParser()
# parser.add_option("-i", "--image", type="string", dest="imagename",
#                   metavar="FILE", help="Name of Image")
# parser.add_option("-c", "--count", type="string", dest="count",
#                   default=0, help="amount of voronoi-points")
# parser.add_option("-r", "--randomcolor", action="store_true", dest="randomcolor",
#                   default=False, help="random color in picture")
#
# (options, args) = parser.parse_args()
# img_path = options.imagename
# if (img_path is None):
#     print("No image file given")
#     quit()
# num_cells = int(options.count)
# if (num_cells is None):
#     print("No amount of cells given")
#     quit()
# randomcolor = bool(options.randomcolor)

def scale_points(points, width, height):
    """
    scale the points to the size of the image
    """
    scaled_points = []
    for x, y in points:
        x = int(x * width)
        y = int(y * height)
        scaled_points.append([x, y])
    return scaled_points


def generate_voronoi_diagram(num_cells, width, height, vergrotingsfactor, factorX, factorY):
    """
    generate voronoi diagramm as polygons
    """
    # make up data points
    pointsDelta = np.random.rand(width, height, 2)
    geschaalde_points= np.zeros((width * height, 2))
    for x in range(width):
        for y in range(height):
            geschaalde_points[x + y * width, 0] = max(0, min(width - 1, x + factorX * pointsDelta[x, y, 0])) * vergrotingsfactor
            geschaalde_points[x + y * width, 1] = max(0, min(height - 1, y + factorY * pointsDelta[x, y, 1])) * vergrotingsfactor
    # Hoekjes willen we geen random factor
    geschaalde_points[0, 0] = 0
    geschaalde_points[0, 1] = 0
    geschaalde_points[(height - 1) * width, 0] = 0
    geschaalde_points[(height - 1) * width, 1] = height - 1
    geschaalde_points[width - 1, 0] = width - 1
    geschaalde_points[width - 1, 1] = 0
    geschaalde_points[width - 1 + (height - 1) * width, 0] = width - 1
    geschaalde_points[width - 1 + (height - 1) * width, 1] = height - 1

    # compute Voronoi tesselation
    vor = Voronoi(geschaalde_points)

    points= np.zeros((width * height, 2))
    for x in range(width):
        for y in range(height):
            points[x + y * width, 0] = x
            points[x + y * width, 1] = y

    # plot
    voronoi_plot_2d(vor)

    return vor, points


def get_color_of_point(point, rgb_im, width, height):
    """
    get the color of specific point
    """
    x = point[0]
    y = point[1]
    new_point = (x, y)

    try:
        return rgb_im.getpixel(new_point)
    except:
        # unsure if this is needed
        new_point = list(new_point)
        if (new_point[0] == width):
            new_point[0] -= 1
        if (new_point[1] == height):
            new_point[1] -= 1
        new_point = tuple(new_point)
        # print("new point = " + str(new_point) + "\n")
        return rgb_im.getpixel(new_point)


def makeup_polygons(draw, num_cells, width, height, rgb_im):
    """
    makeup and draw polygons
    """
    # print("calculating diagramm")
    voronoi, points = generate_voronoi_diagram(num_cells, width, height, schaal, randomFactorX, randomFactorY)

    for point, index in zip(points, voronoi.point_region):
        # getting the region of the given point
        region = voronoi.regions[index]

        # gettings the points ind arrays
        polygon = list()
        for i in region:
            # if vektor is out of plot do not add
            if i != -1:
                polygon.append(voronoi.vertices[i])
        # Alleen polygoon als er minstens 2 punten zijn
        if len(polygon) > 1:
            # make tuples of the points
            polygon_tuples = list()
            for l in polygon:
                polygon_tuples.append(tuple(l))

            rgb = (0, 0, 0)

            # getting colors of the middle point
            rgb = get_color_of_point(point, rgb_im, width, height)

            # drawing the calculated polygon with the color of the middle point
            if polygon and polygon_tuples:
                draw.polygon(polygon_tuples, rgb)


"""
make image out of the old image
"""

try:
    im = Image.open(img_path).convert('RGB')
except (FileNotFoundError):
    print("Image not found")
    quit()
rgb_im = im.convert('RGB')
width, height = im.size

num_cells = width * height

image = Image.new("RGB", (width * schaal, height * schaal))
draw = ImageDraw.Draw(image)

makeup_polygons(draw, num_cells, width, height, rgb_im)

path, imagename = os.path.split(img_path)
imagename = imagename.replace(".jpg", "")
    # print (imagename)
nieuweImagePad = path + "/" + imagename + "-voronoi" + str(num_cells) + ".jpg"

print(nieuweImagePad)

image.save(nieuweImagePad , "JPEG")
# image.show()