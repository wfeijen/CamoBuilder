import os
from tkinter import ttk, Tk, CENTER, Button, Label, Canvas, BOTTOM
from PIL import ImageTk, Image, UnidentifiedImageError
import random

def rgb_naar_hex(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb

def leerImageEnBereidVoor(img_file, doel_grootte):
    img = Image.open(img_file)
    img = img.resize(doel_grootte, Image.BICUBIC)
    return ImageTk.PhotoImage(img)




class CamoVergelijkingsTestScherm:
    def __init__(self, scenesImageList, camoImageList,
                 scene_grootte=(1920, 1200),
                 camo_grootte=(150, 150)):
        if len(scenesImageList)>0:
            self.index = 0
            self.scenesImageList = scenesImageList
            self.camoImageList = camoImageList
            self.scene_grootte = scene_grootte
            self.camo_grootte = camo_grootte
            self.camo_plaatsingsruimte = tuple(map(lambda i, j: i - j, scene_grootte, camo_grootte))
            self.camo1_file_name = ''
            self.camo2_file_name = ''
            self.root = Tk()
            self.root.geometry('1920x1200')
            try:
                self.root.title("Vergelijken")
                img_scene = leerImageEnBereidVoor(self.scenesImageList[self.index], doel_grootte=self.scene_grootte)
                self.label = ttk.Label(self.root, image=img_scene)
                self.label.place(relx=0.5, rely=0.5, anchor=CENTER)
                # Ophalen van twee camo's
                self.camo1_file_name, self.camo2_file_name = random.sample(self.camoImageList, 2)
                x1, y1, x2, y2 = self.two_random_locations()
                img_camo1 = leerImageEnBereidVoor(self.camo1_file_name, self.camo_grootte)
                self.camo1_label = Label(self.root, image=img_camo1, bd = 0)
                self.camo1_label.place(x=x1, y=y1)
                self.camo1_label.bind('<Button>', self.camo2_click)
                img_camo2 = leerImageEnBereidVoor(self.camo2_file_name, self.camo_grootte)
                self.camo2_label = Label(self.root, image=img_camo2, bd = 0)
                self.camo2_label.place(x=x2, y=y2)
                self.camo2_label.bind('<Button>', self.camo2_click)
                self.afbrekenBtn = Button(self.root, text="AFBREKEN", command=self.afbreken, height=8, width=13)
                self.afbrekenBtn.place(x=self.camo_plaatsingsruimte[0] / 2, y=self.camo_plaatsingsruimte[1] / 2)
            except UnidentifiedImageError as e:
                print("Image niet te openen: ", self.scenesImageList[self.index], " - ", e)

            self.root.bind("<Key>", self.key)
            self.root.mainloop()
        else:
            print("lijst is leeg")


    def wisselScherm(self):
        if self.index < len(self.scenesImageList):
            img_scene = leerImageEnBereidVoor(self.scenesImageList[self.index], doel_grootte=(self.scene_grootte))
            self.label.configure(image=img_scene)
            self.label.image = self.scenesImageList[self.index]
            # Ophalen van twee camo's
            self.camo1_file_name, self.camo2_file_name = random.sample(self.camoImageList, 2)
            x1, y1, x2, y2 = self.two_random_locations()
            img_camo1 = leerImageEnBereidVoor(self.camo1_file_name, self.camo_grootte)
            self.camo1_label.configure(image=img_camo1)
            self.camo1_label.place(x=x1, y=y1)
            self.camo1_label.bind('<Button>', self.camo1_click)
            img_camo2 = leerImageEnBereidVoor(self.camo2_file_name, self.camo_grootte)
            self.camo2_label.configure(image=img_camo2)
            self.camo2_label.place(x=x2, y=y2)
            self.camo2_label.bind('<Button>', self.camo2_click)
        else:
            self.root.title("Alle images verwerkt")
        self.root.mainloop()

    def key(self, event):
        kp = repr(event.keysym)
        print(kp)  # repr(event.char))




    def camo1_click(self, event): #event is argument with info about event that triggered the function
        print('raak1')
        if self.index < len(self.scenesImageList):
            self.index = self.index + 1
            self.wisselScherm()

    def camo2_click(self, event): #event is argument with info about event that triggered the function
        print('raak2')
        if self.index < len(self.scenesImageList):
            self.index = self.index + 1
            self.wisselScherm()

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
        self.root.destroy()