import csv
import os
import time

from enums.colors import Colors as colors
from utils import draw_grid, reset_grid, calculate_blocks, draw_spot
import pygame
from grid import Grid
from algorithms import a_star, dijkstra, bfs, limited_deep_dfs, bfs_no_path

WIDTH = 1400


class AlgorithmAnalyzer:
    def __init__(self, rows, draw_updates, window_mode=True):
        self.end_spot = None
        self.grid_maze = None
        self.start_spot = None
        self.grid_object = None
        self.window_mode = window_mode
        self.draw_updates = draw_updates
        self.rows = rows
        self.gap = WIDTH // self.rows
        self.width = self.rows * self.gap
        if self.width > WIDTH:
            self.width = 500

        filename = f"algorithms_results_{self.rows+1}.csv"

        with open(filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Algorithm_name ", "Execution Time (s) ", "Path Length (cells) ",
                             "Searched Cells (%) ", "Total Path Cost "])
        self.algorithm_analyze()

    def generate_maze(self):
        self.grid_object = Grid(self.rows, self.gap)
        self.grid_maze = self.grid_object.grid_maze
        self.start_spot, self.end_spot = self.grid_object.start_spot, self.grid_object.end_spot

    def run_algorithm(self, algorithm, win):
        time_start = time.time()
        path, visited = algorithm(self.grid_maze, self.start_spot, self.end_spot, win, self.draw_updates,
                                  self.window_mode)
        end_time = round(time.time() - time_start, 2)
        path_cost = 0
        for spot in path:
            path_cost += spot.spot_value
        if self.window_mode:
            time.sleep(1)
        reset_grid(win, self.grid_maze, self.window_mode)
        return end_time, len(path), len(visited), path_cost

    def algorithm_analyze(self):
        algorithms = {
            # "A*": a_star,
            # "Djikstra": dijkstra,
            # "DFS_LIM": limited_deep_dfs,
            "BFS": bfs,
            "BFSNP": bfs_no_path,
        }
        self.window_handler(algorithms)

    def window_handler(self, algorithms):
        win = None
        if self.window_mode:
            pygame.display.set_caption("Path Finding Algorithm")
            win = pygame.display.set_mode((self.width, self.width))
            run = True
            while run:
                # self.run_algorithms_n_times(20, algorithms, win)
                # run = False
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        run = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.run_algorithms_n_times(1, algorithms, win)
                            run = False
        else:
            self.run_algorithms_n_times(1, algorithms, win)
        pygame.quit()

    def run_algorithms_n_times(self, n, algorithms, win):
        for _ in range(n):
            self.generate_maze()
            if self.window_mode:
                draw_grid(win, self.grid_maze)
            total_open_cells = calculate_blocks(self.grid_maze, [colors.WHITE_1, colors.WHITE_10, colors.WHITE_25])
            for name, algorithm in algorithms.items():
                print(f'Executing {name} algorithm...\n')
                exec_time, path_len, searched, path_cost = self.run_algorithm(algorithm, win)
                searched_cells_percentage = round(((searched / total_open_cells) * 100), 2)
                print(f"\n\tExecution_time: {exec_time} s,"
                      f"\n\tTrace length: {path_len} cells,"
                      f"\n\tSearched cells percentage: {searched_cells_percentage} %"
                      f"\n\tTotal path cost: {path_cost}\n")
                self.dump_results_into_csv(name, exec_time, path_len, searched_cells_percentage, path_cost)

    def dump_results_into_csv(self, alg_name, exec_time, path_len, searched, path_cost):
        filename = f"algorithms_results_{self.rows+1}.csv"

        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([alg_name, exec_time, path_len, searched, path_cost])


if __name__ == "__main__":
    display_results = False
    debug_update_draw = False
    if not display_results and debug_update_draw:
        print('Incorrect flag values!')
    else:
        AlgorithmAnalyzer(1000, debug_update_draw, display_results)

