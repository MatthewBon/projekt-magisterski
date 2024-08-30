import pygame
from spot import Spot
from enums.colors import Colors as colors
from typing import List, Optional


def manhattan_heuristic(p1: Spot, p2: Spot, weight: int = 1) -> int:
    """
    Calculate the Manhattan distance heuristic between two spots.

    Args:
        p1 (Spot): The first spot.
        p2 (Spot): The second spot.
        weight (int): The weight to apply to the heuristic. Defaults to 1.

    Returns:
        int: The Manhattan distance between the two spots.
    """
    return weight * (abs(p1.row - p2.row) + abs(p1.col - p2.col))


def chebyshev_heuristic(spot: Spot, end: Spot) -> int:
    """
    Calculate the Chebyshev distance heuristic between two spots.

    Args:
        spot (Spot): The current spot.
        end (Spot): The target spot.

    Returns:
        int: The Chebyshev distance between the two spots.
    """
    return max(abs(spot.row - end.row), abs(spot.col - end.col))


def reconstruct_path(path: List[Spot], grid: List[List[Spot]], start_spot: Spot, end_spot: Spot,
                     draw_updates: bool, win: Optional[pygame.Surface], color: Optional[colors] = None,
                     window_mode: bool = True) -> None:
    """
    Reconstruct and display the path from the start spot to the end spot.

    Args:
        path (List[Spot]): The list of spots representing the path.
        grid (List[List[Spot]]): The grid of spots.
        start_spot (Spot): The starting spot of the path.
        end_spot (Spot): The ending spot of the path.
        draw_updates (bool): Whether to draw updates to the window.
        win (Optional[pygame.Surface]): The window surface to draw on.
        color (Optional[colors]): The color to draw the path. Defaults to TURQUOISE.
        window_mode (bool): Whether the window mode is enabled. Defaults to True.
    """
    for spot in path:
        if spot != start_spot and spot != end_spot:
            spot.make_path(color)
            if draw_updates and window_mode:
                draw_spot(win, spot)
    if not draw_updates and window_mode:
        draw_grid(win, grid)


def draw_grid(win: pygame.Surface, grid: List[List[Spot]]) -> None:
    """
    Draw the entire grid of spots on the window surface.

    Args:
        win (pygame.Surface): The window surface to draw on.
        grid (List[List[Spot]]): The grid of spots.
    """
    for row in grid:
        for spot in row:
            spot.draw(win)
    pygame.display.update()


def draw_spot(win: pygame.Surface, spot: Spot) -> None:
    """
    Draw a single spot on the window surface.

    Args:
        win (pygame.Surface): The window surface to draw on.
        spot (Spot): The spot to draw.
    """
    spot.draw(win)
    pygame.display.update()


def reset_grid(grid: List[List[Spot]], win: Optional[pygame.Surface] = None, window_mode: bool = True) -> None:
    """
    Reset the grid to its initial state, updating the window if necessary.

    Args:
        grid (List[List[Spot]]): The grid of spots.
        win (Optional[pygame.Surface]): The window surface to draw on. Defaults to None.
        window_mode (bool): Whether the window mode is enabled. Defaults to True.
    """
    for row in grid:
        for spot in row:
            spot.reset()
            if window_mode and win:
                spot.draw(win)
    if window_mode and win:
        pygame.display.update()


def is_within_bounds(x: int, y: int, rows: int) -> bool:
    """
    Check if the given coordinates are within the valid bounds of the grid.

    Args:
        x (int): The x-coordinate (row index).
        y (int): The y-coordinate (column index).
        rows (int): The total number of rows in the grid.

    Returns:
        bool: True if the coordinates are within bounds, False otherwise.
    """
    return 0 < x < rows - 1 and 0 < y < rows - 1
