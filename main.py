"""This is the main function for the maze algorithms. It should draw the maze the modules from definitions.py"""

import definitions
import pygame
import time

definitions.graphics_enabled = False
FPS = 20

generation_algorithm = 'depth_first'
solver_algorithm = 'depth_first'

pygame.init()
screen = pygame.display.set_mode((definitions.WIDTH, definitions.HEIGHT))
pygame.display.set_caption('Maze Generator')
maze = definitions.generate_maze(25, generation_algorithm, None)

agent = definitions.MazeSolver(maze, color=(255, 0, 0), trail_color=(0, 200, 0), target_cell=maze.cells[-1][-1])
clock = pygame.time.Clock()
screen.fill((255, 255, 255))
maze.draw_maze(screen)
definitions.graphics_enabled = True
agent.draw_agent(screen)
time.sleep(2)
running = True

while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # solve one step of the maze
    if not agent.done:
        agent.algorithms[solver_algorithm](screen)
        agent.draw_agent(screen)
        pygame.display.flip()
    else:
        print('Maze solved!')
        running = False
    pygame.display.update()
