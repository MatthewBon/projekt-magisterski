import time
from enums.colors import Colors as colors
from utils import draw_grid, reset_grid, calculate_blocks
import pygame
from grid import Grid
from algorithms import a_star, dijkstra, bfs


WIDTH = 1200


def run_algorithm(algorithm, grid, start, end):
    execution_time, trace_length, searched = algorithm(grid, start, end)
    return execution_time, trace_length, len(searched),


def main(display_mode=False):
    rows = 7000
    if not rows % 2:
        rows += 1
    gap = WIDTH // rows
    width = rows * gap
    pygame.display.set_caption("Path Finding Algorithm")
    grid_object = Grid(rows, gap)
    grid_maze, start, end = grid_object.grid_maze, grid_object.start_spot, grid_object.end_spot
    algorithms = {
        "Djikstra": dijkstra,
        "A*": a_star,
        #"BFS": bfs
    }
    if display_mode:
        window_handler(grid_maze, width, start, end)
    else:
        total_cells = calculate_blocks(grid_maze, colors.WHITE)
        for name, algorithm in algorithms.items():
            print(f"Current algorythm name: {name}")
            execution_time, trace_len, searched = run_algorithm(algorithm, grid_maze, start, end)
            print(f"\tExecution_time: {execution_time},"
                  f" Trace length: {trace_len}, Searched open cells: {searched},"
                  f" Total open cells: {total_cells}")


def window_handler(grid, width, start, end):
    win = pygame.display.set_mode((width, width))
    total_cells = calculate_blocks(grid, colors.WHITE)
    run = True
    algorithms = {
        "Djikstra": dijkstra,
        "A*": a_star,
        #"BFS": bfs
    }

    while run:
        draw_grid(win, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                for name, algorithm in algorithms.items():
                    reset_grid(grid)
                    draw_grid(win, grid)
                    time.sleep(2)
                    if event.key == pygame.K_SPACE:
                        execution_time, trace_len, searched = run_algorithm(algorithm, grid, start, end)
                        print(f"Algorithm name: {name}, Execution_time: {execution_time},"
                              f" Trace length: {trace_len}, Searched open cells: {searched},"
                              f" Total open cells: {total_cells}")
                        draw_grid(win, grid)
                        time.sleep(2)
                    elif event.key == pygame.K_r:
                        reset_grid(grid)

    pygame.quit()


if __name__ == "__main__":
    main(False)
