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
            row (int): The row position of the spot in the grid.
            col (int): The column position of the spot in the grid.
            width (int): The width (and height) of the spot.
            total_rows (int): The total number of rows in the grid.
            color (colors): The initial color of the spot.
            spot_value (int): The weight or cost associated with moving through the spot.
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

    def __lt__(self, other) -> bool:
        """
        Compare two spots (required for priority queue operations).

        Args:
            other (Spot): Another spot for comparison.

        Returns:
            bool: Always returns False, as Spot instances are not directly comparable.
        """
        return False

    def __repr__(self) -> str:
        """
        Return a string representation of the spot.

        Returns:
            str: String representation of the spot, including its row, column, and color.
        """
        return f"Spot({self.row}, {self.col}, {self.color})"

    def get_pos(self) -> Tuple[int, int]:
        """
        Get the grid position of the spot.

        Returns:
            Tuple[int, int]: A tuple containing the row and column of the spot.
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
        Check if the spot is closed (visited).

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

    def make_open(self) -> None:
        """
        Mark the spot as open (not a barrier) and assign a color based on its value.
        """
        if self.spot_value == spot_weight.DEFAULT.value:
            self.color = colors.WHITE_1
        elif self.spot_value == spot_weight.LIGHT.value:
            self.color = colors.WHITE_5
        elif self.spot_value == spot_weight.HEAVY.value:
            self.color = colors.WHITE_15

    def make_closed(self) -> None:
        """
        Mark the spot as closed (visited).
        """
        self.color = colors.RED

    def make_next(self) -> None:
        """
        Mark the spot as the next spot to be checked (e.g., part of the frontier).
        """
        self.color = colors.GREEN

    def make_barrier(self) -> None:
        """
        Mark the spot as a barrier.
        """
        self.color = colors.BLACK

    def make_path(self, color: colors = colors.TURQUOISE) -> None:
        """
        Mark the spot as part of the path.

        Args:
            color (colors, optional): The color to use for marking the path. Defaults to TURQUOISE.
        """
        self.color = colors.TURQUOISE if color is None else color

    def make_start(self) -> None:
        """
        Mark the spot as the start spot.
        """
        self.color = colors.ORANGE

    def make_end(self) -> None:
        """
        Mark the spot as the end spot.
        """
        self.color = colors.PURPLE

    def reset(self) -> None:
        """
        Reset the spot to its open state, unless it's a barrier, start, or end spot.
        """
        if not self.is_barrier() and not self.is_start() and not self.is_end():
            self.make_open()

    def draw(self, win: pygame.Surface) -> None:
        """
        Draw the spot on the window.

        Args:
            win (pygame.Surface): The Pygame surface to draw on.
        """
        pygame.draw.rect(win, self.color.value, (self.x, self.y, self.width, self.width))

    def update_open_neighbors(self, grid: List[List['Spot']]) -> None:
        """
        Update the spot's list of open (non-barrier) neighbors.

        Args:
            grid (List[List[Spot]]): The grid of spots.
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

    def update_barrier_neighbors(self, grid: List[List['Spot']]) -> None:
        """
        Update the spot's list of barrier neighbors.

        Args:
            grid (List[List[Spot]]): The grid of spots.
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
