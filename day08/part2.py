# usage:
#   python part2.py <image width> <image height> <image file>

import sys

black = 0
white = 1
transparent = 2

class Image:
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

    def output(self, output=sys.stdout):
        characters = {
            black: ' ',
            white: '*',
            transparent: ' ',
        }

        for y in range(self.h):
            for x in range(self.w):
                color = self.image[x][y]
                output.write(characters[color])
            output.write('\n')

if __name__ == "__main__":
    width = int(sys.argv[1])
    height = int(sys.argv[2])
    pixels = width * height

    layers = []
    with open(sys.argv[3]) as input:
        count = 0
        while True:
            layer = input.read(pixels).strip()
            if len(layer) == 0:
                break
            count = count + 1
            layers.append(layer)

    image = Image(width, height)
    for layer in reversed(layers):
        image.render(layer)

    image.output()
