from random import choice
from numpy import zeros, uint8


class Die:
    MARGIN = 1
    DOT = 2
    SIZE = 4*MARGIN + 3*DOT

    def __init__(self, initial_value=1, initial_rotation=0,
                 end_value=6, end_rotation=0, steps=10, x=0, y=0):
        self.value = initial_value
        self.rotation = initial_rotation
        self.end_value = end_value
        self.end_rotation = end_rotation
        self.steps = steps
        self.step = 0
        self.x = x
        self.y = y

        if steps == 0:
            self.value = self.end_value

    def pixels(self):
        """Creates a grid of 9x9 with the dots' positions"""
        if self.value == 1:
            return [[1, 1]]
        elif self.value == 2:
            if self.rotation == 0:
                return [[0, 0], [2, 2]]
            else:
                return [[0, 2], [2, 0]]
        elif self.value == 3:
            if self.rotation == 0:
                return [[0, 0], [1, 1], [2, 2]]
            else:
                return [[0, 2], [1, 1], [2, 0]]
        elif self.value == 4:
            return [[0, 0], [2, 0], [0, 2], [2, 2]]
        elif self.value == 5:
            return [[0, 0], [2, 0], [1, 1], [0, 2], [2, 2]]
        elif self.value == 6:
            if self.rotation == 0:
                return [[0, 0], [1, 0], [2, 0], [0, 2], [1, 2], [2, 2]]
            else:
                return [[0, 0], [0, 1], [0, 2], [2, 0], [2, 1], [2, 2]]

    def draw(self, grayscale=False):
        """Creates a numpy array with the die drawing"""

        if grayscale:
            canvas = zeros((self.SIZE, self.SIZE), dtype=uint8)
        else:
            canvas = zeros((self.SIZE, self.SIZE, 3), dtype=uint8)

        margin = self.MARGIN
        dot = self.DOT
        pixels = self.pixels()

        for px in pixels:
            row = (margin + dot) * px[0] + margin
            col = (margin + dot) * px[1] + margin
            if grayscale:
                canvas[row:row + dot, col:col+dot] = 1
            else:
                canvas[row:row + dot, col:col+dot, :] = 1

        if grayscale:
            canvas[0, :] = 200
            canvas[-1, :] = 200
            canvas[:, 0] = 200
            canvas[:, -1] = 200
        else:
            canvas[0, :, :] = 200
            canvas[-1, :, :] = 200
            canvas[:, 0, :] = 200
            canvas[:, -1, :] = 200
        canvas[canvas == 0] = 255
        canvas[canvas == 1] = 0
        return canvas

    def roll(self):
        """Roll the die. If it reached the final value, returns True"""
        if self.step < self.steps - 1:
            self.value = choice([v for v in range(1, 7) if v != self.value])
            self.rotation = choice([0, 90])
            self.step += 1
            return False
        elif self.step == self.steps - 1:
            self.value = choice([v for v in range(1, 7) if v != self.value
                                 and v != self.end_value])
            self.rotation = choice([0, 90])
            self.step += 1
            return False
        else:
            self.value = self.end_value
            self.rotation = self.end_rotation
            return True


if __name__ == '__main__':
    d = Die(end_value=6)
    print(d.value)
    while(not d.roll()):
        print(d.value)
    print(d.value)
    print(d.draw()[:, :,  0])
    print(d.draw().shape)
