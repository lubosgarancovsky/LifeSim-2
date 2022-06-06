from gettext import find
from person import Person
import pygame


class Population:
    def __init__(self, settings):
        self.men = self.createMen(settings)
        self.women = self.createWomen(settings)
        self.people = self.women + self.men

    # Draws people on the screen
    def drawPeople(self, surface):
        for person in self.people:
            pygame.draw.circle(surface, (person.color), (person.pos_x, person.pos_y), person.size)
            person.HUD.drawHUD(surface, person)

    # Creates instances of men and returns them in array
    def createMen(self, settings):
        men = []
        for i in range(settings.males_num):
            men.append(Person(settings, gender='M'))
        return men

    # Creates instances of women and returns them in array
    def createWomen(self, settings):
        women = []
        for i in range(settings.females_num):
            women.append(Person(settings, gender='F'))
        return women

    # Simulates peoples behavior using methods of each person instance in an array
    def simulateLife(self, surface, settings):
        for person in self.people:
            if pygame.time.get_ticks() - person.started_waiting > 2000:
                person.handleNeeds()
                person.handleWalk(settings)
                person.findFood(settings.FOOD.FOOD_ITEMS)
                person.findWater(settings.WATER)
                person.goEat()
                person.goDrink()
                person.handleMating(self.people)
                person.goMate()
                person.handlePregnancy()
                if person.gender == 'F':
                    for child in person.awaited_children:
                        self.people.append(child)
                    person.awaited_children = []


            
        self.removeDead()
        self.drawPeople(surface);

    # Checks for dead people and removes them from array
    def removeDead(self):
        for person in self.people:
            if person.isDead:
                self.people.remove(person)
