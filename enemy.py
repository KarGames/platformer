import pygame
import body

WIDTH, HEIGHT = 1200, 800
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
RED = (255, 0, 0)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
ground_level = screen.get_height()-242


class Enemy(body.Body):
    def __init__(self, health, strength, start_pos, end_pos, width, height, beginning_pos):
        super().__init__(health, strength, start_pos, width, height)
        self.end_pos = end_pos
        self.start_pos = beginning_pos
        self.color = RED
        self.speed = 2
        self.move_right = True
        self.collided = False
        self.died = False

    def move(self):
        if not self.died:
            if self.pos[0] > self.end_pos[0]:
                self.move_right = False
            if self.pos[0] < self.start_pos[0]:
                self.move_right = True
                
            if self.pos[0] <= self.end_pos[0] and self.move_right:
                self.pos[0] += self.speed
            elif self.pos[0] >= self.start_pos[0] and not self.move_right:
                self.pos[0] -= self.speed    
                
            self.collide_left = pygame.Rect(self.pos[0]+50, self.pos[1]+10, 1, 40)
            self.collide_right = pygame.Rect(self.pos[0]-1, self.pos[1]+10, 1, 40)
            self.collide_top = pygame.Rect(self.pos[0]+7, self.pos[1], 35, 1)
        
    def check_collision(self, player):
        if not self.died:
            #check if player kills enemy
            if not self.collided and player.get_rect().colliderect(self.collide_top):
                player.is_jump = True
                player.pos[1] -= 50
                self.died = True
                return
            elif player.finish_level:
                self.died = True
                return
            
            #check if player gets hit 
            if not self.collided and (player.get_rect().colliderect(self.collide_left) or player.get_rect().colliderect(self.collide_right)):
                player.take_damage(33)
        
            if (player.get_rect().colliderect(self.collide_left) or player.get_rect().colliderect(self.collide_right)):
                self.collided = True
            else:
                self.collided = False
            
    def draw(self):
        #draw player onto screen
        if not self.died:
            super().draw()