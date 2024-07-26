import heapq
import random
import sys
import time
from colorama import Fore, init
from enums.colors import Colors as colors
from spot import Spot
from utils import calculate_blocks


class Grid:
    def __init__(self, rows, gap, print_maze=False):
        init()
        self.rows = rows
        self._start = (1, 1)
        self._end = (rows - 2, rows - 2)

        print(f"Maze size: {rows} x {rows}, {rows * rows} cells")
        print(f"Generating maze...")
        time_start = time.time()

        self.grid_maze = [[Spot(y, x, gap, rows, colors.BLACK) for x in range(rows)] for y in range(rows)]
        self.start_spot, self.end_spot = self.generate_grid_maze()
        self.update_all_neighbors()

        print(f"Maze generated in {round(time.time() - time_start, 3)}s\n")
        if print_maze:
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

            start_spot, end_spot = self.select_start_end_spots()
            start_spot.make_start()
            end_spot.make_end()

            if self.ensure_path_to_end(start_spot, end_spot):
                break
            counter += 1

        return start_spot, end_spot

    def carve_path_from_start_recursively(self, cx, cy):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx * 2, cy + dy * 2
            if self.is_within_bounds(nx, ny) and self.grid_maze[nx][ny].color == colors.BLACK:
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
                if self.is_within_bounds(nx, ny) and self.grid_maze[nx][ny].color == colors.BLACK:
                    self.grid_maze[cx][cy].make_open()
                    self.grid_maze[cx + dx][cy + dy].make_open()
                    self.grid_maze[nx][ny].make_open()
                    stack.append((nx, ny))

    def carve_additional_passages(self):
        def has_two_barrier_neighbors_in_line(spot_):
            counter = 0
            spot_.update_barrier_neighbors(self.grid_maze)
            for neighbor in spot_.neighbors:
                if neighbor.is_barrier() and self.is_within_bounds(neighbor.row, neighbor.col):
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
                    if self.is_within_bounds(spot.row, spot.col) and has_two_barrier_neighbors_in_line(spot):
                        barrier_positions.append((spot.row, spot.col))

        if len(barrier_positions) != 0:
            new_path_counter = int(len(barrier_positions) * 0.0001)
            print(f"\t\t{new_path_counter}")
            if new_path_counter > 1000:
                new_path_counter = 100
            elif new_path_counter == 0:
                new_path_counter = 1

            selected_positions = random.sample(barrier_positions, new_path_counter)
            for x, y in selected_positions:
                self.grid_maze[x][y].make_open()

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
                    if (self.is_within_bounds(nx, ny) and
                            self.grid_maze[nx][ny].color in [colors.WHITE, colors.PURPLE]):
                        stack.append((nx, ny))

        print('no trace to end')
        return False

    def select_start_end_spots(self):
        grid = [(y, x) for x in range(1, self.rows - 1) for y in range(1, self.rows - 1)]
        print(grid)
        start_x, start_y = 0, 0
        end_x, end_y = 0, 0
        while True:
            if self.grid_maze[start_x][start_y].is_barrier():
                start_x, start_y = random.sample(grid, 1)[0]
                grid.remove((start_x, start_y))
                print(grid)

            if self.grid_maze[end_x][end_y].is_barrier():
                end_x, end_y = random.sample(grid, 1)[0]
                grid.remove((end_x, end_y))
                print(grid)

            if not self.grid_maze[start_x][start_y].is_barrier() and not self.grid_maze[end_x][end_y].is_barrier():
                if abs(start_x - end_x) > 1 and abs(start_y - end_y) > 1:
                    break
        return self.grid_maze[start_x][start_y], self.grid_maze[end_x][end_y]

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
                elif spot.color == colors.WHITE:
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

    def is_within_bounds(self, x, y):
        return 0 < x < self.rows - 1 and 0 < y < self.rows - 1

    def dijkstra(self):
        print("Running Dijkstra's Algorithm...")
        start = self.start_spot
        end = self.end_spot
        pq = [(0, start)]  # Priority queue of (distance, Spot)
        distances = {spot: float('inf') for row in self.grid_maze for spot in row}
        distances[start] = 0
        came_from = {spot: None for row in self.grid_maze for spot in row}

        while pq:
            current_distance, current_spot = heapq.heappop(pq)
            current_spot.make_closed()

            if current_spot == end:
                print("End spot reached!")
                break

            for neighbor in current_spot.neighbors:
                if neighbor.is_barrier():
                    continue
                distance = current_distance + 1  # Assuming each edge has a weight of 1

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    came_from[neighbor] = current_spot
                    heapq.heappush(pq, (distance, neighbor))

        current = end
        path = []
        while current:
            path.append(current)
            current = came_from[current]
        path.reverse()
        self.reconstruct_path_from_path(path)

    def dfs(self):
        print("Running DFS...")
        start = self.start_spot
        end = self.end_spot
        stack = [(start, [])]  # Stack of (Spot, path)
        visited = set()

        while stack:
            current_spot, path = stack.pop()
            current_spot.make_closed()
            if current_spot in visited:
                continue
            visited.add(current_spot)
            path = path + [current_spot]

            if current_spot == end:
                print("End spot reached!")
                self.reconstruct_path_from_path(path)
                return

            for neighbor in current_spot.neighbors:
                if neighbor.is_barrier() or neighbor in visited:
                    continue
                stack.append((neighbor, path))

    def bfs(self):
        print("Running BFS...")
        start = self.start_spot
        end = self.end_spot
        queue = [(start, [])]  # Queue of (Spot, path)
        visited = set()

        while queue:
            current_spot, path = queue.pop(0)
            if current_spot in visited:
                continue
            visited.add(current_spot)
            path = path + [current_spot]
            current_spot.make_closed()
            if current_spot == end:
                print("End spot reached!")
                self.reconstruct_path_from_path(path)
                return

            for neighbor in current_spot.neighbors:
                if neighbor.is_barrier() or neighbor in visited:
                    continue
                queue.append((neighbor, path))

    def reconstruct_path_from_path(self, path):
        print("Path found:")
        for spot in path:
            if spot != self.start_spot and spot != self.end_spot:
                spot.make_path()
        self.print_grid_maze_to_console()
        for spot in path:
            if spot != self.start_spot and spot != self.end_spot:
                spot.make_open()


def main(width, rows):
    if not rows % 2:
        rows += 1
    grid = Grid(rows, width, True)
    grid.dijkstra()  # Run Dijkstra's algorithm
    grid.dfs()       # Run DFS algorithm
    grid.bfs()       # Run BFS algorithm


if __name__ == "__main__":
    main(200, 25)
    print('')
