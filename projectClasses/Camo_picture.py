from PIL import Image, ImageDraw, ImageCms
import numpy as np
from scipy.spatial import Voronoi, voronoi_plot_2d
from projectClasses.Utilities import replace_with_dict
import random


class CamoPicture:
    def __init__(self, canvas, punt_delta, getal_naar_kleur):
        self.canvas_in = canvas
        self.punt_delta = punt_delta
        self.width, self.height = self.canvas_in.shape
        self.getal_naar_kleur = getal_naar_kleur

    def vul_bolletje(self, canvas, kleur_waarde, x, y):
        ybase = y * 3
        xbase = x * 4
        if (y % 2) == 0:
            xbase = xbase + 2 

        canvas[xbase, ybase + 1] = kleur_waarde
        canvas[xbase, ybase + 2] = kleur_waarde
        canvas[xbase + 1, ybase] = kleur_waarde
        canvas[xbase + 1, ybase + 1] = kleur_waarde
        canvas[xbase + 1, ybase + 2] = kleur_waarde
        canvas[xbase + 1, ybase + 3] = kleur_waarde
        canvas[xbase + 2, ybase] = kleur_waarde
        canvas[xbase + 2, ybase + 1] = kleur_waarde
        canvas[xbase + 2, ybase + 2] = kleur_waarde
        canvas[xbase + 2, ybase + 3] = kleur_waarde
        canvas[xbase + 3, ybase + 1] = kleur_waarde
        canvas[xbase + 3, ybase + 2] = kleur_waarde

    def create_bolletjes(self):
        groot_canvas = np.zeros((self.width * 4 + 2, self.height * 3 + 1))
        for ix in range(self.width):
            for iy in range(self.height):
                self.vul_bolletje(canvas=groot_canvas, kleur_waarde=self.canvas_in[ix, iy], x=ix, y=iy)
        image_array = np.uint8(replace_with_dict(groot_canvas, self.getal_naar_kleur))
        self.img = Image.fromarray(image_array)
        self.info = ",bol"

    def maak_geschaalde_punten(self):

        # pointsDelta = np.random.rand(self.width, self.height, 2)
        geschaalde_points = np.zeros((self.width * self.height, 2))
        for x in range(self.width):
            for y in range(self.height):
                geschaalde_points[x + y * self.width, 0] = max(0, min(self.width - 1,
                                                                      x + (self.randomfactor_X * (random.random() - 0.5) + self.punt_delta[x, y, 0]))) * self.schaal_X
                geschaalde_points[x + y * self.width, 1] = max(0, min(self.height - 1,
                                                                      y + (self.randomfactor_Y * (random.random() - 0.5) + self.punt_delta[x, y, 1]))) * self.schaal_y
        # Hoekjes willen we geen random factor
        geschaalde_points[0, 0] = 0
        geschaalde_points[0, 1] = 0
        geschaalde_points[(self.height - 1) * self.width, 0] = 0
        geschaalde_points[(self.height - 1) * self.width, 1] = self.height - 1
        geschaalde_points[self.width - 1, 0] = self.width - 1
        geschaalde_points[self.width - 1, 1] = 0
        geschaalde_points[self.width - 1 + (self.height - 1) * self.width, 0] = self.width - 1
        geschaalde_points[self.width - 1 + (self.height - 1) * self.width, 1] = self.height - 1
        return geschaalde_points.astype(int)
    
    def generate_voronoi_diagram(self):
        """
        generate voronoi diagramm as polygons
        """
        # make up data points
        geschaalde_points = self.maak_geschaalde_punten()

        # compute Voronoi tesselation
        vor = Voronoi(geschaalde_points)

        points = np.zeros((self.width * self.height, 2)).astype(int)
        for x in range(self.width):
            for y in range(self.height):
                points[x + y * self.width, 0] = x
                points[x + y * self.width, 1] = y

        # plot
        voronoi_plot_2d(vor)

        return vor, points

    def get_color_of_point(self, point):
        x = point[0]
        y = point[1]
        kleurwaarde = self.canvas_in[point[0], point[1]]
        kleur = self.getal_naar_kleur[kleurwaarde]
        return kleur

    def makeup_polygons(self, draw):
        # print("calculating diagramm")
        voronoi, points = self.generate_voronoi_diagram()

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
                rgb = self.get_color_of_point(point)

                # drawing the calculated polygon with the color of the middle point
                if polygon and polygon_tuples:
                    draw.polygon(polygon_tuples, rgb)

    def create_vonoroi(self, schaal_X, schaal_Y, randomfactor_X, randomfactor_Y):
        self.schaal_X = schaal_X
        self.schaal_y = schaal_Y
        self.randomfactor_X = randomfactor_X
        self.randomfactor_Y = randomfactor_Y

        num_cells = self.width * self.height

        self.img = Image.new("RGB", (self.width * self.schaal_X, self.height * self.schaal_y))
        draw = ImageDraw.Draw(self.img)
        self.makeup_polygons(draw)

        self.info = ",vor_sx," + str(self.schaal_X) + ",vor_sy," + str(self.schaal_y) + ",_rx," + str(self.randomfactor_X) + ",_ry," + str(self.randomfactor_Y)

    def show(self):
        self.img.show()

    def save(self, rootDir, name):
        profile = ImageCms.createProfile("sRGB")
        self.img.save(rootDir + name + ".jpg", icc_profile=ImageCms.ImageCmsProfile(profile).tobytes())
# %%
