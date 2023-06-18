import tkinter as tk
from tkinter import ttk

level = 0
running = True

class Button():
    def __init__(self, level, root):
        self.level = level
        self.root = root
    
    def set_level(self):
        global level
        level = self.level
        self.root.destroy()
        
    def quit_game(self):
        global running
        running = False
        self.root.destroy()

def loop():
    root = tk.Tk()
    root.title("Platformer")
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    
    button_one = Button(1, root)
    #following levels not added yet
    button_two = Button(2, root)
    button_three = Button(3, root)
    button_four = Button(4, root)
    quit_button = Button(None, root)

    root.geometry(f"{width}x{height}")
    root.grid_columnconfigure(0, weight=1)
    title = ttk.Frame(root, width=400, height=100)
    title.grid()
    ttk.Label(title, text="Levels", font="Arial 40").grid(column=0, row=0)
    button = ttk.Button(title, text="QUIT", command=quit_button.quit_game).grid(column=1, row=0)

    levels = ttk.Frame(root, width=400, height=400)
    levels.grid()
    ttk.Button(levels, text="1", command=button_one.set_level).grid(column=0, row=0)
    ttk.Button(levels, text="2", command=root.destroy).grid(column=1, row=0)
    ttk.Button(levels, text="3", command=root.destroy).grid(column=2, row=0)
    ttk.Button(levels, text="4", command=root.destroy).grid(column=3, row=0)

    if level == 0:
        root.mainloop()
        
loop()
    
import pygame
import images
import levels
from player import Player
from enemy import Enemy

pygame.init()

WIDTH, HEIGHT = 1280, 800
CHARACTER_WIDTH, CHARACTER_HEIGHT = 50, 50
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60
SKY_COLOR = (135, 206, 235)
ground_level = screen.get_height()-242
speed = 6
health = 100
strength = 5
start_pos = [5, ground_level]
restart = False


#create new player
player = Player(health, strength, start_pos, CHARACTER_WIDTH, CHARACTER_HEIGHT)

#create new enemy for testing purposes
enemy = Enemy(health, strength, [500, ground_level], [750, ground_level], CHARACTER_WIDTH, CHARACTER_HEIGHT, [500, ground_level])

#sets all the platforms in level one into a list to loop through and draw everything
levels.init_level_one(screen, ground_level)

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
    screen.fill(SKY_COLOR)
    
    print(level)
    if level == 0:
        loop()
    elif level == 1:
        if restart:
            player.pos = [5, ground_level]
            enemy = Enemy(health, strength, [500, ground_level], [750, ground_level], CHARACTER_WIDTH, CHARACTER_HEIGHT, [500, ground_level])
            restart = False
            
        levels.level_one(player, screen)
        
    #handle left and right movement of the player
    player.handle_movement()
    if player.is_jump:
        player.jump()
        
    #handle enemy movement
    enemy.move()
    enemy.check_collision(player)
    
    #draw flooring tiles on the bottom of the level
    images.ground(screen, ground_level)
    player.draw()
    enemy.draw()
    
    player.gravity()
    
    if player.pos[1] >= player.ground_level:
        player.can_jump = True
    
    if player.health <= 0:
        print("You Lost!")
        running = False
    elif player.finish_level:
        print("You Won!")
        level = 0
        player.finish_level = False
        restart = True
        
    pygame.display.flip()
            
pygame.quit()