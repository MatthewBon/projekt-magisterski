import random
import time
from typing import Tuple
from logger import ProjectLogger
from algorithms import a_star
from colorama import Fore, init
from enums.colors import Colors as colors
from enums.weight import Weight as spot_weight
from spot import Spot
from utils import is_within_bounds, reset_grid, manhattan_heuristic


class Grid(ProjectLogger):
    def __init__(self, rows: int, gap: int, print_maze: bool = False):
        """
        Initialize the Grid.

        Args:
            rows (int): Number of rows in the grid.
            gap (int): Gap between the spots.
            print_maze (bool): Flag to print the maze to console.
        """
        super().__init__()
        init()
        self.grid_maze = []
        self.end_spot = None
        self.start_spot = None
        self.gap = gap
        self.rows = rows
        self.print_flag = print_maze

        self.logger.info(f"Generating {rows}x{rows} maze...")
        time_start = time.time()
        self.generate_grid_maze()
        self.logger.info(f"Maze generated in {round(time.time() - time_start, 4)}s\n")
        if self.print_flag:
            self.print_grid_maze_to_console()

    def __repr__(self) -> str:
        """
        Return a string representation of the grid maze.

        Returns:
            str: String representation of the grid maze.
        """
        return '\n'.join([''.join([str(spot) for spot in row]) for row in self.grid_maze])

    def generate_grid_maze(self):
        """
        Generate the grid maze with paths and special spots.
        """
        self.logger.debug("Carving path...")
        time_start = time.time()
        self.carve_path()
        self.logger.debug(f"Path carved in {round(time.time() - time_start, 4)}s\n")

        self.logger.debug("Carving additional paths...")
        time_start = time.time()
        self.carve_additional_passages()
        self.logger.debug(f"Additional paths carved in {round(time.time() - time_start, 4)}s\n")

        self.select_start_end_spots()
        self.logger.debug(f"Start spot: {self.start_spot}, End spot: {self.end_spot}\n")

        if not self.ensure_path_to_end():
            raise Exception("Maze generated incorrectly!")
        self.add_special_spots()

    def carve_path(self):
        """
        Carve the main path in the grid maze using a depth-first search approach.
        """
        dim = self.rows // 2
        self.grid_maze = [[Spot(y, x, self.gap, 2*dim+1, colors.BLACK) for x in range(2*dim+1)] for y in range(2*dim+1)]
        x, y = (0, 0)
        stack = [(x, y)]
        while len(stack) > 0:
            x, y = stack[-1]

            # Define possible directions
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
            random.shuffle(directions)

            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                if (0 <= nx < dim) and (0 <= ny < dim) and self.grid_maze[2 * nx + 1][2 * ny + 1].is_barrier():
                    self.grid_maze[2 * nx + 1][2 * ny + 1].make_open()
                    self.grid_maze[2 * x + 1 + dx][2 * y + 1 + dy].make_open()
                    stack.append((nx, ny))
                    break
            else:
                stack.pop()

    def carve_additional_passages(self):
        """
        Carve additional passages in the grid maze to ensure more complex paths.
        """
        def check_neighbors(spot_: Spot) -> bool:
            spot_.update_barrier_neighbors(self.grid_maze)
            if len(spot_.neighbors) > 2:
                return False
            elif len(spot_.neighbors) == 2:
                neighbors_pos = [neighbor.get_pos() for neighbor in spot_.neighbors]
                if neighbors_pos[0][0] == neighbors_pos[1][0] or neighbors_pos[0][1] == neighbors_pos[1][1]:
                    return True
            elif len(spot_.neighbors) == 1:
                return True
            return False

        barrier_positions = []
        for row in self.grid_maze:
            for spot in row:
                if spot.is_barrier():
                    if is_within_bounds(spot.row, spot.col, self.rows) and check_neighbors(spot):
                        barrier_positions.append((spot.row, spot.col))

        if len(barrier_positions) != 0:
            new_path_counter = int(len(barrier_positions) * 0.20)
            if new_path_counter == 0:
                new_path_counter = 1

            selected_positions = random.sample(barrier_positions, new_path_counter)
            for x, y in selected_positions:
                self.grid_maze[x][y].make_open()

    def select_start_end_spots(self):
        """
        Select the start and end spots for the maze ensuring they are in opposite quadrants.
        """
        def select_spot(quadrant: Tuple[int, int, int, int]) -> Spot:
            grid = [(y, x) for x in range(quadrant[0], quadrant[1] - 1) for y in range(quadrant[2], quadrant[3] - 1)]
            x, y = 0, 0
            while True:
                if self.grid_maze[x][y].is_barrier():
                    x, y = random.sample(grid, 1)[0]
                    grid.remove((x, y))
                if not self.grid_maze[x][y].is_barrier():
                    return self.grid_maze[x][y]

        quadrants = [
            (1, self.rows // 2, 1, self.rows // 2),  # Top-left
            (1, self.rows // 2, self.rows // 2, self.rows - 2),  # Top-right
            (self.rows // 2, self.rows - 2, 1, self.rows // 2),  # Bottom-left
            (self.rows // 2, self.rows - 2, self.rows // 2, self.rows - 2)  # Bottom-right
        ]
        opposite_quadrants = {
            0: 3,  # Top-left <-> Bottom-right
            1: 2,  # Top-right <-> Bottom-left
            2: 1,  # Bottom-left <-> Top-right
            3: 0,  # Bottom-right <-> Top-left
        }

        # Select start spot from a random quadrant
        start_quadrant = random.choice(quadrants)
        start_quadrant_index = quadrants.index(start_quadrant)
        self.start_spot = select_spot(start_quadrant)

        # Ensure end spot is in an opposite quadrant
        opposite_quadrant_index = opposite_quadrants[start_quadrant_index]
        end_quadrant = quadrants[opposite_quadrant_index]
        self.end_spot = select_spot(end_quadrant)

        self.start_spot.make_start()
        self.end_spot.make_end()
        self.update_all_neighbors()

    def add_special_spots(self):
        """
        Add special spots with different weights to the maze.
        """
        def bfs_change_weight(s_spot: Spot, new_weight: int, r_size: int):
            queue = [s_spot]
            visited = set()
            counter = 0
            while queue and counter < r_size:
                current_spot = queue.pop(0)
                if current_spot in visited:
                    continue

                visited.add(current_spot)

                if (current_spot.spot_value == 1
                        and current_spot != self.start_spot
                        and current_spot != self.end_spot
                        and not current_spot.is_barrier()):
                    current_spot.spot_value = new_weight
                    current_spot.make_open()
                    counter += 1

                for neighbor in current_spot.neighbors:
                    if neighbor in visited:
                        continue
                    queue.append(neighbor)

        # Define quadrants
        quadrants = [
            (1, self.rows // 2, 1, self.rows // 2),  # Top-left
            (1, self.rows // 2, self.rows // 2, self.rows - 2),  # Top-right
            (self.rows // 2, self.rows - 2, 1, self.rows // 2),  # Bottom-left
            (self.rows // 2, self.rows - 2, self.rows // 2, self.rows - 2)  # Bottom-right
        ]

        region_amount = self.rows // 25
        region_size = self.rows // 2

        # Add spots with 10x weight in each quadrant
        for _ in range(region_amount):
            for q in quadrants:
                random_x = random.randint(q[0], q[1] - 1)
                random_y = random.randint(q[2], q[3] - 1)
                start_spot = self.grid_maze[random_x][random_y]
                bfs_change_weight(start_spot, spot_weight.LIGHT.value, region_size)

        # Determine the quadrant of the end spot
        end_row, end_col = self.end_spot.get_pos()
        if end_row < self.rows // 2:
            if end_col < self.rows // 2:
                end_quadrant = (1, self.rows // 2, 1, self.rows // 2)  # Top-left
            else:
                end_quadrant = (1, self.rows // 2, self.rows // 2, self.rows - 2)  # Top-right
        else:
            if end_col < self.rows // 2:
                end_quadrant = (self.rows // 2, self.rows - 2, 1, self.rows // 2)  # Bottom-left
            else:
                end_quadrant = (self.rows // 2, self.rows - 2, self.rows // 2, self.rows - 2)  # Bottom-right
        for _ in range(region_amount):
            random_x = random.randint(end_quadrant[0], end_quadrant[1] - 1)
            random_y = random.randint(end_quadrant[2], end_quadrant[3] - 1)
            start_spot = self.grid_maze[random_x][random_y]
            bfs_change_weight(start_spot, spot_weight.HEAVY.value, region_size // 2)

    def ensure_path_to_end(self) -> bool:
        """
        Ensure there is a valid path from the start spot to the end spot.

        Returns:
            bool: True if a valid path exists, False otherwise.
        """
        self.logger.debug("Verifying path...")
        path, _ = a_star(self.grid_maze, self.start_spot, self.end_spot, window_mode=False,
                         heuristic_method=manhattan_heuristic)
        if not len(path) > 0:
            self.logger.error('No trace to end')
            self.print_grid_maze_to_console()
            return False
        reset_grid(self.grid_maze, window_mode=False)
        return True

    def update_all_neighbors(self):
        """
        Update neighbors for all spots in the grid maze.
        """
        self.logger.debug("Updating neighbors...")
        time_start = time.time()
        for row in self.grid_maze:
            for spot in row:
                spot.update_open_neighbors(self.grid_maze)
        self.logger.debug(f"Neighbors updated in {round(time.time() - time_start, 4)}s\n")

    def print_grid_maze_to_console(self):
        """
        Print the grid maze to the console.
        """
        for row in self.grid_maze:
            for spot in row:
                if spot.color == colors.BLACK:
                    print(Fore.RED + 'W ', end="")
                elif spot.color in [colors.WHITE_1, colors.WHITE_15, colors.WHITE_15]:
                    print(Fore.WHITE + 'c ', end="")
                elif spot.color == colors.ORANGE:
                    print(Fore.CYAN + 'S ', end="")
                elif spot.color == colors.PURPLE:
                    print(Fore.BLUE + 'E ', end="")
                elif spot.color == colors.TURQUOISE:
                    print(Fore.GREEN + 'c ', end="")
                elif spot.color == colors.RED:
                    print(Fore.YELLOW + 'v ', end="")
            print(Fore.RESET)  # Reset the color after each line