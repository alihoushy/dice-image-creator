import cv2
import numpy as np
from draw import load_image, draw_dice, generate_dice, dither
from sys import argv


if __name__ == '__main__':
    if len(argv) == 2:
        fname = argv[1]
    else:
        fname = 'dice_cat.jpg'

    img = load_image(fname, scale=2)
    dithered_img = dither(img)

    width = img.shape[1]
    height = img.shape[0]

    dice = generate_dice(dithered_img)

    img_new = np.zeros((height, width, 3), dtype=np.uint8)
    draw_dice(img_new, dice)

    cv2.imwrite('dice_' + fname, img_new)
