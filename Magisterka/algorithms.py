import heapq
from typing import List
from spot import Spot
from utils import heuristic, reconstruct_path, draw_spot


def a_star(grid_maze: List[List[Spot]], start_spot: Spot, end_spot: Spot, win=None, draw_updates=True, window_mode=True):
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
            if draw_updates and window_mode:
                draw_spot(win=win, spot=current_spot)

        if current_spot == end_spot:
            while current_spot:
                path.append(current_spot)
                current_spot = came_from[current_spot]
            path.reverse()
            reconstruct_path(path, grid_maze, start_spot, end_spot, draw_updates, win, window_mode=window_mode)
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
                    if draw_updates and window_mode:
                        draw_spot(win=win, spot=neighbor)

    return [], visited


def dijkstra(grid_maze: List[List[Spot]], start_spot: Spot, end_spot: Spot, win=None, draw_updates=True, window_mode=True):
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
            if draw_updates and window_mode:
                draw_spot(win=win, spot=current_spot)

        if current_spot == end_spot:
            current = end_spot
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            path.reverse()
            reconstruct_path(path, grid_maze, start_spot, end_spot, draw_updates, win, window_mode=window_mode)
            return path, visited

        for neighbor in current_spot.neighbors:
            distance = current_distance + current_spot.spot_value
            if distance < g_score[neighbor]:
                g_score[neighbor] = distance
                came_from[neighbor] = current_spot
                heapq.heappush(pq, (distance, neighbor))
                if neighbor != start_spot and neighbor != end_spot:
                    neighbor.mark_next()
                    if draw_updates and window_mode:
                        draw_spot(win=win, spot=neighbor)

    return [], visited


def limited_deep_dfs(grid_maze: List[List[Spot]], start_spot: Spot, end_spot: Spot,
                     win=None, draw_updates=True, window_mode=True):
    path = []
    stack = [(start_spot, path)]  # Stack of (Spot, path)
    visited = set()
    deep_limit = 100
    ctr = 0
    while stack:
        if len(path) > deep_limit:
            deep_limit += int(deep_limit * 0.2)
            ctr += 1
            current_spot, path = stack.pop(0)
        else:
            current_spot, path = stack.pop()

        if current_spot in visited:
            continue
        visited.add(current_spot)
        if current_spot != start_spot and current_spot != end_spot:
            current_spot.make_closed()
            if draw_updates and window_mode:
                draw_spot(win=win, spot=current_spot)
        # path = path + [current_spot]

        if current_spot == end_spot:
            # print(deep_limit, ctr)
            # reconstruct_path(path, grid_maze, start_spot, end_spot, draw_updates, win, window_mode=window_mode)
            return path, visited

        for neighbor in current_spot.neighbors:
            if neighbor in visited:
                continue
            stack.append((neighbor, path))
            if neighbor != start_spot and neighbor != end_spot:
                neighbor.mark_next()
                if draw_updates and window_mode:
                    draw_spot(win=win, spot=neighbor)
            if neighbor == end_spot:
                break

    return [], visited


def bfs(grid_maze: List[List[Spot]], start_spot: Spot, end_spot: Spot, win=None, draw_updates=True, window_mode=True):
    queue = [(start_spot, [])]  # Stack of (Spot, path)
    visited = set()
    while queue:
        current_spot, path = queue.pop(0)
        if current_spot in visited:
            continue
        visited.add(current_spot)
        if current_spot != start_spot and current_spot != end_spot:
            current_spot.make_closed()
            if draw_updates and window_mode:
                draw_spot(win=win, spot=current_spot)
        path = path + [current_spot]

        if current_spot == end_spot:
            reconstruct_path(path, grid_maze, start_spot, end_spot, draw_updates, win, window_mode=window_mode)
            return path, visited

        for neighbor in current_spot.neighbors:
            if neighbor in visited:
                continue
            queue.append((neighbor, path))
            if neighbor != start_spot and neighbor != end_spot:
                neighbor.mark_next()
                if draw_updates and window_mode:
                    draw_spot(win=win, spot=neighbor)
            if neighbor == end_spot:
                queue.insert(0, (neighbor, path))
                break

    return [], visited


def bfs_no_path(grid_maze: List[List[Spot]], start_spot: Spot, end_spot: Spot, win=None, draw_updates=True, window_mode=True):
    queue = [(start_spot, [])]  # Stack of (Spot, path)
    visited = set()
    while queue:
        current_spot, path = queue.pop(0)
        if current_spot in visited:
            continue
        visited.add(current_spot)
        if current_spot != start_spot and current_spot != end_spot:
            current_spot.make_closed()
            if draw_updates and window_mode:
                draw_spot(win=win, spot=current_spot)
        #path = path + [current_spot]

        if current_spot == end_spot:
            #reconstruct_path(path, grid_maze, start_spot, end_spot, draw_updates, win, window_mode=window_mode)
            return path, visited

        for neighbor in current_spot.neighbors:
            if neighbor in visited:
                continue
            queue.append((neighbor, path))
            if neighbor != start_spot and neighbor != end_spot:
                neighbor.mark_next()
                if draw_updates and window_mode:
                    draw_spot(win=win, spot=neighbor)
            if neighbor == end_spot:
                queue.insert(0, (neighbor, path))
                break

    return [], visited
