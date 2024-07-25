import pygame
from enums.colors import Colors as colors


class Spot:
    def __init__(self, row, col, width, total_rows, color):
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

    def __repr__(self):
        return f"Spot({self.row}, {self.col}, {self.color})"

    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return self.color == colors.BLACK

    def is_start(self):
        return self.color == colors.ORANGE

    def is_end(self):
        return self.color == colors.PURPLE

    def is_path(self):
        return self.color in [colors.TURQUOISE, colors.LIME]

    def make_open(self):
        self.color = colors.WHITE

    def make_closed(self):
        self.color = colors.RED

    def mark_next(self):
        self.color = colors.GREEN

    def make_barrier(self):
        self.color = colors.BLACK

    def make_path(self, color=colors.TURQUOISE):
        self.color = colors.TURQUOISE if not color else color

    def make_start(self):
        self.color = colors.ORANGE

    def make_end(self):
        self.color = colors.PURPLE

    def reset(self):
        if not self.is_barrier() and not self.is_start() and not self.is_end() and not self.is_path():
            self.make_open()

    def draw(self, win):
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

    def update_barrier_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.row > 0 and grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.col > 0 and grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
