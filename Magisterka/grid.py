import random
import time
from colorama import Fore, init
from enums.colors import Colors as colors
from spot import Spot
from utils import is_within_bounds


class Grid:
    def __init__(self, rows, gap, print_maze=False):
        self.end_spot = None
        self.start_spot = None
        init()
        self.rows = rows
        self.print_flag = print_maze

        print(f"Maze size: {rows} x {rows}, {rows * rows} cells")
        print(f"Generating maze...")
        time_start = time.time()

        self.grid_maze = [[Spot(y, x, gap, rows, colors.BLACK) for x in range(rows)] for y in range(rows)]
        self.generate_grid_maze()
        print(f"Maze generated in {round(time.time() - time_start, 3)}s\n")
        if self.print_flag:
            self.print_grid_maze_to_console()

    def __repr__(self):
        return '\n'.join([''.join([str(spot) for spot in row]) for row in self.grid_maze])

    def generate_grid_maze(self):
        counter = 0
        start_spot, end_spot = [], []
        while counter < 10:
            counter += 1
            print(f"\tCarving path...")
            time_start = time.time()
            self.carve_path()
            print(f"\tPath carved in {round(time.time() - time_start, 3)}s\n")

            print(f"\tCarving additional paths...")
            time_start = time.time()
            self.carve_additional_passages()
            print(f"\tAdditional paths carved in {round(time.time() - time_start, 3)}s\n")
            self.start_spot, self.end_spot = self.select_start_end_spots()
            print(f"\tStart spot: {start_spot}, end spot: {end_spot}\n")
            self.start_spot.make_start()
            self.end_spot.make_end()

            if self.ensure_path_to_end(self.start_spot, self.end_spot):
                break
            counter += 1
        self.update_all_neighbors()
        self.add_special_spots()

    def carve_path_from_start_recursively(self, cx, cy):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx * 2, cy + dy * 2
            if is_within_bounds(nx, ny, self.rows) and self.grid_maze[nx][ny].color == colors.BLACK:
                self.grid_maze[cx][cy].make_open()
                self.grid_maze[cx + dx][cy + dy].make_open()
                self.grid_maze[nx][ny].make_open()
                self.carve_path_from_start_recursively(nx, ny)

    def carve_path(self):
        stack = [(1, 1)]
        while stack:
            cx, cy = stack.pop()
            directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
            random.shuffle(directions)
            for dx, dy in directions:
                nx, ny = cx + dx * 2, cy + dy * 2
                if is_within_bounds(nx, ny, self.rows) and self.grid_maze[nx][ny].color == colors.BLACK:
                    self.grid_maze[cx][cy].make_open()
                    self.grid_maze[cx + dx][cy + dy].make_open()
                    self.grid_maze[nx][ny].make_open()
                    stack.append((nx, ny))

    def carve_additional_passages(self):
        def has_two_barrier_neighbors_in_line(spot_):
            counter = 0
            spot_.update_barrier_neighbors(self.grid_maze)
            for neighbor in spot_.neighbors:
                if neighbor.is_barrier() and is_within_bounds(neighbor.row, neighbor.col, self.rows):
                    counter += 1
            if counter != 2:
                return False

            neighbors_pos = [neighbor.get_pos() for neighbor in spot_.neighbors]
            if neighbors_pos[0][0] == neighbors_pos[1][0] or neighbors_pos[0][0] == neighbors_pos[0][1]:
                return True
            return False

        barrier_positions = []
        for row in self.grid_maze:
            for spot in row:
                if spot.is_barrier():
                    if is_within_bounds(spot.row, spot.col, self.rows) and has_two_barrier_neighbors_in_line(spot):
                        barrier_positions.append((spot.row, spot.col))

        if len(barrier_positions) != 0:
            new_path_counter = int(len(barrier_positions) * 0.15)
            print(f"\t\t{len(barrier_positions)}")
            print(f"\t\t{new_path_counter}")
            if new_path_counter > 1000:
                new_path_counter = 100
            elif new_path_counter == 0:
                new_path_counter = 1

            selected_positions = random.sample(barrier_positions, new_path_counter)
            for x, y in selected_positions:
                self.grid_maze[x][y].make_open()

    def select_start_end_spots(self):
        grid = [(y, x) for x in range(1, self.rows - 1) for y in range(1, self.rows - 1)]
        start_x, start_y = 0, 0
        end_x, end_y = 0, 0
        while True:
            if self.grid_maze[start_x][start_y].is_barrier():
                start_x, start_y = random.sample(grid, 1)[0]
                grid.remove((start_x, start_y))

            if self.grid_maze[end_x][end_y].is_barrier():
                end_x, end_y = random.sample(grid, 1)[0]
                grid.remove((end_x, end_y))

            if not self.grid_maze[start_x][start_y].is_barrier() and not self.grid_maze[end_x][end_y].is_barrier():
                break
        return self.grid_maze[start_x][start_y], self.grid_maze[end_x][end_y]

    def add_special_spots(self):
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
                        and current_spot != self.end_spot):
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

        if self.rows <= 50:
            region_size = 15
        elif self.rows <= 200:
            region_size = 50
        else:
            region_size = 150

        # Add spots with 10x weight in each quadrant
        for _ in range(2):
            for q in quadrants:
                random_x = random.randint(q[0], q[1] - 1)
                random_y = random.randint(q[2], q[3] - 1)
                start_spot = self.grid_maze[random_x][random_y]
                bfs_change_weight(start_spot, 10, region_size)

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
        for _ in range(2):
            random_x = random.randint(end_quadrant[0], end_quadrant[1] - 1)
            random_y = random.randint(end_quadrant[2], end_quadrant[3] - 1)
            start_spot = self.grid_maze[random_x][random_y]
            bfs_change_weight(start_spot, 25, region_size // 2)
        self.update_all_neighbors()

    def ensure_path_to_end(self, start, end):
        print(f"\tVerifying path...")
        time_start = time.time()
        stack = [start.get_pos()]
        visited = set()
        while stack:
            current = stack.pop()
            if current == end.get_pos():
                print(f"\tPaths verified in {round(time.time() - time_start, 3)}s\n")

                return True
            if current not in visited:
                visited.add(current)
                cx, cy = current
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    nx, ny = cx + dx, cy + dy
                    if (is_within_bounds(nx, ny, self.rows) and
                            self.grid_maze[nx][ny].color in [colors.WHITE_1, colors.PURPLE]):
                        stack.append((nx, ny))

        print('no trace to end')
        return False

    def update_all_neighbors(self):
        print(f"\tUpdating neighbors...")
        time_start = time.time()
        for row in self.grid_maze:
            for spot in row:
                spot.update_neighbors(self.grid_maze)
        print(f"\tNeighbors updated in {round(time.time() - time_start, 3)}s\n")

    def print_grid_maze_to_console(self):
        self.start_spot.make_start()
        self.end_spot.make_end()
        for row in self.grid_maze:
            for spot in row:
                if spot.color == colors.BLACK:
                    print(Fore.RED + 'W ', end="")
                elif spot.color in [colors.WHITE_1, colors.WHITE_10, colors.WHITE_25]:
                    print(Fore.WHITE + 'c ', end="")
                elif spot.color == colors.ORANGE:
                    print(Fore.YELLOW + 'S ', end="")
                elif spot.color == colors.PURPLE:
                    print(Fore.BLUE + 'E ', end="")
                elif spot.color == colors.TURQUOISE:
                    print(Fore.GREEN + 'c ', end="")
                elif spot.color == colors.RED:
                    print(Fore.CYAN + 'v ', end="")
            print(Fore.RESET)  # Reset the color after each line


def main(width, rows):
    if not rows % 2:
        rows += 1
    grid = Grid(rows, width, True)


if __name__ == "__main__":
    main(200, 50)
    print('')
