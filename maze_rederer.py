import math
import sys

import pygame

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)


class MazeRenderer:

    def __init__(self, window_size, cell_n, title):
        pygame.init()
        # Window Parameters
        self.window_size = window_size
        self.cell_n = cell_n
        self.square_size = math.floor(window_size / cell_n)
        # Create surface
        self.display_surf = pygame.display.set_mode((window_size, window_size), 0, 32)
        pygame.display.set_caption(title)
        # Cells Grid
        self.grid = self.createGrid(cell_n)

    def createGrid(self, cell_n):
        return [[pygame.Rect(i * self.square_size,
                             j * self.square_size,
                             self.square_size,
                             self.square_size) for j in range(cell_n)] for i in range(cell_n)]

    def render_maze(self, maze):
        # Background
        self.display_surf.fill(WHITE)
        # self.render_grid()
        # Fill Wall Cells
        for i in range(self.cell_n):
            for j in range(self.cell_n):
                if maze[i][j] == 'X':
                    pygame.draw.rect(self.display_surf, BLACK, self.grid[i][j], 0)  # WALLs
                elif maze[i][j] == 'A':
                    pygame.draw.rect(self.display_surf, YELLOW, self.grid[i][j], 0)  # START
                elif maze[i][j] == 'B':
                    pygame.draw.rect(self.display_surf, GREEN, self.grid[i][j], 0)  # FINISH

    def render_grid(self):
        # Render grid:
        for i in range(self.cell_n):
            for j in range(self.cell_n):
                pygame.draw.rect(self.display_surf, BLACK, self.grid[i][j], 1)  # GRID

    def render_solution(self, solution_lst):
        for pos in solution_lst[1:-1]:  # cut of start and end position
            pygame.draw.rect(self.display_surf, RED, self.grid[pos[0]][pos[1]], 0)  # PATH


    def show(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            pygame.display.update()
