import cv2
import numpy as np
from draw import load_image, draw_dice, generate_dice, dither
from sys import argv


if __name__ == '__main__':
    if len(argv) == 2:
        fname = argv[1]
    else:
        fname = 'cat.jpg'

    img = load_image(fname, scale=1)
    print('Dithering image... (this may take a while)')
    dithered_img = dither(img)

    width = img.shape[1]
    height = img.shape[0]

    dice = generate_dice(dithered_img)

    img_new = np.zeros((height, width, 3), dtype=np.uint8)

    i = 0
    while not draw_dice(img_new, dice, roll=True):
        cv2.imwrite('dice%04d_' % i + fname, img_new)
        i += 1
