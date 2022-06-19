import os

def give_list_of_images(baseDir, subdirName):
    data_set_dir = os.path.join(baseDir, subdirName)
    file_names = [os.path.join(data_set_dir, f) for f in os.listdir(data_set_dir) if os.path.isfile(os.path.join(data_set_dir, f)) and os.path.splitext(f)[1]=='.jpg']
    return file_names