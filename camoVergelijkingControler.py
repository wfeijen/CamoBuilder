import camoVergelijkingsTestScherm as cvs
from projectClasses.fileHandling import give_list_of_images

base_dir = '/mnt/GroteSchijf/machineLearningPictures/camoBuilder'
schenes_sub_dir = 'scenesVoorTest'
camos_sub_dir = 'teVergelijkenCamos'

scenes_lijst = give_list_of_images(baseDir=base_dir, subdirName=schenes_sub_dir)
camos_lijst = give_list_of_images(baseDir=base_dir, subdirName=camos_sub_dir)
camoVergelijkingsTestScherm = cvs.CamoVergelijkingsTestScherm(scenesImageList=scenes_lijst, camoImageList=camos_lijst)