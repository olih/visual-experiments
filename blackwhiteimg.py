from PIL import Image
import numpy
resolution = (768, 1024)
drawing = numpy.zeros(resolution, dtype=numpy.uint8)

for x in range(1024):
    for y in range(768):
        if (x % 16) // 8 == (y % 16) // 8:
            drawing[y, x] = 0
        else:
            drawing[y, x] = 255

img = Image.fromarray(drawing, mode='L').convert('1')
img.save('../temp/pil_black.png')

saveImage()
