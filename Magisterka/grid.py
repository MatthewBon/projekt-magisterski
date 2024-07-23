import random

import pygame
from colorama import Fore, init

from enums.colors import Colors as colors
from spot import Spot


def generate_grid_maze(rows, gap):
    init()

    def is_within_bounds(x, y):
        return 0 < x < rows - 1 and 0 < y < rows - 1

    def carve_passages_froms_start(cx, cy):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx * 2, cy + dy * 2
            if is_within_bounds(nx, ny) and grid_maze[nx][ny].color == colors.BLACK:
                grid_maze[cx][cy].color = colors.WHITE
                grid_maze[cx + dx][cy + dy].color = colors.WHITE
                grid_maze[nx][ny].color = colors.WHITE
                carve_passages_froms_start(nx, ny)

    def ensure_path_to_end(maze, start, end):
        stack = [start]
        visited = set()
        while stack:
            current = stack.pop()
            if current == end:
                return True
            if current not in visited:
                visited.add(current)
                cx, cy = current
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = cx + dx, cy + dy
                    if is_within_bounds(nx, ny) and maze[nx][ny].color in [colors.WHITE, colors.TURQUOISE]:
                        stack.append((nx, ny))
        return False

    def print_grid_maze_to_console(maze):
        print('\n')
        for row in maze:
            for spot in row:
                if spot.color == colors.BLACK:
                    print(Fore.RED + 'w ', end="")
                elif spot.color == colors.WHITE:
                    print(Fore.GREEN + 'c ', end="")
                elif spot.color == colors.ORANGE:
                    print(Fore.YELLOW + 's ', end="")
                elif spot.color == colors.TURQUOISE:
                    print(Fore.BLUE + 'e ', end="")
            print(Fore.RESET)  # Reset the color after each line

    start_x, start_y = 1, 1
    end_x, end_y = rows - 2, rows - 2

    while True:
        grid_maze = [[Spot(y, x, gap, rows, colors.BLACK) for x in range(rows)] for y in range(rows)]
        carve_passages_froms_start(start_x, start_y)
        grid_maze[start_y][start_x].color = colors.ORANGE
        grid_maze[end_y][end_x].color = colors.TURQUOISE
        if ensure_path_to_end(grid_maze, (start_x, start_y), (end_x, end_y)):
            break

    print_grid_maze_to_console(grid_maze)
    return grid_maze, grid_maze[1][1], grid_maze[rows - 2][rows - 2]


def draw(win, grid):
    win.fill(colors.WHITE.value)
    for row in grid:
        for spot in row:
            spot.draw(win)
    pygame.display.update()


def main(width):
    rows = 31
    generate_grid_maze(rows, width)


if __name__ == "__main__":
    main(200)
