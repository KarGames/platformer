import pygame

def ground(screen, ground_level):
    ground = pygame.image.load("images/ground.png")
    for i in range(5):
        screen.blit(ground, (i*256, ground_level-14))
        
def wood(screen, pos):
    wood = pygame.image.load("images/wood.png")
    screen.blit(wood, pos)
    
def floor_teleporter(screen, pos):
    teleporter = pygame.image.load("images/teleporter.png")
    screen.blit(teleporter, pos)
    
def ceiling_teleporter(screen, pos):
    teleporter = pygame.image.load("images/teleporter.png")
    teleporter = pygame.transform.flip(teleporter, False, True)
    screen.blit(teleporter, pos)
    
def door(screen, pos):
    door = pygame.image.load("images/door.png")
    screen.blit(door, pos)