class Grid:
    def __init__(self, rows: int, gap: int,
                 print_maze: bool = False):
        self.grid_maze = []
        self.end_spot = None
        self.start_spot = None
        self.gap = gap
        self.rows = rows
        self.print_flag = print_maze
        self.generate_grid_maze()