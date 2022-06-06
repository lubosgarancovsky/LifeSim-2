import pygame

from settingsObject import settings
from population import Population


class Game:
    def __init__(self):
        
        # Stores instance of settings object
        self.settings = settings


        # Sets screen mode 
        if self.settings.FULLSCREEN:
            self.SCREEN = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        else:
            self.SCREEN = pygame.display.set_mode((self.settings.WIDTH, self.settings.HEIGHT))

        pygame.display.set_caption("Life Simulator 2")
        self.CLOCK = pygame.time.Clock()

        # Creates instance of population object, which simulates behavior of people
        self.population = Population(settings)

    
    #Runs main loop
    def run(self):
        run = True
        while run:
            self.CLOCK.tick(self.settings.FPS)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                run = False

            self.settings.GRID.drawGrid(self.SCREEN)
            self.settings.FOOD.drawFood(self.SCREEN)
            self.population.simulateLife(self.SCREEN, self.settings)

            pygame.display.update()