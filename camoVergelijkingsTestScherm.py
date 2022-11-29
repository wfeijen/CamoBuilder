import os
from tkinter import ttk, Tk, CENTER, Button, Label, Canvas, BOTTOM

import pandas as pd
from PIL import ImageTk, Image, UnidentifiedImageError
import random
import numpy as np
from datetime import datetime
from shutil import move


def rgb_naar_hex(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb


def leerImageEnBereidVoor(img_file, doel_grootte):
    img = Image.open(img_file)
    img = img.resize(doel_grootte, Image.BICUBIC)
    return ImageTk.PhotoImage(img)


class CamoVergelijkingsTestScherm:
    def __init__(self, scene_en_camos,
                 boekhouding_file,
                 scene_grootte=(2560, 1390),
                 camo_grootte=(150, 150)):

        self.boekhouding_file = boekhouding_file
        self.label = None
        self.afbrekenBtn = None
        self.camo2_label = None
        self.camo1_label = None
        self.click_tijd1 = None
        self.click_tijd2 = None
        self.click_tijd_start = None
        self.counter = 0
        if scene_en_camos.shape[0] > 0:
            # self.index = 0
            # Opschudden en sorteren van de scenes en camos zodat we straks van boven naar beneden kunnen werken
            scene_en_camos['willekeurig'] = np.random.randint(
                10000000,
                size=scene_en_camos.shape[0])

            scene_en_camos.loc[pd.notna(scene_en_camos['tijd1']) | scene_en_camos['actief'].isnull(), "actief"] = False
            scene_en_camos = scene_en_camos.sort_values(by=['actief', 'willekeurig'], ascending=[False, False],
                                                        na_position='last')
            # Tellen van het aantal actieve (nog te doene vergelijkingen)
            self.aantal_actief = scene_en_camos.actief.sum()
            if self.aantal_actief == 0:
                # Het heeft nu weinig zin om door te gaan
                print("geen nieuwe camo's of scenes ontdekt")
                return True
            self.index = 0
            self.scene_en_camos = scene_en_camos
            self.scene_grootte = scene_grootte
            self.camo_grootte = camo_grootte
            self.camo_plaatsingsruimte = tuple(map(lambda i, j: i - j, scene_grootte, camo_grootte))
            self.camo1_file_name = ''
            self.camo2_file_name = ''
            self.root = Tk()
            self.root.geometry('2560x1440')
            try:
                self.root.title("Vergelijken")
                self.wisselScherm()
            except UnidentifiedImageError as e:
                print("Image niet te openen: ", self.scenesImageList[self.index], " - ", e)

            # self.root.bind("<Key>", self.key)
            self.root.mainloop()
        else:
            print("lijst is leeg")

    def wisselScherm(self):
        if self.index < self.aantal_actief:
            self.click_tijd1 = None
            self.click_tijd2 = None
            self.counter += 1
            if self.counter == 10:
                self.schrijf_boekhouding_weg()
                self.counter = 1
            try:
                img_scene = leerImageEnBereidVoor(self.scene_en_camos.iloc[self.index, 0],
                                                  doel_grootte=self.scene_grootte)
                self.label = ttk.Label(self.root, image=img_scene)
                self.label.place(relx=0.5, rely=0.5, anchor=CENTER)
                # self.label.configure(image=img_scene)
                # self.label.image = self.scenesImageList[self.index]
                self.afbrekenBtn = Button(self.root, text="AFBREKEN", command=self.afbreken, height=8, width=13)
                self.afbrekenBtn.place(x=self.camo_plaatsingsruimte[0] / 2, y=self.camo_plaatsingsruimte[1] / 2)
                # Ophalen van twee camo's
                x1, y1, x2, y2 = self.two_random_locations()
                img_camo1 = leerImageEnBereidVoor(self.scene_en_camos.iloc[self.index, 1], self.camo_grootte)
                self.camo1_label = ttk.Label(self.root, image=img_camo1, relief="flat", borderwidth=0)
                self.camo1_label.place(x=x1, y=y1)
                self.camo1_label.bind('<Button>', self.camo1_click)
                img_camo2 = leerImageEnBereidVoor(self.scene_en_camos.iloc[self.index, 2], self.camo_grootte)
                self.camo2_label = ttk.Label(self.root, image=img_camo2, relief="flat", borderwidth=0)
                self.camo2_label.place(x=x2, y=y2)
                self.camo2_label.bind('<Button>', self.camo2_click)
                self.click_tijd_start = datetime.now()
            except UnidentifiedImageError as e:
                print("Image niet te openen: ", self.scenesImageList[self.index], " - ", e)
        else:
            self.root.title("Alle images verwerkt")
        self.root.mainloop()

    def key(self, event):
        kp = repr(event.keysym)
        print(kp)  # repr(event.char))

    def camo1_click(self, event):  # event is argument with info about event that triggered the function
        if self.click_tijd1 is None:
            self.click_tijd1 = datetime.now() - self.click_tijd_start
            self.camo1_label.place(x=2000, y=2000)
            if self.click_tijd2 is not None:
                self.registreer_score()
                self.index = self.index + 1
                if self.index < self.aantal_actief:
                    self.wisselScherm()
                else:
                    print('We zijn klaar')
                    self.afbreken()

    def camo2_click(self, event):  # event is argument with info about event that triggered the function
        if self.click_tijd2 is None:
            self.click_tijd2 = datetime.now() - self.click_tijd_start
            self.camo2_label.place(x=2000, y=2000)
            if self.click_tijd1 is not None:
                self.registreer_score()
                self.index = self.index + 1
                if self.index < self.aantal_actief:
                    self.wisselScherm()
                else:
                    print('We zijn klaar')
                    self.afbreken()

    def registreer_score(self):
        self.scene_en_camos.iloc[self.index, 3] = self.click_tijd1
        self.scene_en_camos.iloc[self.index, 4] = self.click_tijd2

    def two_random_locations(self):
        if random.randint(0, 2) == 0:
            x1 = random.randint(0, self.camo_plaatsingsruimte[0] // 3)
            y1 = random.randint(0, self.camo_plaatsingsruimte[1])
        else:
            x1 = random.randint(0, self.camo_plaatsingsruimte[0])
            y1 = random.randint(0, self.camo_plaatsingsruimte[1] // 3)
        x2 = self.camo_plaatsingsruimte[0] - x1
        y2 = self.camo_plaatsingsruimte[1] - y1
        return x1, y1, x2, y2

    def afbreken(self):
        self.schrijf_boekhouding_weg()
        self.root.destroy()

    def schrijf_boekhouding_weg(self):
        # Kolommen weggooien
        antwoord = self.scene_en_camos.loc[:, ['scenes', 'camo1', 'camo2', 'tijd1', 'tijd2']]
        # self.boekhouding_file
        move(self.boekhouding_file, self.boekhouding_file + '.back')
        try:
            os.remove(self.boekhouding_file)
        except FileNotFoundError as e:
            print('File was al weg')
        antwoord.to_csv(self.boekhouding_file, index=False)


