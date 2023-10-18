"""This is the main function for the maze algorithms. It should draw the maze the modules from definitions.py"""

import definitions
import pygame
import time


definitions.graphics_enabled = False
FPS = 60


pygame.init()
screen = pygame.display.set_mode((definitions.WIDTH, definitions.HEIGHT))
pygame.display.set_caption('Maze Generator')
maze = definitions.generate_maze(50, None)
clock = pygame.time.Clock()
screen.fill((255, 255, 255))
maze.draw_maze(screen)
definitions.graphics_enabled = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    pygame.display.update()
    clock.tick(FPS)






