import pygame
from spot import Spot
from enums.colors import Colors as colors
from typing import List, Optional, Union


def manhattan_heuristic(p1: Spot, p2: Spot, weight: int = 1) -> int:
    """
    Calculate the Manhattan heuristic between two spots.

    Args:
        p1 (Spot): The first spot.
        p2 (Spot): The second spot.
        weight (int): The weight to apply to the heuristic.

    Returns:
        int: The Manhattan distance between the two spots.
    """
    return weight * (abs(p1.row - p2.row) + abs(p1.col - p2.col))


def taxicab_heuristic(p1: Spot, p2: Spot) -> int:
    """
    Calculate the Taxicab heuristic between two spots.

    Args:
        p1 (Spot): The first spot.
        p2 (Spot): The second spot.

    Returns:
        int: The Taxicab distance between the two spots.
    """
    return abs(p1.row - p2.row) + abs(p1.col - p2.col) - min(abs(p1.row - p2.row), abs(p1.col - p2.col))


def chebyshev_heuristic(spot: Spot, end: Spot) -> int:
    """
    Calculate the Chebyshev heuristic between two spots.

    Args:
        spot (Spot): The current spot.
        end (Spot): The end spot.

    Returns:
        int: The Chebyshev distance between the two spots.
    """
    return max(abs(spot.row - end.row), abs(spot.col - end.col))


def reconstruct_path(path: List[Spot], grid: List[List[Spot]], start_spot: Spot, end_spot: Spot,
                     draw_updates: bool, win: Optional[pygame.Surface], color: Optional[colors] = None,
                     window_mode: bool = True):
    """
    Reconstruct the path from start to end spot.

    Args:
        path (List[Spot]): The list of spots representing the path.
        grid (List[List[Spot]]): The grid of spots.
        start_spot (Spot): The starting spot.
        end_spot (Spot): The ending spot.
        draw_updates (bool): Flag to draw updates.
        win (Optional[pygame.Surface]): The window surface to draw on.
        color (Optional[colors]): The color to draw the path.
        window_mode (bool): Flag to indicate if window mode is enabled.
    """
    for spot in path:
        if spot != start_spot and spot != end_spot:
            spot.make_path(color)
            if draw_updates and window_mode:
                draw_spot(win, spot)
    if not draw_updates and window_mode:
        draw_grid(win, grid)


def draw_grid(win: pygame.Surface, grid: List[List[Spot]]):
    """
    Draw the entire grid on the window.

    Args:
        win (pygame.Surface): The window surface to draw on.
        grid (List[List[Spot]]): The grid of spots.
    """
    for row in grid:
        for spot in row:
            spot.draw(win)
    pygame.display.update()


def draw_spot(win: pygame.Surface, spot: Spot):
    """
    Draw a single spot on the window.

    Args:
        win (pygame.Surface): The window surface to draw on.
        spot (Spot): The spot to draw.
    """
    spot.draw(win)
    pygame.display.update()


def reset_grid(grid: List[List[Spot]], win: Optional[pygame.Surface] = None, window_mode: bool = True):
    """
    Reset the grid to its initial state.

    Args:
        grid (List[List[Spot]]): The grid of spots.
        win (Optional[pygame.Surface]): The window surface to draw on.
        window_mode (bool): Flag to indicate if window mode is enabled.
    """
    for row in grid:
        for spot in row:
            spot.reset()
            if window_mode:
                spot.draw(win)
    if window_mode:
        pygame.display.update()


def calculate_blocks(grid: List[List[Spot]], color: Union[colors, List[colors]] = colors.TURQUOISE) -> int:
    """
    Calculate the number of blocks of a specific color in the grid.

    Args:
        grid (List[List[Spot]]): The grid of spots.
        color (Union[colors, List[colors]]): The color(s) to count.

    Returns:
        int: The number of blocks of the specified color.
    """
    counter = 0
    for row in grid:
        for spot in row:
            if isinstance(color, list):
                if spot.color in color:
                    counter += 1
            else:
                if spot.color == color:
                    counter += 1
    return counter


def is_within_bounds(x: int, y: int, rows: int) -> bool:
    """
    Check if the given coordinates are within the bounds of the grid.

    Args:
        x (int): The x-coordinate.
        y (int): The y-coordinate.
        rows (int): The number of rows in the grid.

    Returns:
        bool: True if the coordinates are within bounds, False otherwise.
    """
    return 0 < x < rows - 1 and 0 < y < rows - 1
