from PIL import Image, ImageDraw

# creating image object which is of specific color
im = Image.new(mode="RGB", size=(300, 200),
                   color=(153, 153, 255))

# this will show image in any image viewer
im.show()