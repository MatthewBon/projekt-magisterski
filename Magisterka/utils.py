import pygame
from enums.colors import Colors as colors


def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(path, start_spot, end_spot, draw_method, win, color=None):
    for spot in path:
        if spot != start_spot and spot != end_spot:
            spot.make_path(color)
            draw_method(win, spot)


def clear_grid_after_algorith(visited_spots, start_spot, end_spot):
    for spot in visited_spots:
        if spot != start_spot and spot != end_spot:
            spot.make_open()


def draw_grid(win, grid):
    for row in grid:
        for spot in row:
            spot.draw(win)
    pygame.display.update()


def draw_spot(win, spot):
    spot.draw(win)
    pygame.display.update()


def reset_grid(win, grid):
    for row in grid:
        for spot in row:
            spot.reset()
            spot.draw(win)
    pygame.display.update()


def calculate_blocks(grid, color=colors.TURQUOISE):
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


def is_within_bounds(x, y, rows):
    return 0 < x < rows - 1 and 0 < y < rows - 1

