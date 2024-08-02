import pygame
from enums.colors import Colors as colors
from enums.weight import Weight as spot_weight
from typing import List, Tuple


class Spot:
    def __init__(self, row: int, col: int, width: int, total_rows: int, color: colors,
                 spot_value: int = spot_weight.DEFAULT.value):
        """
        Initialize a Spot.

        Args:
            row (int): Row position of the spot.
            col (int): Column position of the spot.
            width (int): Width of the spot.
            total_rows (int): Total number of rows in the grid.
            color (colors): Color of the spot.
            spot_value (int): Value of the spot.
        """
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = color
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.spot_value = spot_value

    def __lt__(self, other):
        """
        Compare two spots (required for priority queue).

        Args:
            other: Another spot.

        Returns:
            bool: Always returns False.
        """
        return False

    def __repr__(self) -> str:
        """
        Return a string representation of the spot.

        Returns:
            str: String representation of the spot.
        """
        return f"Spot({self.row}, {self.col}, {self.color})"

    def get_pos(self) -> Tuple[int, int]:
        """
        Get the position of the spot.

        Returns:
            Tuple[int, int]: The row and column of the spot.
        """
        return self.row, self.col

    def is_barrier(self) -> bool:
        """
        Check if the spot is a barrier.

        Returns:
            bool: True if the spot is a barrier, False otherwise.
        """
        return self.color == colors.BLACK

    def is_start(self) -> bool:
        """
        Check if the spot is the start spot.

        Returns:
            bool: True if the spot is the start spot, False otherwise.
        """
        return self.color == colors.ORANGE

    def is_end(self) -> bool:
        """
        Check if the spot is the end spot.

        Returns:
            bool: True if the spot is the end spot, False otherwise.
        """
        return self.color == colors.PURPLE

    def is_closed(self) -> bool:
        """
        Check if the spot is closed.

        Returns:
            bool: True if the spot is closed, False otherwise.
        """
        return self.color == colors.RED

    def is_path(self) -> bool:
        """
        Check if the spot is part of the path.

        Returns:
            bool: True if the spot is part of the path, False otherwise.
        """
        return self.color in [colors.TURQUOISE, colors.LIME]

    def make_open(self):
        """
        Make the spot open with color based on its value.
        """
        if self.spot_value == spot_weight.DEFAULT.value:
            self.color = colors.WHITE_1
        elif self.spot_value == spot_weight.LIGHT.value:
            self.color = colors.WHITE_5
        elif self.spot_value == spot_weight.HEAVY.value:
            self.color = colors.WHITE_15

    def make_closed(self):
        """
        Make the spot a closed.
        """
        self.color = colors.RED

    def make_next(self):
        """
        Make the spot a next spot to be checked.
        """
        self.color = colors.GREEN

    def make_barrier(self):
        """
        Make the spot a barrier.
        """
        self.color = colors.BLACK

    def make_path(self, color=colors.TURQUOISE):
        """
        Make the spot a part of the path.

        Args:
            color (colors): Color to mark the path.
        """
        self.color = colors.TURQUOISE if not color else color

    def make_start(self):
        """
        Make the spot a start spot.
        """
        self.color = colors.ORANGE

    def make_end(self):
        """
        Make the spot a end spot.
        """
        self.color = colors.PURPLE

    def reset(self):
        """
        Reset the spot to open if it's not a barrier, start, or end spot.
        """
        if not self.is_barrier() and not self.is_start() and not self.is_end():
            self.make_open()

    def draw(self, win: pygame.Surface):
        """
        Draw the spot on the window.

        Args:
            win (pygame.Surface): The window surface.
        """
        pygame.draw.rect(win, self.color.value, (self.x, self.y, self.width, self.width))

    def update_open_neighbors(self, grid: List[List['Spot']]):
        """
        Update the open neighbors of the spot.

        Args:
            grid (List[List['Spot']]): The grid of spots.
        """
        self.neighbors = []
        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

    def update_barrier_neighbors(self, grid: List[List['Spot']]):
        """
        Update the barrier neighbors of the spot.

        Args:
            grid (List[List['Spot']]): The grid of spots.
        """
        self.neighbors = []
        if self.row > 0 and grid[self.row - 1][self.col].is_barrier():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])

        if self.col < self.total_rows - 1 and grid[self.row][self.col + 1].is_barrier():  # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])

        if self.row < self.total_rows - 1 and grid[self.row + 1][self.col].is_barrier():  # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.col > 0 and grid[self.row][self.col - 1].is_barrier():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
