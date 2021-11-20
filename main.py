#! /usr/bin/env python
import sys
import contextlib
import functools

import pygame
import numpy as np

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def is_alive(cell: int) -> bool:
    return cell == 1


class Game:
    __slots__ = (
        "width",
        "height",
        "ncols", 
        "nrows", 
        "win", 
        "cells", 
        "cell_width", 
        "cell_height",
        "rect_factory",
    )

    def __init__(
        self,
        width: int,
        height: int,
        ncols: int = 100,
        nrows: int = 100,
    ):
        pygame.init()

        self.width = width
        self.height = height
        self.ncols = ncols
        self.nrows = nrows
        self.win = pygame.display.set_mode((width, height))
        self.cells = np.random.choice((0, 1), size=(ncols, nrows), p=(.90, .10))
        self.cell_width = width / ncols
        self.cell_height = height / nrows

        pygame.display.set_caption("Game of life")

    def draw(self):
        self.win.fill(WHITE)

        for (i, j), cell in np.ndenumerate(self.cells):
            if is_alive(cell):
                rect = pygame.Rect(
                    j * self.cell_width,
                    i * self.cell_height,
                    self.cell_width,
                    self.cell_height,
                )
                pygame.draw.rect(self.win, BLACK, rect)

        pygame.display.update()

    def update(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        for (i, j), cell in np.ndenumerate(self.cells):
            nbrs_num = self.count_neighbours(i, j)
            if nbrs_num == 3 and cell == 0:
                self.cells[i, j] = 1
            elif (nbrs_num < 2 or nbrs_num > 3) and cell == 1:
                self.cells[i, j] = 0

    def count_neighbours(self, row_i: int, col_i: int) -> int:
        nbrs_num = 0
        for i in (row_i - 1, row_i, row_i + 1):
            for j in (col_i - 1, col_i, col_i + 1):
                with contextlib.suppress(IndexError):
                    nbrs_num += self.cells[i, j]
        return nbrs_num - self.cells[row_i, col_i]

    def loop(self):

        while True:
            self.draw()
            self.update()

if __name__ == "__main__":
    ncols, nrows = 100, 100
    if len(sys.argv) > 1:
        ncols, nrows = sys.argv[1:]
    game = Game(1000, 800, ncols, nrows)

    game.loop()
