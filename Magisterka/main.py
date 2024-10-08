import os
import shutil
import csv
import time
from logger import ProjectLogger
from utils import draw_grid, reset_grid
import pygame
from grid import Grid
from algorithms import (a_star, dijkstra, bfs, dfs, limited_deep_dfs, bidirectional_a_star,
                        equalized_bidirectional_a_star)
from typing import Tuple, Dict, Any, Optional
from scoring_and_plot import analyze_results_and_generate_plot

WIDTH = 1440
EXECUTION_NUMBER = 500
MIN_SIZE = 40
MID_SIZE = 160
MAX_SIZE = 640


class AlgorithmAnalyzer(ProjectLogger):
    def __init__(self, rows: int, draw_updates: bool, directory: str, window_mode: bool = True, show_plot: bool = False,
                 cell_open_percentage: int = 0, display_time: int = 1):
        """
        Initialize the AlgorithmAnalyzer.

        Args:
            rows (int): Number of rows in the grid.
            draw_updates (bool): Flag to draw updates.
            directory (str): Directory for storing results.
            window_mode (bool): Flag for window mode.
            show_plot (bool): Flag to show plot after analysis.
            display_time (int): Time to display the result.
        """
        super().__init__()
        if not draw_updates and window_mode:
            self.logger.error('Incorrect flag values!')
        self.end_spot = None
        self.grid_maze = None
        self.start_spot = None
        self.grid_object = None
        self.cell_open_percentage = cell_open_percentage
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
        self.filename = os.path.join(self.directory, f"algorithms_results_{self.rows}_{cell_open_percentage}.csv")

        # Create CSV file and write the header
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Algorithm_name", "Execution Time (ms)", "Searched Cells", "Total Path Cost"])

        algorithms = {
            "A*": a_star,
            "DIJKSTRA": dijkstra,
            "DFS": dfs,
            "BFS": bfs,
            "BA*": bidirectional_a_star,
            "EBA*": equalized_bidirectional_a_star,
            "DFS_LIM": limited_deep_dfs,
        }

        self.window_handler(algorithms)
        self.analyze_results(rows)

    def generate_maze(self) -> None:
        """
        Generate the maze using the Grid class and initialize start and end spots.
        """
        self.grid_object = Grid(self.rows, self.gap, self.cell_open_percentage)
        self.grid_maze = self.grid_object.grid_maze
        self.start_spot, self.end_spot = self.grid_object.start_spot, self.grid_object.end_spot

    def solv_maze(self, algorithm: Any, **kwargs: Any) -> Tuple[float, int, float]:
        """
        Run a given algorithm and measure its performance.

        Args:
            algorithm (Any): The algorithm to run.
            kwargs (Any): Additional arguments like 'win' and 'heuristic'.

        Returns:
            Tuple[float, int, float]: Execution time, number of visited cells, and total path cost.
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
        return end_time * 1000, len(visited), path_cost

    def window_handler(self, algorithms: Dict[str, Any]) -> None:
        """
        Handle the window setup and execution of algorithms.

        Args:
            algorithms (Dict[str, Any]): Dictionary of algorithms to run.
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

    def run_algorithms_n_times(self, n: int, algorithms: Dict[str, Any], win: Optional[Any]) -> None:
        """
        Run each algorithm 'n' times and log the results.

        Args:
            n (int): Number of times to run each algorithm.
            algorithms (Dict[str, Any]): Dictionary of algorithms to run.
            win (Optional[Any]): Pygame window to draw the grid.
        """
        for i in range(n):
            self.logger.debug(f"{i} iteration running...")
            self.generate_maze()
            if self.window_mode:
                draw_grid(win, self.grid_maze)
            for name, algorithm in algorithms.items():
                self.logger.debug(f'Executing {name} algorithm...\n')
                exec_time, searched, path_cost = self.solv_maze(algorithm, win=win)
                self.logger.debug(f"\n\tExecution_time: {exec_time} ms,"
                                  f"\n\tSearched cells : {searched}"
                                  f"\n\tTotal path cost: {path_cost}\n")
                self.dump_results_into_csv(name, exec_time, searched, path_cost)

    def dump_results_into_csv(self, alg_name: str, exec_time: float, searched: int, path_cost: float) -> None:
        """
        Dump the results of algorithm execution into a CSV file.

        Args:
            alg_name (str): Name of the algorithm.
            exec_time (float): Execution time in ms.
            searched (int): Number of searched cells.
            path_cost (float): Total cost of the path.
        """
        with open(self.filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([alg_name, exec_time, searched, path_cost])

    def analyze_results(self, rows: int) -> None:
        """
        Analyze the results of the algorithms and generate plots.

        Args:
            rows (int): Number of rows in the grid.
        """
        analyze_results_and_generate_plot(self.filename, rows, self.logger, self.show_plot, self.cell_open_percentage)


if __name__ == "__main__":
    display_results = False
    debug_update_draw = False
    show_plt = False

    for size in [MIN_SIZE, MID_SIZE, MAX_SIZE]:
        for cell_open_pct in [25, 5, 0]:
            # Directory for storing CSV and PNG files
            directory_name = f"size{size}_open_cells_pct{cell_open_pct}"
            # Check if the directory exists and remove its contents if it does
            if os.path.exists(directory_name):
                shutil.rmtree(directory_name)
            # Recreate the directory
            os.makedirs(directory_name)

            AlgorithmAnalyzer(rows=size, draw_updates=debug_update_draw, directory=directory_name,
                              window_mode=display_results, show_plot=show_plt, cell_open_percentage=cell_open_pct)
