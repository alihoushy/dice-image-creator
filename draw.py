import cv2
import numpy as np
from sys import exit
from die import Die
from random import randint
from sys import argv


def load_image(img, scale=1):
    """Loads an image using OpenCV, converts it to grayscale and scales it.
    Also removes pixels from the bottom left corner so it's multiple of
    die_size

    :param img: Path to the image
    :param scale: Scale in times of the original size
    """
    i = cv2.imread(img)
    ig = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
    return cv2.resize(ig, (int(ig.shape[1] * scale // Die.SIZE * Die.SIZE),
                           int(ig.shape[0] * scale // Die.SIZE * Die.SIZE)))


def dither(img):
    print('Dithering image... (this may take a while)')
    if len(img.shape) != 2:
        raise ValueError('The image is not grayscaled or bad format')

    rows, cols = img.shape

    dithered_image = img.copy()

    for r in range(rows):
        for c in range(cols):
            oldpixel = dithered_image[r, c]
            newpixel = np.round(oldpixel/255) * 255
            dithered_image[r, c] = newpixel
            quant_error = oldpixel - newpixel
            if c + 1 < cols:
                dithered_image[r, c + 1] += quant_error * 7/16
            if r + 1 < rows and c - 1 > 0:
                dithered_image[r + 1, c - 1] += quant_error * 3/16
            if r + 1 < rows:
                dithered_image[r + 1,  c] += quant_error * 5/16
                if c + 1 < cols:
                    dithered_image[r + 1,  c + 1] += quant_error * 1/16

    #import matplotlib.pyplot as plt; plt.imshow(dithered_image); plt.show()

    return dithered_image


def generate_dice(img, roll=False):
    """Generate the dice array from grayscaled image

    :param img: Grayscaled image
    """
    print("Generating dice...")

    if len(img.shape) != 2:
        raise ValueError('The image is not grayscaled or bad format')

    output = []
    # output_index = 0
    dice = []
    height, width = img.shape
    for row in range(0, height, Die.SIZE):
        for col in range(0, width, Die.SIZE):
            if roll:
                steps = randint(5, 50)
            else:
                steps = 0
            reference = img[row:row + Die.SIZE, col:col + Die.SIZE]
            K = 256//5
            reference = reference // K * K
            value, rotation = find_closest_die(reference)

            output.append([value, rotation])

            dice.append(Die(end_value=value, end_rotation=rotation,
                            steps=steps, x=col, y=row))

    return dice


def distance(img1, img2):
    """Calculates the distance between two images. This is used in
    `find_closest_die` in order to find the closest die to the given image.

    :param img1: Image array
    :param img2: Image array
    """

    if img1.shape != img2.shape:
        raise ValueError('Images must be same shape!')

    return 1 - np.mean(img1 == img2)


def find_closest_die(reference):
    """Find the closest die to the given reference

    :param reference: Image array of the same size of the die
    """

    if reference.shape != (Die.SIZE, Die.SIZE):
        raise ValueError('The reference image is not the same size as the die'
                         '(%dx%d px)' % (Die.SIZE, Die.SIZE))

    min_distance = np.inf
    min_die = -1

    for value in [1, 2, 3, 4, 5, 6]:
        for rotation in [0, 90]:
            d = Die(initial_value=value, initial_rotation=rotation)
            current_distance = distance(reference, d.draw(grayscale=True))

            if current_distance < min_distance:
                min_distance = current_distance
                min_die = (d.value, d.rotation)

            # print(d.value, d.rotation, current_distance)

    return min_die


def draw_dice(arr, dice, swapxy=True, roll=False):
    """Writes an array with every dice

    :param arr: Input array
    :param dice: Dice array
    :param swapxy: True if y goes before x
    :param roll: True if every die rolls after drawing
    """

    done = True
    for d in dice:
        if swapxy:
            arr[d.y:d.y + d.SIZE, d.x:d.x + d.SIZE] = d.draw()
        else:
            arr[d.x:d.x + d.SIZE, d.y:d.y + d.SIZE] = np.swapaxes(d.draw(),
                                                                  0, 1)
        if roll:
            if not d.roll():
                done = False

    return done


if __name__ == '__main__':
    import pygame
    import sys

    pygame.init()

    if len(argv) == 2:
        fname = argv[1]
    else:
        fname = 'cat.jpg'

    img = load_image(fname, scale=1.2)
    dithered_img = dither(img)
    width = img.shape[1]
    height = img.shape[0]

    dice = generate_dice(dithered_img, roll=True)

    print("Number of dice: %d" % len(dice))

    screen = pygame.display.set_mode((width, height))
    pygame.mouse.set_visible(0)
    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        screen.fill((255, 255, 255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        arr = pygame.surfarray.pixels3d(screen)

        draw_dice(arr, dice, swapxy=False, roll=True)

        pygame.display.flip()
