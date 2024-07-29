import heapq
from typing import Callable, List
from spot import Spot
from utils import heuristic, reconstruct_path, calculate_blocks


def a_star(grid_maze: List[List[Spot]], start_spot: Spot, end_spot: Spot, draw_progress_method: Callable, win):
    pq = [(0, start_spot)]  # Priority queue of (f_score, Spot)
    visited = set()
    path = []
    g_score = {spot: float("inf") for row in grid_maze for spot in row}
    g_score[start_spot] = 0
    f_score = {spot: float("inf") for row in grid_maze for spot in row}
    f_score[start_spot] = heuristic(start_spot.get_pos(), end_spot.get_pos())
    came_from = {spot: None for row in grid_maze for spot in row}

    while pq:
        current_f_score, current_spot = heapq.heappop(pq)
        if current_spot in visited:
            continue
        visited.add(current_spot)
        if current_spot != start_spot and current_spot != end_spot:
            current_spot.make_closed()
            draw_progress_method(win=win, spot=current_spot)

        if current_spot == end_spot:
            print("End spot reached!")

            while current_spot:
                path.append(current_spot)
                current_spot = came_from[current_spot]
            path.reverse()
            reconstruct_path(path, start_spot, end_spot, draw_progress_method, win)

            return path, visited

        for neighbor in current_spot.neighbors:
            if neighbor in visited:
                continue
            temp_g_score = g_score[current_spot] + current_spot.spot_value

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current_spot
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end_spot.get_pos())
                heapq.heappush(pq, (f_score[neighbor], neighbor))

                if neighbor != start_spot and neighbor != end_spot:
                    neighbor.mark_next()
                    draw_progress_method(win=win, spot=neighbor)

    return [], visited


def dijkstra(grid_maze, start_spot, end_spot, draw_progress_method: Callable, win):
    pq = [(0, start_spot)]  # Priority queue of (distance, Spot)
    g_score = {spot: float('inf') for row in grid_maze for spot in row}
    g_score[start_spot] = 0
    visited = set()
    came_from = {spot: None for row in grid_maze for spot in row}

    while pq:

        current_distance, current_spot = heapq.heappop(pq)
        if current_spot in visited:
            continue
        visited.add(current_spot)

        if current_spot != start_spot and current_spot != end_spot:
            current_spot.make_closed()
            draw_progress_method(win=win, spot=current_spot)

        if current_spot == end_spot:
            print("End spot reached!")
            current = end_spot
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            path.reverse()
            reconstruct_path(path, start_spot, end_spot, draw_progress_method, win)
            return path, visited

        for neighbor in current_spot.neighbors:
            distance = current_distance + current_spot.spot_value
            if distance < g_score[neighbor]:
                g_score[neighbor] = distance
                came_from[neighbor] = current_spot
                heapq.heappush(pq, (distance, neighbor))
                if neighbor != start_spot and neighbor != end_spot:
                    neighbor.mark_next()
                    draw_progress_method(win=win, spot=neighbor)

    return [], visited


def dfs(grid, start_spot, end_spot, draw_progress_method: Callable, win):
    print("Running DFS...")
    stack = [(start_spot, [])]  # Stack of (Spot, path)
    visited = set()

    while stack:
        current_spot, path = stack.pop()
        if current_spot in visited:
            continue
        visited.add(current_spot)
        if current_spot != start_spot and current_spot != end_spot:
            current_spot.make_closed()
            draw_progress_method(win=win, spot=current_spot)

        path = path + [current_spot]

        if current_spot == end_spot:
            print("End spot reached!")
            reconstruct_path(path, start_spot, end_spot, draw_progress_method, win)
            return path, visited

        for neighbor in current_spot.neighbors:
            if neighbor in visited:
                continue
            stack.append((neighbor, path))
            if neighbor != start_spot and neighbor != end_spot:
                neighbor.mark_next()
                draw_progress_method(win=win, spot=neighbor)
            if neighbor == end_spot:
                break

    return [], visited


def bfs(grid, start_spot, end_spot, draw_progress_method: Callable, win):
    print("Running BFS...")
    queue = [(start_spot, [])]  # Stack of (Spot, path)
    visited = set()

    while queue:
        current_spot, path = queue.pop(0)
        if current_spot in visited:
            continue
        visited.add(current_spot)
        if current_spot != start_spot and current_spot != end_spot:
            current_spot.make_closed()
            draw_progress_method(win=win, spot=current_spot)

        path = path + [current_spot]

        if current_spot == end_spot:
            print("End spot reached!")
            reconstruct_path(path, start_spot, end_spot, draw_progress_method, win)
            return path, visited

        for neighbor in current_spot.neighbors:
            if neighbor in visited:
                continue
            queue.append((neighbor, path))
            if neighbor != start_spot and neighbor != end_spot:
                neighbor.mark_next()
                draw_progress_method(win=win, spot=neighbor)
            if neighbor == end_spot:
                queue.insert(0, (neighbor, path))
                break

    return [], visited

