def generate_grid_maze(self) -> None:
    self.carve_path()
    self.carve_additional_passages()
    self.select_start_end_spots()
    if not self.ensure_path_to_end():
        raise Exception("Error")
    self.add_special_spots()