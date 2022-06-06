import pygame

pygame.font.init()
person_info_font = pygame.font.SysFont("Courier New", 12)


# Draws HUD on top of person 
class PersonHUD:
    hud_width = 40
    def drawHUD(self, surface, person):
        # Background
        background_rect = pygame.Rect(person.pos_x - ( PersonHUD.hud_width / 2), person.pos_y - 21, PersonHUD.hud_width, 8)
        hunger_bar = pygame.Rect(person.pos_x - ( PersonHUD.hud_width / 2), person.pos_y - 21, (person.hunger/100* PersonHUD.hud_width), 2)
        thirst_bar = pygame.Rect(person.pos_x - ( PersonHUD.hud_width / 2), person.pos_y - 19, (person.thirst/100* PersonHUD.hud_width), 2)
        mating_bar = pygame.Rect(person.pos_x - ( PersonHUD.hud_width / 2), person.pos_y - 17, (person.mating_urge/100* PersonHUD.hud_width), 2)
        sickness_bar = pygame.Rect(person.pos_x - ( PersonHUD.hud_width / 2), person.pos_y - 15, (person.sickness/100* PersonHUD.hud_width), 2)

        #pygame.draw.circle(surface, (201, 201, 201), (person.pos_x, person.pos_y), person.viewrange, 1)
        

        pygame.draw.rect(surface, (69, 69, 69) if person.sick == False else (117, 65, 54), background_rect)
        pygame.draw.rect(surface, (247, 189, 62), hunger_bar)
        pygame.draw.rect(surface, (0, 123, 255), thirst_bar)
        pygame.draw.rect(surface, (207, 25, 125), mating_bar)
        pygame.draw.rect(surface, (255, 255, 255), sickness_bar)

        # DESTINATION
        #pygame.draw.circle(surface, (255, 0, 0), (person.dest_x, person.dest_y), 2)

        # STATUS
        status_text = person_info_font.render(f"{person.status} {int(person.age)}", False, (0, 0, 0))
        status_width = status_text.get_width()
        surface.blit(status_text, (person.pos_x - (status_width//2) , person.pos_y + 10))