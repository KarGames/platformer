import pygame

WIDTH, HEIGHT = 1200, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
ground_level = screen.get_height()-242
speed = 6

class Body():
    def __init__(self, health, strength, start_pos, width, height):
        self.health = health
        self.stength = strength
        self.color = (0, 0, 0)
        self.jump_count = 10
        self.grav = 0
        self.pos = start_pos
        self.speed = speed
        self.width = width
        self.height = height
        self.ground_level = ground_level
        self.collide_above = False
        self.collide_below = False
    
    def draw(self):
        #draw player
        if self.health > 0:
            pygame.draw.rect(screen, self.color, pygame.Rect(self.pos[0], self.pos[1], self.width, self.height))
               
    def get_rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.width, self.height)
    
    def gravity(self):
        if not self.is_jump and self.pos[1] <= self.ground_level and not self.collide_below:
            check_pos = self.pos[1] + (self.grav**2) * .5
            if check_pos >= self.ground_level:
                self.pos[1] = self.ground_level
                self.collide_below = True
                self.can_jump = True
            else:
                self.pos[1] += (self.grav**2) * .5
                self.grav -= 1
                self.can_jump = False
        else:
            self.grav = 0
            
    def set_ground_level(self, new_level):
        self.ground_level = new_level