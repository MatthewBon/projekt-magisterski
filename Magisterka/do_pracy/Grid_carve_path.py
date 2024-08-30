def carve_path(self) -> None:
    dim = self.rows // 2
    self.grid_maze = [[Spot(y, x, self.gap, 2 * dim + 1, colors.BLACK)
                       for x in range(2 * dim + 1)] for y in range(2 * dim + 1)]
    x, y = (0, 0)
    stack = [(x, y)]
    while len(stack) > 0:
        x, y = stack[-1]
        # Define possible directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if ((0 <= nx < dim) and (0 <= ny < dim) and
                    self.grid_maze[2 * nx + 1][2 * ny + 1].is_barrier()):
                self.grid_maze[2 * nx + 1][2 * ny + 1].make_open()
                self.grid_maze[2 * x + 1 + dx][2 * y + 1 + dy].make_open()
                stack.append((nx, ny))
                break
        else:
            stack.pop()