import heapq
from typing import List, Tuple, Set
from spot import Spot
from utils import reconstruct_path, draw_spot, manhattan_heuristic


def a_star(grid_maze: List[List[Spot]], start_spot: Spot, end_spot: Spot, **kwargs) -> Tuple[List[Spot], Set[Spot]]:
    """
    Perform the A* search algorithm to find the shortest path from the start spot to the end spot.

    Args:
        grid_maze (List[List[Spot]]): The grid maze containing all the spots.
        start_spot (Spot): The starting spot of the search.
        end_spot (Spot): The ending spot of the search.
        kwargs: Additional optional arguments like 'win' (Pygame window), 'draw_updates' (whether to draw updates),
                'window_mode' (whether to display in windowed mode), and 'heuristic_method' (method to calculate the heuristic).

    Returns:
        Tuple[List[Spot], Set[Spot]]: A tuple containing the path from start to end and the set of visited spots.
    """
    win = kwargs.get('win')
    draw_updates = kwargs.get('draw_updates', True)
    window_mode = kwargs.get('window_mode', True)

    pq = [(0, start_spot)]  # Priority queue initialized with the start spot
    visited = set()
    path = []

    g_score = {spot: float("inf") for row in grid_maze for spot in row}  # Initialize g_scores with infinity
    g_score[start_spot] = 0
    f_score = {spot: float("inf") for row in grid_maze for spot in row}  # Initialize f_scores with infinity
    f_score[start_spot] = manhattan_heuristic(start_spot, end_spot)  # Set the f_score of the start spot

    came_from = {spot: None for row in grid_maze for spot in row}  # Track the most efficient path

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

        __explore_neighbours(pq, current_spot, came_from, visited, g_score, f_score, end_spot, start_spot,
                             draw_updates, window_mode, win)

    return [], visited


def equalized_bidirectional_a_star(grid_maze: List[List[Spot]], start_spot: Spot, end_spot: Spot, **kwargs) -> Tuple[List[Spot], Set[Spot]]:
    """
    Perform the equalized bidirectional A* search algorithm from both the start and end spots simultaneously.

    Args:
        grid_maze (List[List[Spot]]): The grid maze containing all the spots.
        start_spot (Spot): The starting spot of the search.
        end_spot (Spot): The ending spot of the search.
        kwargs: Additional optional arguments like 'win', 'draw_updates', 'window_mode', and 'heuristic_method'.

    Returns:
        Tuple[List[Spot], Set[Spot]]: A tuple containing the path from start to end and the set of visited spots.
    """
    win = kwargs.get('win')
    draw_updates = kwargs.get('draw_updates', True)
    window_mode = kwargs.get('window_mode', True)

    pq_start = [(0, start_spot)]  # Priority queue for the start search
    pq_end = [(0, end_spot)]  # Priority queue for the end search

    visited_start = set()
    visited_end = set()
    path = []

    g_score_start = {spot: float("inf") for row in grid_maze for spot in row}
    g_score_end = {spot: float("inf") for row in grid_maze for spot in row}
    g_score_start[start_spot] = 0
    g_score_end[end_spot] = 0

    f_score_start = {spot: float("inf") for row in grid_maze for spot in row}
    f_score_end = {spot: float("inf") for row in grid_maze for spot in row}
    f_score_start[start_spot] = manhattan_heuristic(start_spot, end_spot)
    f_score_end[end_spot] = manhattan_heuristic(end_spot, start_spot)

    came_from_start = {spot: None for row in grid_maze for spot in row}
    came_from_end = {spot: None for row in grid_maze for spot in row}

    while pq_start and pq_end:
        if len(pq_start) <= len(pq_end):
            current_f_score_start, current_spot_start = heapq.heappop(pq_start)

            if current_spot_start in visited_start:
                continue
            visited_start.add(current_spot_start)

            if current_spot_start != start_spot and current_spot_start != end_spot:
                current_spot_start.make_closed()
                if draw_updates and window_mode:
                    draw_spot(win=win, spot=current_spot_start)

            if current_spot_start in visited_end:
                path = __reconstruct_bidirectional_path(current_spot_start, came_from_start, came_from_end)
                reconstruct_path(path, grid_maze, start_spot, end_spot, draw_updates, win, window_mode=window_mode)
                return path, visited_start.union(visited_end)

            __explore_neighbours(pq_start, current_spot_start, came_from_start, visited_start,
                                 g_score_start, f_score_start, end_spot, start_spot,
                                 draw_updates, window_mode, win)
        else:
            current_f_score_end, current_spot_end = heapq.heappop(pq_end)

            if current_spot_end in visited_end:
                continue
            visited_end.add(current_spot_end)

            if current_spot_end != start_spot and current_spot_end != end_spot:
                current_spot_end.make_closed()
                if draw_updates and window_mode:
                    draw_spot(win=win, spot=current_spot_end)

            if current_spot_end in visited_start:
                path = __reconstruct_bidirectional_path(current_spot_end, came_from_start, came_from_end)
                reconstruct_path(path, grid_maze, start_spot, end_spot, draw_updates, win, window_mode=window_mode)
                return path, visited_start.union(visited_end)

            __explore_neighbours(pq_end, current_spot_end, came_from_end, visited_end,
                                 g_score_end, f_score_end, end_spot, start_spot,
                                 draw_updates, window_mode, win)

    return [], visited_start.union(visited_end)


def bidirectional_a_star(grid_maze: List[List[Spot]], start_spot: Spot, end_spot: Spot, **kwargs) -> Tuple[List[Spot], Set[Spot]]:
    """
    Perform the bidirectional A* search algorithm from both the start and end spots simultaneously.

    Args:
        grid_maze (List[List[Spot]]): The grid maze containing all the spots.
        start_spot (Spot): The starting spot of the search.
        end_spot (Spot): The ending spot of the search.
        kwargs: Additional optional arguments like 'win', 'draw_updates', 'window_mode', and 'heuristic_method'.

    Returns:
        Tuple[List[Spot], Set[Spot]]: A tuple containing the path from start to end and the set of visited spots.
    """
    win = kwargs.get('win')
    draw_updates = kwargs.get('draw_updates', True)
    window_mode = kwargs.get('window_mode', True)

    pq_start = [(0, start_spot)]  # Priority queue for the start search
    pq_end = [(0, end_spot)]  # Priority queue for the end search

    visited_start = set()
    visited_end = set()
    path = []

    g_score_start = {spot: float("inf") for row in grid_maze for spot in row}
    g_score_end = {spot: float("inf") for row in grid_maze for spot in row}
    g_score_start[start_spot] = 0
    g_score_end[end_spot] = 0

    f_score_start = {spot: float("inf") for row in grid_maze for spot in row}
    f_score_end = {spot: float("inf") for row in grid_maze for spot in row}
    f_score_start[start_spot] = manhattan_heuristic(start_spot, end_spot)
    f_score_end[end_spot] = manhattan_heuristic(end_spot, start_spot)

    came_from_start = {spot: None for row in grid_maze for spot in row}
    came_from_end = {spot: None for row in grid_maze for spot in row}

    while pq_start and pq_end:
        current_f_score_start, current_spot_start = heapq.heappop(pq_start)

        if current_spot_start in visited_start:
            continue
        visited_start.add(current_spot_start)

        if current_spot_start != start_spot and current_spot_start != end_spot:
            current_spot_start.make_closed()
            if draw_updates and window_mode:
                draw_spot(win=win, spot=current_spot_start)

        if current_spot_start in visited_end:
            path = __reconstruct_bidirectional_path(current_spot_start, came_from_start, came_from_end)
            reconstruct_path(path, grid_maze, start_spot, end_spot, draw_updates, win, window_mode=window_mode)
            return path, visited_start.union(visited_end)

        __explore_neighbours(pq_start, current_spot_start, came_from_start, visited_start, g_score_start, f_score_start,
                             end_spot, start_spot, draw_updates, window_mode, win)

        current_f_score_end, current_spot_end = heapq.heappop(pq_end)

        if current_spot_end in visited_end:
            continue
        visited_end.add(current_spot_end)

        if current_spot_end != start_spot and current_spot_end != end_spot:
            current_spot_end.make_closed()
            if draw_updates and window_mode:
                draw_spot(win=win, spot=current_spot_end)

        if current_spot_end in visited_start:
            path = __reconstruct_bidirectional_path(current_spot_end, came_from_start, came_from_end)
            reconstruct_path(path, grid_maze, start_spot, end_spot, draw_updates, win, window_mode=window_mode)
            return path, visited_start.union(visited_end)

        __explore_neighbours(pq_end, current_spot_end, came_from_end, visited_end, g_score_end, f_score_end,
                             end_spot, start_spot, draw_updates, window_mode, win)

    return [], visited_start.union(visited_end)


def dijkstra(grid_maze: List[List[Spot]], start_spot: Spot, end_spot: Spot, **kwargs) -> Tuple[List[Spot], Set[Spot]]:
    """
    Perform Dijkstra's algorithm to find the shortest path from the start spot to the end spot.

    Args:
        grid_maze (List[List[Spot]]): The grid maze containing all the spots.
        start_spot (Spot): The starting spot of the search.
        end_spot (Spot): The ending spot of the search.
        kwargs: Additional optional arguments like 'win', 'draw_updates', and 'window_mode'.

    Returns:
        Tuple[List[Spot], Set[Spot]]: A tuple containing the path from start to end and the set of visited spots.
    """
    win = kwargs.get('win')
    draw_updates = kwargs.get('draw_updates', True)
    window_mode = kwargs.get('window_mode', True)

    pq = [(0, start_spot)]  # Priority queue initialized with the start spot

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
            distance = current_distance + neighbor.spot_value
            if distance < g_score[neighbor]:
                g_score[neighbor] = distance
                came_from[neighbor] = current_spot
                heapq.heappush(pq, (distance, neighbor))
                if neighbor != start_spot and neighbor != end_spot:
                    neighbor.make_next()
                    if draw_updates and window_mode:
                        draw_spot(win=win, spot=neighbor)

    return [], visited


def limited_deep_dfs(grid_maze: List[List[Spot]], start_spot: Spot, end_spot: Spot, **kwargs) -> Tuple[List[Spot], Set[Spot]]:
    """
    Perform the limited depth-first search (DFS) algorithm with a dynamic depth limit.

    Args:
        grid_maze (List[List[Spot]]): The grid maze containing all the spots.
        start_spot (Spot): The starting spot of the search.
        end_spot (Spot): The ending spot of the search.
        kwargs: Additional optional arguments like 'win', 'draw_updates', and 'window_mode'.

    Returns:
        Tuple[List[Spot], Set[Spot]]: A tuple containing the path from start to end and the set of visited spots.
    """
    win = kwargs.get('win')
    draw_updates = kwargs.get('draw_updates', True)
    window_mode = kwargs.get('window_mode', True)

    depth = 0
    stack = [(start_spot, None)]  # Stack initialized with the start spot
    visited = set()
    came_from = {spot: None for row in grid_maze for spot in row}
    path = []
    depth_limit = len(grid_maze[0]) // 2  # Initial depth limit

    while stack:
        depth += 1
        if depth < depth_limit:
            current_spot, prev = stack.pop()
        else:
            current_spot, prev = stack.pop(0)
            depth = 0
            depth_limit += int(depth_limit * 0.1)  # Increase depth limit by 10%

        if current_spot not in visited:
            visited.add(current_spot)
            came_from[current_spot] = prev

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
                if neighbor not in visited:
                    stack.append((neighbor, current_spot))
                    if neighbor != start_spot and neighbor != end_spot:
                        neighbor.make_next()
                        if draw_updates and window_mode:
                            draw_spot(win=win, spot=neighbor)

    return [], visited


def dfs(grid_maze: List[List[Spot]], start_spot: Spot, end_spot: Spot, **kwargs) -> Tuple[List[Spot], Set[Spot]]:
    """
    Perform the depth-first search (DFS) algorithm to find a path from the start spot to the end spot.

    Args:
        grid_maze (List[List[Spot]]): The grid maze containing all the spots.
        start_spot (Spot): The starting spot of the search.
        end_spot (Spot): The ending spot of the search.
        kwargs: Additional optional arguments like 'win', 'draw_updates', and 'window_mode'.

    Returns:
        Tuple[List[Spot], Set[Spot]]: A tuple containing the path from start to end and the set of visited spots.
    """
    win = kwargs.get('win')
    draw_updates = kwargs.get('draw_updates', True)
    window_mode = kwargs.get('window_mode', True)

    stack = [(start_spot, None)]  # Stack initialized with the start spot
    visited = set()
    came_from = {spot: None for row in grid_maze for spot in row}
    path = []

    while stack:
        current_spot, prev = stack.pop()

        if current_spot not in visited:
            visited.add(current_spot)
            came_from[current_spot] = prev

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
                if neighbor not in visited:
                    stack.append((neighbor, current_spot))
                    if neighbor != start_spot and neighbor != end_spot:
                        neighbor.make_next()
                        if draw_updates and window_mode:
                            draw_spot(win=win, spot=neighbor)

    return [], visited


def bfs(grid_maze: List[List[Spot]], start_spot: Spot, end_spot: Spot, **kwargs) -> Tuple[List[Spot], Set[Spot]]:
    """
    Perform the breadth-first search (BFS) algorithm to find the shortest path from the start spot to the end spot.

    Args:
        grid_maze (List[List[Spot]]): The grid maze containing all the spots.
        start_spot (Spot): The starting spot of the search.
        end_spot (Spot): The ending spot of the search.
        kwargs: Additional optional arguments like 'win', 'draw_updates', and 'window_mode'.

    Returns:
        Tuple[List[Spot], Set[Spot]]: A tuple containing the path from start to end and the set of visited spots.
    """
    win = kwargs.get('win')
    draw_updates = kwargs.get('draw_updates', True)
    window_mode = kwargs.get('window_mode', True)

    queue = [(start_spot, None)]  # Queue initialized with the start spot
    visited = set()
    path = []

    came_from = {spot: None for row in grid_maze for spot in row}

    while queue:
        current_spot, prev = queue.pop(0)

        if current_spot not in visited:
            visited.add(current_spot)
            came_from[current_spot] = prev

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
                if neighbor not in visited:
                    queue.append((neighbor, current_spot))
                    if neighbor != start_spot and neighbor != end_spot:
                        neighbor.make_next()
                        if draw_updates and window_mode:
                            draw_spot(win=win, spot=neighbor)

    return [], visited


def __reconstruct_bidirectional_path(meeting_spot, came_from_start, came_from_end):
    """
    Reconstruct the path for bidirectional search algorithms.

    Args:
        meeting_spot (Spot): The spot where the two searches met.
        came_from_start (dict): The path reconstruction dictionary for the start search.
        came_from_end (dict): The path reconstruction dictionary for the end search.

    Returns:
        List[Spot]: The reconstructed path from start to end.
    """
    path_start = []
    path_end = []

    current_spot = meeting_spot
    while current_spot:
        path_start.append(current_spot)
        current_spot = came_from_start[current_spot]
    path_start.reverse()

    current_spot = meeting_spot
    while current_spot:
        path_end.append(current_spot)
        current_spot = came_from_end[current_spot]

    return path_start + path_end[1:]


def __explore_neighbours(pq, current_spot, came_from, visited, g_score, f_score, end_spot, start_spot,
                         draw_updates, window_mode, win):
    """
    Explore the neighbors of the current spot for pathfinding algorithms.

    Args:
        pq (list): The priority queue for the search.
        current_spot (Spot): The current spot being expanded.
        came_from (dict): The path reconstruction dictionary.
        visited (set): The set of visited spots.
        g_score (dict): The g_score dictionary for the search.
        f_score (dict): The f_score dictionary for the search.
        end_spot (Spot): The target spot of the search.
        start_spot (Spot): The starting spot of the search.
        draw_updates (bool): Whether to draw updates on the grid.
        window_mode (bool): Whether the search is displayed in a window.
        win (Any): The Pygame window for drawing updates.

    Returns:
        None
    """
    for neighbor in current_spot.neighbors:
        if neighbor not in visited:
            temp_g_score = g_score[current_spot] + neighbor.spot_value
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current_spot
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + manhattan_heuristic(neighbor, end_spot)
                heapq.heappush(pq, (f_score[neighbor], neighbor))

                if neighbor != start_spot and neighbor != end_spot:
                    neighbor.make_next()
                    if draw_updates and window_mode:
                        draw_spot(win=win, spot=neighbor)
