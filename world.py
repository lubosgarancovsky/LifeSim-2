import imp
import numpy as np
import pygame
from perlin_noise import PerlinNoise

# Grid of ground and water tiles
class Grid:
    def __init__(self, width, height, x_count = 64, y_count = 32, waterDensity = -0.1):
        self.COUNT_X = x_count
        self.COUNT_Y = y_count

        self.waterDensity = waterDensity

        # Computes width and height of one grid cell
        self.CELL_W = int(width/self.COUNT_X)
        self.CELL_H = int(height/self.COUNT_Y)


        # Creates perlin noise 
        self.NOISE = PerlinNoise(octaves=5)

        self.GRID = self.makeGrid()

        self.WATER_CELLS = []
        self.GROUND_CELLS = []

        self.fillArrays()
        
    # Creates grid of cells
    # Uses perlin noise to make water and ground
    def makeGrid(self):
        grid = []
        color = (0, 0, 0)

        for y in range(0, self.COUNT_Y):
            for x in range(0, self.COUNT_X):

                noise_val = self.NOISE([x/self.COUNT_X, y/self.COUNT_Y])

                if noise_val < self.waterDensity: 
                    tile = Tile(self.CELL_W, self.CELL_H , self.CELL_W*x, self.CELL_H*y, (0, 0, 255), False)
                else:
                    tile = Tile(self.CELL_W, self.CELL_H , self.CELL_W*x, self.CELL_H*y, (0, 255, 0), True)

                grid.append(tile)

        return grid

    # Draws grid on the screen
    def drawGrid(self, surface):
        for cell in self.GRID:
            pygame.draw.rect(surface, cell.color, cell.tile)

    # Splits grid into array of ground cells and array of water cells
    def fillArrays(self):
        for cell in self.GRID:
            if cell.isGround == True:
                self.GROUND_CELLS.append(cell)
            else:
                self.WATER_CELLS.append(cell)

# Tile in a grid
class Tile:
    def __init__(self, width, height, x, y, color, isGround):
        self.width = width
        self.height = height
        self.pos_x = x
        self.pos_y = y
        (self.center) = (self.pos_x + self.width / 2, self.pos_y + self.height / 2)
        (self.color) = (color)
        self.isGround = isGround
        self.tile = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)