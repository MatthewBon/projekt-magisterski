def dijkstra(grid_maze, start_spot, end_spot):
    pq = [(0, start_spot)]
    came_from = {}
    g_score = {spot: float('inf') for row in grid_maze for spot in row}
    g_score[start_spot] = 0
    visited = set()
    while pq:
        current_g_score, current_spot = heapq.heappop(pq)
        if current_spot == end_spot:
            return reconstruct_path(came_from, start_spot, end_spot)
        visited.add(current_spot)
        for neighbor in current_spot.neighbors:
            tentative_g_score = current_g_score + neighbor.spot_value
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current_spot
                g_score[neighbor] = tentative_g_score
                heapq.heappush(pq, (tentative_g_score, neighbor))
    return []