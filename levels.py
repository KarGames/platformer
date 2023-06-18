import pygame
import images

pygame.init()

space = 64
font_size = 64
font = pygame.font.Font(None, font_size)

class Platform():
    def __init__(self, platform_pos, screen, ground_level):
        self.platform_pos = platform_pos
        self.screen = screen
        self.normal_ground_level = ground_level
        self.top_hitbox = pygame.Rect(platform_pos[0] + 8, platform_pos[1], 48, 1)
        self.bottom_hitbox = pygame.Rect(platform_pos[0], platform_pos[1]+64, 64, 1)
        self.right_hitbox = pygame.Rect(platform_pos[0]+64, platform_pos[1] + 16, 1, 32)
        self.left_hitbox = pygame.Rect(platform_pos[0]-1, platform_pos[1] + 16, 1, 32)
         
class Solid_Platform(Platform):
    def __init__(self, platform_pos, screen, ground_level):
        super().__init__(platform_pos, screen, ground_level)     
    
    def check_collision(self, player):
        #check collision on bottom of the platform
        if player.get_rect().colliderect(self.bottom_hitbox):
            player.pos[1] = self.platform_pos[1] + 60
            player.collide_above = True
            
        #check collision on right of the platform
        if player.get_rect().colliderect(self.right_hitbox):
            player.pos[0] = self.platform_pos[0]+64
            
        if player.get_rect().colliderect(self.left_hitbox):
            player.pos[0] = self.platform_pos[0]-50
            
    def check_top_collision(self, player):
        #check collision on the top of the platform
        if player.get_rect().colliderect(self.top_hitbox):
            player.set_ground_level(self.platform_pos[1] - player.height)
            player.pos[1] = self.platform_pos[1] - player.height+1
            player.collide_below = True
            return True
        elif not player.get_rect().colliderect(self.top_hitbox):
            player.collide_below = False
            player.ground_level = self.normal_ground_level    

class Interactive_Platform(Platform):
    def __init__(self, platform_pos, screen, ground_level):
        super().__init__(platform_pos, screen, ground_level)
        self.interaction_hitbox = pygame.Rect(platform_pos[0], platform_pos[1], 64, 64)
        
class Wood(Solid_Platform):
    def __init__(self, platform_pos, screen, ground_level):
        super().__init__(platform_pos, screen, ground_level)
    
    #draw wood image
    def draw(self):
        images.wood(self.screen, self.platform_pos)
           
class Teleporter(Interactive_Platform):
    def __init__(self, platform_pos, screen, ground_level):
        super().__init__(platform_pos, screen, ground_level)
        
    def draw(self):
        images.floor_teleporter(self.screen, self.platform_pos)
        
    def interact(self, player, screen, pos):
        if player.get_rect().colliderect(self.interaction_hitbox):
            interact_text = font.render("Press E to teleport", True, (255, 255, 255))
            screen.blit(interact_text, (screen.get_width()/2-200, 100))
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_e]:
                player.pos = pos
            return True

class Door(Interactive_Platform):
    def draw(self):
        images.door(self.screen, self.platform_pos)
        
    def interact(self, player, screen):
        if player.get_rect().colliderect(self.interaction_hitbox):
            interact_text = font.render("Press E to open door", True, (255, 255, 255))
            screen.blit(interact_text, (screen.get_width()/2-200, 100))
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_e]:
                player.finish_level = True
            return True
    
#ceiling teleporter where player can teleport to
class Ceiling_Teleporter(Teleporter):
    def __init__(self, platform_pos, screen, ground_level):
        super().__init__(platform_pos, screen, ground_level)
        
    def draw(self):
        images.ceiling_teleporter(self.screen, self.platform_pos)
           
level_one_solid_platform_list = []
level_one_interactive_platform_list = []

def init_level_one(screen, ground_level):   
    #bottom platform with teleporter on top
    for i in range(5):
        wood = Wood([800+i*64, 400], screen, ground_level)
        level_one_solid_platform_list.append(wood)
    
    teleporter_one = Teleporter([928, 336], screen, ground_level)
    level_one_interactive_platform_list.append(teleporter_one)
    
    #top platform where player gets teleported into
    #top 
    for i in range(1, 4):
        wood = Wood([i*64, 0], screen, ground_level)
        level_one_solid_platform_list.append(wood)
    
    #bottom
    for i in range(1, 4):
        wood = Wood([i*64, 192], screen, ground_level)
        level_one_solid_platform_list.append(wood)
    
    #left
    for i in range(4):
        wood = Wood([0, i*64], screen, ground_level)
        level_one_solid_platform_list.append(wood)
    
    #right
    for i in range(4):
        wood = Wood([256, i*64], screen, ground_level)
        level_one_solid_platform_list.append(wood)
    
    teleporter_two = Ceiling_Teleporter([128, 64], screen, ground_level)
    level_one_interactive_platform_list.append(teleporter_two)
    
    door = Door([128, 128], screen, ground_level)
    level_one_interactive_platform_list.append(door)

def level_one(player, screen):
    for platform in level_one_solid_platform_list:
        platform.draw()
        
    for platform in level_one_solid_platform_list:
        platform.check_collision(player)
    
    for platform in level_one_solid_platform_list:    
        if platform.check_top_collision(player):
            break
        
    for platform in level_one_interactive_platform_list:
        platform.draw()
    
    for platform in level_one_interactive_platform_list:
        if type(platform).__name__ == "Teleporter":
            if platform.interact(player, screen, [135, 64]):
                break
            
        if type(platform).__name__ == "Door":
            if platform.interact(player, screen):
                break
        