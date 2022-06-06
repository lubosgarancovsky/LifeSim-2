import pygame
from world import Grid
from food import Food

# Stores settings of display and arrays of food, water and ground cells
class SettingsObject():
    def __init__(self):

        pygame.init()

        # Number of people spawned in the beginning
        self.males_num = 10
        self.females_num = 10

        # Display
        self.FULLSCREEN = True
        self.DISPLAY = pygame.display.Info()
        self.WIDTH = self.DISPLAY.current_w if  self.FULLSCREEN else 600
        self.HEIGHT = self.DISPLAY.current_h if  self.FULLSCREEN else 300
        self.FPS = 60

        # Number of tiles on the screen
        self.x_size = 64
        self.y_size = 32

        # 0 - 1 
        self.food_density = 0.15

        # lower means more water
        # Optimal value between -0.0 to -0.3   -0.08
        self.water_density = -0.08


        # Create World
        self.GRID = Grid(self.WIDTH, self.HEIGHT, x_count=self.x_size, y_count=self.y_size, waterDensity = self.water_density)
        self.FOOD = Food(self.GRID.GROUND_CELLS, self.food_density)
        self.WATER = self.GRID.WATER_CELLS
        self.GROUND = self.GRID.GROUND_CELLS

        self.cell_size = (self.WIDTH / self.x_size, self.HEIGHT / self.y_size)


# Game settings instance
settings = SettingsObject()