def a_star(grid_maze, start_spot, end_spot, heuristic=manhattan_heuristic):
    pq = [(0, start_spot)]
    came_from = {}
    g_score = {spot: float('inf') for row in grid_maze for spot in row}
    f_score = {spot: float('inf') for row in grid_maze for spot in row}
    g_score[start_spot] = 0
    f_score[start_spot] = heuristic(start_spot, end_spot)
    visited = set()
    while pq:
        current_f_score, current_spot = heapq.heappop(pq)
        if current_spot == end_spot:
            return reconstruct_path(came_from, start_spot, end_spot)
        visited.add(current_spot)
        for neighbor in current_spot.neighbors:
            tentative_g_score = g_score[current_spot] + neighbor.spot_value
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current_spot
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic(neighbor, end_spot)
                heapq.heappush(pq, (f_score[neighbor], neighbor))
    return []