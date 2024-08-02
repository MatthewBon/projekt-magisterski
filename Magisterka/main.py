import csv
import time
from enums.colors import Colors as colors
from utils import draw_grid, reset_grid, calculate_blocks, manhattan_heuristic, taxicab_heuristic, chebyshev_heuristic
import pygame
from grid import Grid
from algorithms import a_star, dijkstra, bfs, limited_deep_dfs, dfs

WIDTH = 1440
EXECUTION_NUMBER = 5
MIN_SIZE = 50
MID_SIZE = 200
MAX_SIZE = 700


class AlgorithmAnalyzer:
    def __init__(self, rows, draw_updates, window_mode=True, display_time=1):
        self.end_spot = None
        self.grid_maze = None
        self.start_spot = None
        self.grid_object = None
        self.window_mode = window_mode
        self.display_time = display_time
        self.draw_updates = draw_updates
        self.rows = rows
        self.filename = f"algorithms_results_{self.rows}.csv"
        if not self.rows % 2:
            self.rows += 1
        self.gap = WIDTH // self.rows
        self.width = self.rows * self.gap
        if self.width > WIDTH:
            self.width = 500

        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Algorithm_name ", "Execution Time (s) ", "Path Length (cells) ",
                             "Searched Cells (%) ", "Total Path Cost "])
        algorithms = {
            # "A*": a_star,
            # "DJIKSTRA": dijkstra,
            # "DFS_NORMAL": dfs,
            "DFS_LIM": limited_deep_dfs,
            # "BFS": bfs,
        }

        self.window_handler(algorithms)

    def generate_maze(self):
        self.grid_object = Grid(self.rows, self.gap)
        self.grid_maze = self.grid_object.grid_maze
        self.start_spot, self.end_spot = self.grid_object.start_spot, self.grid_object.end_spot

    def run_algorithm(self, algorithm, win, heuristic=None):
        time_start = time.time()
        path, visited = algorithm(self.grid_maze, self.start_spot, self.end_spot, win, self.draw_updates,
                                  self.window_mode, heuristic)
        end_time = round(time.time() - time_start, 4)
        path_cost = 0
        for spot in path:
            path_cost += spot.spot_value
        if self.window_mode:
            time.sleep(self.display_time)
        reset_grid(self.grid_maze, win, self.window_mode)
        return end_time, len(path), len(visited), path_cost

    def window_handler(self, algorithms):
        win = None
        n = EXECUTION_NUMBER
        if self.window_mode:
            pygame.display.set_caption("Path Finding Algorithm")
            win = pygame.display.set_mode((self.width, self.width))
            self.run_algorithms_n_times(n, algorithms, win)
            pygame.quit()
        else:
            self.run_algorithms_n_times(n, algorithms, win)

    def run_algorithms_n_times(self, n, algorithms, win):
        for _ in range(n):
            self.generate_maze()
            if self.window_mode:
                draw_grid(win, self.grid_maze)
            total_open_cells = calculate_blocks(self.grid_maze, [colors.WHITE_1, colors.WHITE_15, colors.WHITE_15])
            for name, algorithm in algorithms.items():
                if name == 'A*':
                    heuristic_list = [manhattan_heuristic, taxicab_heuristic, chebyshev_heuristic]
                    for heuristic in heuristic_list:
                        name += heuristic.__name__
                        print(f'Executing {name} algorithm...\n')

                        exec_time, path_len, searched, path_cost = self.run_algorithm(algorithm, win, heuristic)
                        searched_cells_percentage = round(((searched / total_open_cells) * 100), 4)
                        print(f"\n\tExecution_time: {exec_time} s,"
                              f"\n\tTrace length: {path_len} cells,"
                              f"\n\tSearched cells percentage: {searched_cells_percentage} %"
                              f"\n\tTotal path cost: {path_cost}\n")
                        self.dump_results_into_csv(name, exec_time, path_len, searched_cells_percentage, path_cost)
                else:
                    print(f'Executing {name} algorithm...\n')
                    exec_time, path_len, searched, path_cost = self.run_algorithm(algorithm, win)
                    searched_cells_percentage = round(((searched / total_open_cells) * 100), 4)
                    print(f"\n\tExecution_time: {exec_time} s,"
                          f"\n\tTrace length: {path_len} cells,"
                          f"\n\tSearched cells percentage: {searched_cells_percentage} %"
                          f"\n\tTotal path cost: {path_cost}\n")
                    self.dump_results_into_csv(name, exec_time, path_len, searched_cells_percentage, path_cost)

    def dump_results_into_csv(self, alg_name, exec_time, path_len, searched, path_cost):
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([alg_name, exec_time, path_len, searched, path_cost])


if __name__ == "__main__":
    display_results = True
    debug_update_draw = True
    if not display_results and debug_update_draw:
        print('Incorrect flag values!')
    else:
        #AlgorithmAnalyzer(MIN_SIZE, debug_update_draw, display_results, 0.5)
        AlgorithmAnalyzer(MID_SIZE, debug_update_draw, display_results, 0.5)
        #AlgorithmAnalyzer(MAX_SIZE, debug_update_draw, display_results, 0.5)

