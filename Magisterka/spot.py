import pygame
from enums.colors import Colors as colors


class Spot:
    def __init__(self, row, col, width, total_rows, color=colors.WHITE):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = color
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def __lt__(self, other):
        return False

    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return self.color == colors.BLACK

    def reset(self):
        self.color = colors.WHITE

    def make_closed(self):
        self.color = colors.RED

    def make_open(self):
        self.color = colors.GREEN

    def make_barrier(self):
        self.color = colors.BLACK

    def make_path(self):
        self.color = colors.PURPLE

    def make_start(self):
        self.color = colors.ORANGE

    def make_end(self):
        self.color = colors.TURQUOISE

    def draw(self, win):
        #print(self.width)
        pygame.draw.rect(win, self.color.value, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
