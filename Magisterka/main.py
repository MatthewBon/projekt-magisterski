import time

from enums.colors import Colors as colors
from utils import draw_grid, reset_grid, calculate_blocks, draw_spot
import pygame
from grid import Grid
from algorithms import a_star, dijkstra, bfs, dfs

WIDTH = 1300


class WindowHandler:
    def __init__(self, rows):
        self.end_spot = None
        self.grid_maze = None
        self.start_spot = None
        self.grid_object = None

        self.rows = rows
        if not rows % 2:
            self.rows += 1
        self.gap = WIDTH // self.rows
        self.width = self.rows * self.gap
        self.generate_maze()
        self.algorithm_analyze()

    def generate_maze(self):
        self.grid_object = Grid(self.rows, self.gap)
        self.grid_maze = self.grid_object.grid_maze
        self.start_spot, self.end_spot = self.grid_object.start_spot, self.grid_object.end_spot

    def run_algorithm(self, algorithm, draw_method, win):
        time_start = time.time()
        path, visited = algorithm(self.grid_maze, self.start_spot, self.end_spot, draw_method, win)
        end_time = round(time.time() - time_start, 2)
        path_cost = 0
        for spot in path:
            path_cost += spot.spot_value
        return end_time, len(path), len(visited), path_cost

    def algorithm_analyze(self):
        algorithms = {
            "Djikstra": dijkstra,
            "A*": a_star,
            "BFS": bfs,
            "DFS": dfs
        }

        total_open_cells = calculate_blocks(self.grid_maze, [colors.WHITE_1, colors.WHITE_10, colors.WHITE_25])
        pygame.display.set_caption("Path Finding Algorithm")
        win = pygame.display.set_mode((self.width, self.width))
        for name, algorithm in algorithms.items():
            print(f'Executing {name} algorithm...\n')
            run = True
            while run == True:
                run = self.window_handler(total_open_cells, win, algorithm, draw_spot)
            if run == 'Quit':
                break
        pygame.quit()

    def window_handler(self, total_open_cells, win, algorithm, draw_method):
        while True:
            draw_grid(win, self.grid_maze)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 'Quit'
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    elif event.key == pygame.K_r:
                        self.generate_maze()
                        draw_grid(win, self.grid_maze)
                    elif event.key == pygame.K_SPACE:
                        execution_time, path_len, searched, path_cost = self.run_algorithm(algorithm, draw_method, win)
                        searched_cells_percentage = round(((searched / total_open_cells) * 100), 2)
                        print(f"\n\tExecution_time: {execution_time} s,"
                              f"\n\tTrace length: {path_len} cells,"
                              f"\n\tSearched cells percentage: {searched_cells_percentage} %"
                              f"\n\tTotal path cost: {path_cost}")
                        time.sleep(2)
                        reset_grid(win, self.grid_maze)


if __name__ == "__main__":
    WindowHandler(75)
