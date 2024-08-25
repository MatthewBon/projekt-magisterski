import os
import shutil
import csv
import time
from logger import ProjectLogger
from enums.colors import Colors as colors
from utils import draw_grid, reset_grid, calculate_blocks
import pygame
from grid import Grid
from algorithms import (a_star, dijkstra, bfs, dfs, limited_deep_dfs, bidirectional_a_star,
                        equalized_bidirectional_a_star)
from typing import Tuple, Dict, Any
from scoring_and_plot import analyze_results_and_generate_plot


WIDTH = 1440
EXECUTION_NUMBER = 500
MIN_SIZE = 40
MID_SIZE = 160
MAX_SIZE = 640


class AlgorithmAnalyzer(ProjectLogger):
    def __init__(self, rows: int, draw_updates: bool, directory: str, window_mode: bool = True, show_plot: bool = False,
                 start_end_in_the_same_q: bool = False, display_time: int = 1):
        """
        Initialize the AlgorithmAnalyzer.

        Args:
            rows (int): Number of rows in the grid.
            draw_updates (bool): Flag to draw updates.
            window_mode (bool): Flag for window mode.
            display_time (int): Time to display the result.
        """
        super().__init__()
        if not draw_updates and window_mode:
            self.logger.error('Incorrect flag values!')
        self.end_spot = None
        self.grid_maze = None
        self.start_spot = None
        self.grid_object = None
        self.start_end_in_the_same_q = start_end_in_the_same_q
        self.window_mode = window_mode
        self.display_time = display_time
        self.draw_updates = draw_updates
        self.show_plot = show_plot
        self.rows = rows
        if not self.rows % 2:
            self.rows += 1
        self.gap = WIDTH // self.rows
        self.width = self.rows * self.gap
        if self.width > WIDTH:
            self.width = 500

        # Directory for storing CSV and PNG files
        self.directory = directory

        # Create CSV file inside the directory
        self.filename = os.path.join(self.directory, f"algorithms_results_{self.rows}_{start_end_in_the_same_q}.csv")

        # Create CSV file and write the header
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Algorithm_name", "Execution Time (s)", "Searched Cells", "Total Path Cost"])
        algorithms = {
            "A*": a_star,
            "BA*": bidirectional_a_star,
            "EBA*": equalized_bidirectional_a_star,
            "DIJKSTRA": dijkstra,
            "DFS_NORMAL": dfs,
            "DFS_LIM": limited_deep_dfs,
            "BFS": bfs,
        }

        self.window_handler(algorithms)
        self.analyze_results(rows)

    def generate_maze(self):
        """
        Generate the maze using Grid class.
        """
        self.grid_object = Grid(self.rows, self.gap, self.start_end_in_the_same_q)
        self.grid_maze = self.grid_object.grid_maze
        self.start_spot, self.end_spot = self.grid_object.start_spot, self.grid_object.end_spot

    def solv_maze(self, algorithm, **kwargs) -> Tuple[float, int, float]:
        """
        Run a given algorithm and measure its performance.

        Args:
            algorithm: The algorithm to run.
            kwargs: Additional arguments like 'win' and 'heuristic'.

        Returns:
            Tuple containing execution time, path length, number of visited cells, and total path cost.
        """
        win = kwargs.get('win')

        time_start = time.time()
        path, visited = algorithm(self.grid_maze, self.start_spot, self.end_spot, win=win,
                                  draw_updates=self.draw_updates, window_mode=self.window_mode)
        end_time = round(time.time() - time_start, 10)
        path_cost = sum(spot.spot_value for spot in path)
        if self.window_mode:
            time.sleep(self.display_time)
        reset_grid(self.grid_maze, win, self.window_mode)
        return end_time, len(visited), path_cost

    def window_handler(self, algorithms: Dict[str, Any]):
        """
        Handle the window setup and execution of algorithms.

        Args:
            algorithms (dict): Dictionary of algorithms to run.
        """
        win = None
        n = EXECUTION_NUMBER
        if self.window_mode:
            pygame.display.set_caption("Path Finding Algorithm")
            win = pygame.display.set_mode((self.width, self.width))
            self.run_algorithms_n_times(n, algorithms, win)
            pygame.quit()
        else:
            self.run_algorithms_n_times(n, algorithms, win)

    def run_algorithms_n_times(self, n: int, algorithms: Dict[str, Any], win):
        """
        Run each algorithm 'n' times and log the results.

        Args:
            n (int): Number of times to run each algorithm.
            algorithms (dict): Dictionary of algorithms to run.
            win: Pygame window to draw the grid.
        """
        for i in range(n):
            self.logger.debug(f"{i} iteration running...")
            self.generate_maze()
            if self.window_mode:
                draw_grid(win, self.grid_maze)
            total_open_cells = calculate_blocks(self.grid_maze, [colors.WHITE_1, colors.WHITE_15, colors.WHITE_15])
            for name, algorithm in algorithms.items():
                self.logger.debug(f'Executing {name} algorithm...\n')
                exec_time, searched, path_cost = self.solv_maze(algorithm, win=win)
                searched_cells_percentage = round(((searched / total_open_cells) * 100), 4)
                self.logger.debug(f"\n\tExecution_time: {exec_time} s,"
                                  f"\n\tSearched cells : {searched}"
                                  f"\n\tSearched cells percentage: {searched_cells_percentage} %"
                                  f"\n\tTotal path cost: {path_cost}\n")
                self.dump_results_into_csv(name, exec_time, searched, path_cost)

    def dump_results_into_csv(self, alg_name: str, exec_time: float, searched: int, path_cost: float):
        """
        Dump the results of algorithm execution into a CSV file.

        Args:
            alg_name (str): Name of the algorithm.
            exec_time (float): Execution time in seconds.
            searched (int): Number of searched cells.
            path_cost (float): Total cost of the path.
        """
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([alg_name, exec_time, searched, path_cost])

    def analyze_results(self, rows):
        analyze_results_and_generate_plot(self.filename, rows, self.logger, self.show_plot,
                                          self.start_end_in_the_same_q)


if __name__ == "__main__":
    display_results = False
    debug_update_draw = False
    show_plt = False

    for size in [MIN_SIZE, MID_SIZE, MAX_SIZE]:
        # Directory for storing CSV and PNG files
        directory_name = f"maze_{size}"
        # Check if the directory exists and remove its contents if it does
        if os.path.exists(directory_name):
            shutil.rmtree(directory_name)
        # Recreate the directory
        os.makedirs(directory_name)

        AlgorithmAnalyzer(size, debug_update_draw, directory_name, display_results, show_plt)
        AlgorithmAnalyzer(size, debug_update_draw, directory_name, display_results, show_plt, True)
