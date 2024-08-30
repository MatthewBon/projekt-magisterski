def dfs(grid_maze, start_spot, end_spot):
    stack = [(start_spot, None)]
    visited = set()
    came_from = {}
    while stack:
        current_spot, prev = stack.pop()
        if current_spot not in visited:
            visited.add(current_spot)
            came_from[current_spot] = prev
            if current_spot == end_spot:
                return reconstruct_path(came_from, start_spot, end_spot)
            for neighbor in current_spot.neighbors:
                if neighbor not in visited:
                    stack.append((neighbor, current_spot))
    return []