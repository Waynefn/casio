import os
import numpy as np
import matplotlib.pyplot as pyplot
from matplotlib.image import imread
import scipy.misc


def gra2png(filename, output=None):
    filesize = os.path.getsize(filename)
    with open(filename, 'br') as gra:
        gra.read(3)
        height = int.from_bytes(gra.read(1), byteorder='big')
        width = int((filesize - 4) / 2 / height)
        print(f"Size: {height}x{width}")
        rgb = np.zeros((height, width, 3), dtype=int)

        for h in range(height):
            for w in range(width):
                data = int.from_bytes(gra.read(2), byteorder='big')
                rgb[h][w][0] = 8 * ((data & 0b1111100000000000) >> 11)
                rgb[h][w][1] = 8 * ((data & 0b0000011111000000) >> 6)
                rgb[h][w][2] = 8 * ((data & 0b0000000000011111) >> 0)
    pyplot.imshow(rgb, interpolation='nearest')
    pyplot.set_cmap('hot')
    pyplot.axis('off')
    if output != None:
        scipy.misc.imsave(output, rgb)
    pyplot.show()


def gra2png_mono(filename, output=None):
    filesize = os.path.getsize(filename)
    with open(filename, 'br') as gra:
        gra.read(3)
        height = int.from_bytes(gra.read(1), byteorder='big')
        width = int((filesize - 4) * 8 / height)
        print(f"Size: {height}x{width}")
        rgb = np.zeros((height, width), dtype=int)

        for h in range(height):
            for w in range(0, width, 16):
                data = int.from_bytes(gra.read(2), byteorder='big')
                for bit in range(16):
                    rgb[h][w+15-bit] = (data & (1 << bit)) >> bit

    pyplot.imshow(rgb, interpolation='nearest')
    pyplot.set_cmap('hot')
    pyplot.axis('off')
    if output != None:
        scipy.misc.imsave(output, rgb)
    pyplot.show()


def png2gra(filename, output=None):
    png = imread(filename)
    if not output:
        output = filename.split('.')[0]+'.gra'
    gra = open(output, "bw")
    gra.write(b'\x21\xe0\x00\xa4')
    for h in range(164):
        for w in range(480):
            rgb = [0] * 3
            for chnn in range(3):
                rgb[chnn] = int(png[h][w][chnn]*255) // 8
            data = (rgb[0] << 11) + (rgb[1] << 6) + (rgb[2])
            gra.write(int.to_bytes(data, length=2, byteorder="big"))
    gra.close()
    gra2png(output)
