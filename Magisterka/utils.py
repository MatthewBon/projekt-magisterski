import pygame
from enums.colors import Colors as colors


def heuristic(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, color=None):
    while current in came_from:
        current = came_from[current]
        current.make_path(color)


def draw_grid(win, grid):
    win.fill(colors.WHITE.value)
    for row in grid:
        for spot in row:
            spot.draw(win)
    pygame.display.update()


def reset_grid(grid):
    for row in grid:
        for spot in row:
            spot.reset()
    pygame.display.update()


def calculate_blocks(grid, color=colors.TURQUOISE):
    counter = 0
    for row in grid:
        for spot in row:
            if spot.color == color:
                counter += 1
    return counter

