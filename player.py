import pygame
import body

WIDTH, HEIGHT = 1200, 800
PLAYER_WIDTH, PLAYER_HEIGHT = 50, 50
BLUE = (0, 0, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font_size = 32
font = pygame.font.Font(None, font_size)
ground_level = screen.get_height()-242

class Player(body.Body):
    def __init__(self, health, strength, start_pos, width, height):
        super().__init__(health, strength, start_pos, width, height)
        self.color = BLUE
        self.can_jump = True
        self.is_jump = False
        self.finish_level = False
        self.healed = False
        self.has_key = False
    
    def draw(self):
        #draw player onto screen
        super().draw()
        #draw health bar onto screen
        health_bar_width = 300
        health_bar_height = 50
        pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(20, screen.get_height() - 75, self.health*3, 50))
        pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(20, screen.get_height() - 75, health_bar_width, health_bar_height), 3)
        health_text = font.render(str(self.health), True, (255, 255, 255))
        screen.blit(health_text, (20 + (health_bar_width/2) - (font_size/2), screen.get_height() - 75 + (health_bar_height/2) - (font_size/4)))
       
    #handle left right and jump movement 
    def handle_movement(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_d]:
            self.pos[0] += self.speed
        if pressed[pygame.K_a]:
            self.pos[0] -= self.speed
        if pressed[pygame.K_w] and self.can_jump:
            self.is_jump = True
            self.can_jump = False
        
    #jump action
    def jump(self):
        if self.is_jump and self.jump_count >= 0 and not self.collide_above:
            self.pos[1] -= (self.jump_count * abs(self.jump_count)) * .5
            self.jump_count -= 1
        else:
            self.jump_count = 10
            self.is_jump = False  
            self.collide_above = False
        
    def take_damage(self, damage):
        self.health -= damage
        
        