# usage:
#   python part2.py width height image_file output_image

from PIL import Image

import sys

black = 0
white = 1
transparent = 2

class ImageData:
    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.image = [[transparent for y in range(h)] for x in range(w)]

    def render(self, layer):
        for index, c in enumerate(layer):
            color = int(c)
            x = index % self.w
            y = index / self.w
            if color != transparent:
                self.image[x][y] = color

    def output(self, filename):
        colors = {
            black: (0, 0, 0, 255),
            white: (255, 255, 255, 255),
            transparent: (0, 0, 0, 0),
        }

        scale = 16
        width = self.w * scale
        height = self.h * scale
        im = Image.new('RGBA', (width, height), color=None)
        for y in range(self.h):
            for x in range(self.w):
                for i in range(scale):
                    for j in range(scale):
                        im.putpixel((x*scale+i, y*scale+j), colors[self.image[x][y]])
        im.save(filename)

if __name__ == "__main__":
    width = int(sys.argv[1])
    height = int(sys.argv[2])
    pixels = width * height

    layers = []
    with open(sys.argv[3]) as fh:
        count = 0
        while True:
            layer = fh.read(pixels).strip()
            if len(layer) == 0:
                break
            count = count + 1
            layers.append(layer)

    image = ImageData(width, height)
    for layer in reversed(layers):
        image.render(layer)

    image.output(sys.argv[4])
