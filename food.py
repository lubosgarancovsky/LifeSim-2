import pygame
import random


class Food:
    def __init__(self, cellArray, foodDensity):
        self.GROUND_CELLS = cellArray
        self.foodDensity = foodDensity
        self.FOOD_CELLS = self.distributeFood()
        self.FOOD_ITEMS = self.createFood()


    # Decides what cells are going to gave a food inside
    def distributeFood(self):
        arr = []
        for cell in self.GROUND_CELLS:
            value = random.random()
            if value < self.foodDensity:
                arr.append(cell)
        return arr

    # Creates and returns array of Food objects
    def createFood(self):
        items = []
        for cell in self.FOOD_CELLS:
            food_x = cell.pos_x + cell.width / 2
            food_y = cell.pos_y + cell.height / 2
            radius = cell.width/4
            items.append(FoodItem(food_x, food_y, radius))

        return items


    # Draws food objects on the screen using draw method in FoodItem class
    def drawFood(self, surface):
        for item in self.FOOD_ITEMS:
            if not item.isEaten:
                item.drawFoodItem(surface)
            else:
                item.grow()


class FoodItem:
    def __init__(self, x, y, radius):
        self.pos_x = x
        self.pos_y = y
        self.radius = radius
        self.isEaten = False
        self.timeGotEaten = 0

    # Draws itself on the screen
    def drawFoodItem(self, surface):
        pygame.draw.circle(surface, (0, 180, 0), (self.pos_x, self.pos_y), self.radius)

    # Turns food to eaten and gets time of getting eaten
    def getEaten(self):
        self.isEaten = True
        self.timeGotEaten = pygame.time.get_ticks()
    
    # If certain time has passed, it grows food item back
    def grow(self):
        timeNow = pygame.time.get_ticks()
        if timeNow - self.timeGotEaten > 10000:
            self.isEaten = False
