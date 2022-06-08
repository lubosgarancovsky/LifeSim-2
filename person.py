import random
import math
import pygame

from hud import PersonHUD

class Person:
    def __init__(self, settings, mother = None, father = None, gender = None):

        self.isDead = False
        self.isChild = True

        self.settings = settings

        # Position and appearance
        if mother == None and father == None:
            self.pos_x, self.pos_y = self.randomPos(settings)
            self.gender = gender

            # Genes
            self.hunger_gene = random.random()
            self.thirst_gene = random.random()
            self.mating_gene = random.random()
            self.viewrange = random.randint(40, 120)
            self.speed = random.random() + 0.2
            self.attractivity = random.random()
            self.maxAge = random.randint(50, 100)
            self.health = random.random()
        else:
            self.pos_x = mother.pos_x
            self.pos_y = mother.pos_y
            self.gender = random.choice(('M','F'))
            self.hunger_gene = random.choice((mother.hunger_gene, father.hunger_gene))
            
            self.thirst_gene = random.choice((mother.thirst_gene, father.thirst_gene))
            self.mating_gene = random.choice((mother.mating_gene, father.mating_gene))
            self.viewrange = random.choice((mother.viewrange, father.viewrange))
            self.speed = random.choice((mother.speed, father.speed))
            self.attractivity = random.choice((mother.attractivity, father.attractivity))
            self.maxAge = random.choice((mother.maxAge, father.maxAge))
            self.health = random.choice((mother.health, father.health))


        self.age = 0
        self.birth = pygame.time.get_ticks()
        self.size = self.settings.cell_size[0] / 4 
        self.color = (self.attractivity* 255, 0, 0) if self.gender == 'F' else (self.attractivity * 255, self.attractivity * 255, 255)

        #Needs 0 - 100
        self.hunger = 0
        self.thirst = 0
        self.mating_urge = 0


        # Other
        self.HUD = PersonHUD()
        self.dest_x = random.randint(-self.viewrange, self.viewrange) + self.pos_x
        self.dest_y = random.randint(-self.viewrange, self.viewrange) + self.pos_y
        self.status = "Wandering"

        self.started_waiting = -2000


        self.food_item = None
        self.water_item = None
        self.mate = None

        self.mating_condition = random.random()

        # Pregnancy
        self.awaited_children = []
        self.got_pregnant = 0
        self.isPregnant = False
        self.child_father = None
        self.fertility = random.random()

        # Health
        self.sick = False
        self.sickness = 0
        self.got_sick = pygame.time.get_ticks()

    def randomPos(self, settings):
        cell = random.choice(settings.GROUND)
        return (cell.pos_x + cell.width/2, cell.pos_y + cell.height/2)

    def getSick(self, chance):
        now = pygame.time.get_ticks()
        if  now - self.got_sick > 15000:
            if random.random() > chance:
                self.sick = True
                self.got_sick = now

    def handleNeeds(self):
        if self.hunger > 100:
            self.hunger = 100
            self.isDead = True

        if self.thirst > 100:
            self.thirst = 100
            self.isDead = True

        if self.mating_urge > 100:
            self.mating_urge = 100

        self.hunger += self.hunger_gene / 5
        self.thirst += self.thirst_gene / 5

        if self.sick:
            self.sickness += 0.07

            

            if pygame.time.get_ticks() % 3000 > 2980:
                chance_to_heal = random.random()

                if chance_to_heal > 1 - (self.health / 10):
                    self.sick = False
                    self.sickness = 0

        

        if self.sickness > 100:
            self.sickness = 100
            self.isDead = True

        if not self.isChild:
            self.mating_urge += (0.5 - (self.mating_gene * (self.age/200)))**2

        if self.age >= 15 and self.isChild:
            self.isChild = False
            self.size = self.settings.cell_size[0] / 3

        if self.age > self.maxAge:
            self.isDead = True

        self.age = (pygame.time.get_ticks() - self.birth) / 3000

    def handleWalk(self, settings):
        distance = int(math.hypot(self.pos_x - self.dest_x, self.pos_y - self.dest_y)) / self.speed
        radians = math.atan2(self.dest_y - self.pos_y, self.dest_x - self.pos_x)

        dx = math.cos(radians) * self.speed
        dy = math.sin(radians) * self.speed


        if distance and not self.waterCheck():
            self.pos_x += dx
            self.pos_y += dy
        else:
            if self.food_item == None and self.water_item == None and self.mate == None:
                self.randomDestination(settings)


    # Sets destination to point within persons viewrange
    def randomDestination(self, settings):
        x = random.randint(-self.viewrange, self.viewrange)
        y = random.randint(-self.viewrange, self.viewrange)


        if self.pos_x + x > 0 and self.pos_y + y > 0:
            if self.pos_x + x < settings.WIDTH and self.pos_y + y < settings.HEIGHT:
                self.dest_x = self.pos_x + x
                self.dest_y = self.pos_y + y
        
    def waterCheck(self):
        if not self.status == "Going to drink":
            for cell in self.settings.WATER:
                if cell.tile.collidepoint(self.dest_x, self.dest_y):
                    return True
        return False

    def findFood(self, food):
        if self.food_item == None and self.hunger > 40:
            closest_food = food[0]
            min_distance = 5000
            for item in food:
                if not item.isEaten:
                    distance = int(math.hypot(self.pos_x - item.pos_x, self.pos_y - item.pos_y))

                    if distance < min_distance:
                        min_distance = distance
                        closest_food = item


                if min_distance <= self.viewrange + self.size:
                    self.food_item = closest_food
                    return


    def goEat(self):
        if not self.food_item == None:
            self.dest_x = self.food_item.pos_x
            self.dest_y = self.food_item.pos_y

            distance = int(math.hypot(self.pos_x - self.food_item.pos_x, self.pos_y - self.food_item.pos_y))

            self.status = "Going to eat"


            if distance <= 1:
                self.wait()
                self.food_item.getEaten()
                self.hunger = 0
                self.randomDestination(self.settings)
                self.food_item = None
                self.status = "Wandering"

                self.getSick(0.997)

    def findWater(self, water):
        if self.water_item == None and self.thirst > 40:
            min_distance = 2000
            closest = water[0]
            for item in water:
                distance = int(math.hypot(self.pos_x - (item.pos_x + item.width / 2), self.pos_y - (item.pos_y + item.height / 2)))

                if distance < min_distance:
                    min_distance = distance
                    closest = item


            if min_distance <= self.viewrange + self.size:
                self.water_item = closest
                return

    def goDrink(self):
        if not self.water_item == None:
            self.dest_x = self.water_item.pos_x + self.water_item.width / 2
            self.dest_y = self.water_item.pos_y + self.water_item.height / 2

            distance = int(math.hypot(self.pos_x - self.dest_x, self.pos_y -  self.dest_y))

            self.status = "Going to drink"


            if distance <= 1:
                self.wait()
                self.thirst = 0
                self.randomDestination(self.settings)
                self.water_item = None
                self.status = "Wandering"

                self.getSick(0.997)

    def handleMating(self, people):
        if self.mate == None:
            for item in people:
                if item.gender != self.gender and item.mate == None:
                    distance = int(math.hypot(self.pos_x - item.pos_x, self.pos_y - item.pos_y))

                    if distance < self.viewrange + self.size:
                        if distance < self.size * 2:
                            if self.sick and not item.sick:
                                item.getSick(0.93)
                        if self.matingCheck(item):
                            self.mate = item
                            item.mate = self
                            return

    def matingCheck(self, item):
        my_index = ((self.mating_urge / 100)**2) / (1 - item.attractivity + 0.1)
        mate_index = ((item.mating_urge / 100) **2) / (1 - self.attractivity + 0.1)
        if my_index >= self.mating_condition and mate_index >= item.mating_condition:
            return True
        return False 

    def goMate(self):
        if not self.mate == None:
            self.dest_x = self.mate.pos_x
            self.dest_y = self.mate.pos_y

            
            distance = int(math.hypot(self.pos_x - self.dest_x, self.pos_y -  self.dest_y))

            if distance <= 1:
                if self.gender == 'F':
                    self.rollPregnancy(self.mate)
                if self.sick:
                    self.mate.getSick(0.2)

                self.wait()
                self.mating_urge = 0
                self.mate = None
                self.randomDestination(self.settings)
                self.status = "Wandering"



    def rollPregnancy(self, father):
        if self.gender == 'F' and not self.isPregnant:
            result = random.random()

            if result < self.fertility:
                self.color = (255, 247, 0)
                self.got_pregnant = pygame.time.get_ticks()
                self.isPregnant = True
                self.child_father = father

    def handlePregnancy(self):
        if self.isPregnant and pygame.time.get_ticks() - self.got_pregnant > 10000:
            self.isPregnant = False
            self.color  = (self.attractivity* 255, 0, 0)

            children_num_chance = random.random()
            num_of_children = 1

            if children_num_chance < 0.8:
                num_of_children = 1

            if children_num_chance >= 0.8 and children_num_chance < 0.95:
                num_of_children = 2

            if children_num_chance >= 0.95:
                num_of_children = 3

            for i in range(0, num_of_children):
                self.awaited_children.append(Person(self.settings, self, self.child_father))

            self.child_father = None

    def wait(self):
        self.started_waiting = pygame.time.get_ticks()