def bfs(grid_maze, start_spot, end_spot):
    queue = [(start_spot, None)]
    visited = set()
    came_from = {}
    while queue:
        current_spot, prev = queue.pop(0)
        if current_spot not in visited:
            visited.add(current_spot)
            came_from[current_spot] = prev
            if current_spot == end_spot:
                return reconstruct_path(came_from, start_spot, end_spot)
            for neighbor in current_spot.neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, current_spot))
    return []