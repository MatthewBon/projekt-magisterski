import random
from colorama import Fore, init
from enums.colors import Colors as colors
from spot import Spot
from utils import calculate_blocks


class Grid:
    def __init__(self, rows, gap, print_maze=False):
        self.rows = rows
        self.grid_maze = [[Spot(y, x, gap, rows, colors.BLACK) for x in range(rows)] for y in range(rows)]
        self._start = (1, 1)
        self._end = (rows - 2, rows - 2)

        self.start_spot, self.end_spot = self.generate_grid_maze()
        self.update_all_neighbors()
        if print_maze:
            self.print_grid_maze_to_console()

    def __repr__(self):
        return '\n'.join([''.join([str(spot) for spot in row]) for row in self.grid_maze])

    def generate_grid_maze(self):
        counter = 0

        while counter < 10:
            counter += 1
            self.carve_path_from_start_to_end(self._start[0], self._start[1])
            self.carve_additional_passages()
            self.grid_maze[self._start[0]][self._start[1]].make_start()
            self.grid_maze[self._end[0]][self._end[1]].make_end()
            if self.ensure_path_to_end((self._start[0], self._start[1]), (self._end[0], self._end[1])):
                break

        return self.grid_maze[self._start[0]][self._start[1]], self.grid_maze[self._end[0]][self._end[1]]

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

    def carve_path_from_start_to_end(self, start_cx, start_cy):
        stack = [(start_cx, start_cy)]
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

        barrier_counter = calculate_blocks(self.grid_maze, colors.BLACK)
        barrier_without_frame = barrier_counter - (len(self.grid_maze) * 4)
        new_path_counter = int(barrier_without_frame * 0.01) + 2
        barrier_positions = []
        for row in self.grid_maze:
            for spot in row:
                if spot.is_barrier():
                    if self.is_within_bounds(spot.row, spot.col) and has_two_barrier_neighbors_in_line(spot):
                        barrier_positions.append((spot.row, spot.col))

        selected_positions = random.sample(barrier_positions, new_path_counter)

        for x, y in selected_positions:
            self.grid_maze[x][y].make_open()

    def ensure_path_to_end(self, start, end):
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
                    if (self.is_within_bounds(nx, ny) and
                            self.grid_maze[nx][ny].color in [colors.WHITE, colors.PURPLE]):
                        stack.append((nx, ny))

        print('no trace to end')
        return False

    def update_all_neighbors(self):
        for row in self.grid_maze:
            for spot in row:
                spot.update_neighbors(self.grid_maze)

    def print_grid_maze_to_console(self):
        init()
        print('\n')
        for row in self.grid_maze:
            for spot in row:
                if spot.color == colors.BLACK:
                    print(Fore.RED + 'w ', end="")
                elif spot.color == colors.WHITE:
                    print(Fore.WHITE + 'c ', end="")
                elif spot.color == colors.ORANGE:
                    print(Fore.YELLOW + 's ', end="")
                elif spot.color == colors.PURPLE:
                    print(Fore.BLUE + 'e ', end="")
                elif spot.color == colors.RED:
                    print(Fore.GREEN + 'c ', end="")
            print(Fore.RESET)  # Reset the color after each line

    def is_within_bounds(self, x, y):
        return 0 < x < self.rows - 1 and 0 < y < self.rows - 1


def main(width, rows):
    if not rows % 2:
        rows += 1
    Grid(rows, width)


if __name__ == "__main__":
    main(200, 1000)
