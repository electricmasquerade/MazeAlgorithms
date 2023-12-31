"""This holds the definitions for a maze generator and solver, including the Maze, Cell, and Agent classes."""
import pygame
import random
import time

# Define pygame constants for the window size and frames per second
HEIGHT = 1000
WIDTH = 1000
FPS = 1000

thickness = 3

graphics_enabled = True


class Cell:
    """This is a cell in the maze. It has a position, walls, and a visited flag."""

    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
        # walls are stored as a dictionary of booleans, defaulted to all walls up (True)
        self.walls = {'N': True, 'E': True, 'S': True, 'W': True}
        self.visited = False

    def __repr__(self):
        return f'Cell({self.row}, {self.col})'

    def print_walls(self):
        """Prints the walls of the cell."""
        print(f'Cell({self.row}, {self.col}) walls: {self.walls}')


class Maze:
    """This represents the overall maze, which is a grid of cells."""

    def __init__(self, size: int):
        self.size = size
        # cells are stored as a list of lists, with each inner list representing a row. Walls are up by default.
        self.cells = [[Cell(row, col) for col in range(size)] for row in range(size)]
        self.cell_size = HEIGHT // size

    def __repr__(self):
        return f'Maze({self.size})'

    def print_maze(self):
        """Prints the maze."""
        print(f'Maze({self.size})')
        for row in self.cells:
            print(row)

    def fill_cell(self, color: tuple, screen: pygame.Surface, cell: Cell):
        """Draws a rectangle in the cell to fill it in, and """
        pygame.draw.rect(screen, color, ((cell.col * self.cell_size) + 1, (cell.row * self.cell_size) + 1,
                                         self.cell_size - 2, self.cell_size - 2))
        pygame.display.flip()

    def update_walls(self, cell: Cell, screen: pygame.Surface):
        """Updates the maze by checking the walls of the cell. If the cell wall is marked as False,
            the wall is erased."""
        if graphics_enabled:
            if not cell.walls['N']:
                pygame.draw.line(screen, (51, 204, 51), (cell.col * self.cell_size, cell.row * self.cell_size),
                                 ((cell.col + 1) * self.cell_size, cell.row * self.cell_size), thickness)
            if not cell.walls['E']:
                pygame.draw.line(screen, (51, 204, 51), ((cell.col + 1) * self.cell_size, cell.row * self.cell_size),
                                 ((cell.col + 1) * self.cell_size, (cell.row + 1) * self.cell_size), thickness)
            if not cell.walls['S']:
                pygame.draw.line(screen, (51, 204, 51),
                                 ((cell.col + 1) * self.cell_size, (cell.row + 1) * self.cell_size),
                                 (cell.col * self.cell_size, (cell.row + 1) * self.cell_size), thickness)
            if not cell.walls['W']:
                pygame.draw.line(screen, (51, 204, 51), (cell.col * self.cell_size, (cell.row + 1) * self.cell_size),
                                 (cell.col * self.cell_size, cell.row * self.cell_size), thickness)
            pygame.display.flip()

    def draw_maze(self, screen: pygame.Surface):
        """Draws the initial grid for the maze using pygame. Cell borders are drawn where walls are up.
        Also used to clear the maze generator."""

        screen.fill((255, 255, 255))

        for row in self.cells:
            for cell in row:
                if cell.walls['N']:
                    pygame.draw.line(screen, (0, 0, 0), (cell.col * self.cell_size, cell.row * self.cell_size),
                                     ((cell.col + 1) * self.cell_size, cell.row * self.cell_size), thickness)
                if cell.walls['E']:
                    pygame.draw.line(screen, (0, 0, 0), ((cell.col + 1) * self.cell_size, cell.row * self.cell_size),
                                     ((cell.col + 1) * self.cell_size, (cell.row + 1) * self.cell_size), thickness)
                if cell.walls['S']:
                    pygame.draw.line(screen, (0, 0, 0),
                                     ((cell.col + 1) * self.cell_size, (cell.row + 1) * self.cell_size),
                                     (cell.col * self.cell_size, (cell.row + 1) * self.cell_size), thickness)
                if cell.walls['W']:
                    pygame.draw.line(screen, (0, 0, 0), (cell.col * self.cell_size, (cell.row + 1) * self.cell_size),
                                     (cell.col * self.cell_size, cell.row * self.cell_size), thickness)
        pygame.display.flip()


class Agent:
    """This is a generic agent class. It has a position and a maze that it is created in. It is represented by a
    red box that is drawn in a cell on the maze. """

    def __init__(self, maze: Maze, starting_row: int = 0, starting_col: int = 0, color: tuple = (255, 0, 0),
                 trail_color: tuple = (51, 204, 51)):
        self.maze = maze
        self.row = starting_row
        self.col = starting_col
        self.size = maze.cell_size - 2
        self.color = color
        self.trail_color = trail_color
        self.current_cell = self.maze.cells[self.row][self.col]

    def __repr__(self):
        return f'Agent({self.maze})'

    def print_agent(self):
        """Prints the agent's position."""
        print(f'Agent({self.maze}) is at ({self.row}, {self.col})')

    def draw_agent(self, screen: pygame.Surface):
        """Draws the agent on the maze, centered in the cell."""
        pygame.draw.rect(screen, self.color,
                         ((self.col * self.maze.cell_size) + 1, (self.row * self.maze.cell_size) + 1,
                          self.size, self.size))
        # pygame.display.flip()

    def move(self, direction: str, screen: pygame.Surface):
        """Moves the agent in the given direction, if possible. if the agent is at the edge of the maze, it will not
        move. It will also not move through walls. """
        #
        if graphics_enabled:
            # color in the current spot with the trail color, same size as the agent
            pygame.draw.rect(screen, self.trail_color,
                             ((self.col * self.maze.cell_size) + 1, (self.row * self.maze.cell_size) + 1,
                              self.size, self.size))
        if direction == 'N' and not self.maze.cells[self.row][self.col].walls['N']:
            if self.row > 0:
                self.row -= 1
        elif direction == 'E' and not self.maze.cells[self.row][self.col].walls['E']:
            if self.col < self.maze.size - 1:
                self.col += 1
        elif direction == 'S' and not self.maze.cells[self.row][self.col].walls['S']:
            if self.row < self.maze.size - 1:
                self.row += 1
        elif direction == 'W' and not self.maze.cells[self.row][self.col].walls['W']:
            if self.col > 0:
                self.col -= 1
        else:
            # print('Invalid direction.')
            pass

        self.current_cell = self.maze.cells[self.row][self.col]
        if graphics_enabled:
            self.draw_agent(screen)


def generate_maze(size, algorithm, screen: pygame.Surface = None):
    maze = Maze(size)
    maze_generator = MazeGenerator(maze)
    while not maze_generator.done:
        maze_generator.algorithms[algorithm](screen)  # Pass None for the screen if we're not displaying
        if screen is not None:
            pygame.display.flip()

    return maze


class MazeGenerator(Agent):
    """This is the maze generator class, a superclass of the Agent class. It contains all the maze generation
    algorithms."""

    def __init__(self, maze: Maze, color: tuple = (255, 0, 0), trail_color: tuple = (0, 255, 0)):
        super().__init__(maze, color=color, trail_color=trail_color)
        self.current_cell.visited = True
        self.stack = []
        self.stack.append(self.current_cell)
        self.done = False
        self.algorithms = {'depth_first': self.generate_maze_depth_first_step}

    def generate_maze_depth_first_step(self, screen: pygame.Surface):
        """Generate one step of the maze using iterative backtracking (randomized depth-first)."""
        if len(self.stack) > 0:
            # Pop the current cell from the stack
            self.current_cell = self.stack.pop()

            # place agent on current cell
            self.row = self.current_cell.row
            self.col = self.current_cell.col
            neighbors = []
            if self.current_cell.row > 0:
                neighbors.append(self.maze.cells[self.current_cell.row - 1][self.current_cell.col])
            if self.current_cell.col < self.maze.size - 1:
                neighbors.append(self.maze.cells[self.current_cell.row][self.current_cell.col + 1])
            if self.current_cell.row < self.maze.size - 1:
                neighbors.append(self.maze.cells[self.current_cell.row + 1][self.current_cell.col])
            if self.current_cell.col > 0:
                neighbors.append(self.maze.cells[self.current_cell.row][self.current_cell.col - 1])
            # If current cell has unvisited neighbors, push it back to the stack
            if not all(neighbor.visited for neighbor in neighbors):
                self.stack.append(self.current_cell)

            direction = random.choice(['N', 'E', 'S', 'W'])
            if direction == 'N':
                if self.current_cell.row > 0:
                    neighbor_cell = self.maze.cells[self.current_cell.row - 1][self.current_cell.col]
                    if not neighbor_cell.visited:
                        self.current_cell.walls['N'] = False
                        neighbor_cell.walls['S'] = False
                        neighbor_cell.visited = True
                        self.stack.append(neighbor_cell)
                        self.maze.update_walls(self.current_cell, screen)
                        self.maze.update_walls(neighbor_cell, screen)
                        self.move(direction, screen)
            elif direction == 'E':
                if self.current_cell.col < self.maze.size - 1:
                    neighbor_cell = self.maze.cells[self.current_cell.row][self.current_cell.col + 1]
                    if not neighbor_cell.visited:
                        self.current_cell.walls['E'] = False
                        neighbor_cell.walls['W'] = False
                        neighbor_cell.visited = True
                        self.stack.append(neighbor_cell)
                        self.maze.update_walls(self.current_cell, screen)
                        self.maze.update_walls(neighbor_cell, screen)
                        self.move(direction, screen)
            elif direction == 'S':
                if self.current_cell.row < self.maze.size - 1:
                    neighbor_cell = self.maze.cells[self.current_cell.row + 1][self.current_cell.col]
                    if not neighbor_cell.visited:
                        self.current_cell.walls['S'] = False
                        neighbor_cell.walls['N'] = False
                        neighbor_cell.visited = True
                        self.stack.append(neighbor_cell)
                        self.maze.update_walls(self.current_cell, screen)
                        self.maze.update_walls(neighbor_cell, screen)
                        self.move(direction, screen)
            elif direction == 'W':
                if self.current_cell.col > 0:
                    neighbor_cell = self.maze.cells[self.current_cell.row][self.current_cell.col - 1]
                    if not neighbor_cell.visited:
                        self.current_cell.walls['W'] = False
                        neighbor_cell.walls['E'] = False
                        neighbor_cell.visited = True
                        self.stack.append(neighbor_cell)
                        self.maze.update_walls(self.current_cell, screen)
                        self.maze.update_walls(neighbor_cell, screen)
                        self.move(direction, screen)
        else:
            # No unvisited neighbors, maze generation is complete
            self.done = True


class MazeSolver(Agent):
    def __init__(self, maze: Maze, target_cell: Cell, color: tuple = (0, 0, 255), trail_color: tuple = (0, 255, 0)):
        super().__init__(maze, color=color, trail_color=trail_color)
        self.current_cell.visited = True
        self.stack = []
        self.stack.append(self.current_cell)
        self.done = False
        self.algorithms = {'depth_first': self.depth_first_step, 'breadth_first': self.breadth_first_step(),
                           'a_star': self.a_star_step}
        self.target_cell = target_cell

    def depth_first_step(self, screen: pygame.Surface):
        """One step of the maze solver algorithm using depth first search."""
        pass

    def breadth_first_step(self):
        """One step of the maze solver algorithm using breadth first search."""
        pass

    def a_star_step(self):
        pass


def main():
    """This animates the maze being generated. Useful for testing/visualizing the maze generation algorithm."""
    print('This is a module for a maze generator and solver.')
    maze = Maze(20)
    maze_generator = MazeGenerator(maze)

    if graphics_enabled:
        pygame.init()
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Maze Generator')
        clock = pygame.time.Clock()
        screen.fill((255, 255, 255))
        maze.draw_maze(screen)
        maze_generator.draw_agent(screen)
        pygame.display.flip()
        time.sleep(2)
        # Generate maze step by step

        running = True
        while running:
            clock.tick(FPS)  # Control the frame rate

            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    running = False

            # Generate one step of the maze and update the display
            if not maze_generator.done:
                maze_generator.generate_maze_depth_first_step(screen)
                pygame.display.flip()
            else:
                maze.draw_maze(screen)

    pygame.quit()


if __name__ == '__main__':
    main()
