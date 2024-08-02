import heapq
from typing import List, Tuple, Set
from spot import Spot
from utils import manhattan_heuristic, reconstruct_path, draw_spot


def a_star(grid_maze: List[List[Spot]], start_spot: Spot, end_spot: Spot, **kwargs) -> Tuple[List[Spot], Set[Spot]]:
    """
    Perform the A* search algorithm.

    Args:
        grid_maze (List[List[Spot]]): The grid maze containing spots.
        start_spot (Spot): The starting spot.
        end_spot (Spot): The ending spot.
        kwargs: Additional arguments like 'win', 'draw_updates', 'window_mode', 'heuristic_method'.

    Returns:
        Tuple[List[Spot], Set[Spot]]: The path and visited spots.
    """
    win = kwargs.get('win')
    draw_updates = kwargs.get('draw_updates', True)
    window_mode = kwargs.get('window_mode', True)
    heuristic_method = kwargs.get('heuristic_method', manhattan_heuristic)

    # Priority queue initialized with the start spot
    pq = [(0, start_spot)]  # Priority queue of (f_score, Spot)
    visited = set()
    path = []

    # Initialize g_score and f_score for all spots
    g_score = {spot: float("inf") for row in grid_maze for spot in row}
    g_score[start_spot] = 0
    f_score = {spot: float("inf") for row in grid_maze for spot in row}
    f_score[start_spot] = manhattan_heuristic(start_spot, end_spot)

    # Dictionary to keep track of the most efficient path
    came_from = {spot: None for row in grid_maze for spot in row}

    while pq:
        current_f_score, current_spot = heapq.heappop(pq)

        if current_spot in visited:
            continue
        visited.add(current_spot)

        # Mark the current spot as closed and draw it if needed
        if current_spot != start_spot and current_spot != end_spot:
            current_spot.make_closed()
            if draw_updates and window_mode:
                draw_spot(win=win, spot=current_spot)

        # If the end spot is reached, reconstruct the path
        if current_spot == end_spot:
            while current_spot:
                path.append(current_spot)
                current_spot = came_from[current_spot]
            path.reverse()
            reconstruct_path(path, grid_maze, start_spot, end_spot, draw_updates, win, window_mode=window_mode)
            return path, visited

        # Explore the neighbors of the current spot
        for neighbor in current_spot.neighbors:
            if neighbor not in visited:
                temp_g_score = g_score[current_spot] + neighbor.spot_value
                if temp_g_score < g_score[neighbor]:
                    came_from[neighbor] = current_spot
                    g_score[neighbor] = temp_g_score
                    f_score[neighbor] = temp_g_score + heuristic_method(neighbor, end_spot)
                    heapq.heappush(pq, (f_score[neighbor], neighbor))

                    if neighbor != start_spot and neighbor != end_spot:
                        neighbor.make_next()
                        if draw_updates and window_mode:
                            draw_spot(win=win, spot=neighbor)

    return [], visited


def dijkstra(grid_maze: List[List[Spot]], start_spot: Spot, end_spot: Spot, **kwargs) -> Tuple[List[Spot], Set[Spot]]:
    """
    Perform the Dijkstra's algorithm.

    Args:
        grid_maze (List[List[Spot]]): The grid maze containing spots.
        start_spot (Spot): The starting spot.
        end_spot (Spot): The ending spot.
        kwargs: Additional arguments like 'win', 'draw_updates', 'window_mode'.

    Returns:
        Tuple[List[Spot], Set[Spot]]: The path and visited spots.
    """
    win = kwargs.get('win')
    draw_updates = kwargs.get('draw_updates', True)
    window_mode = kwargs.get('window_mode', True)

    # Priority queue initialized with the start spot
    pq = [(0, start_spot)]  # Priority queue of (distance, Spot)

    # Initialize g_score for all spots
    g_score = {spot: float('inf') for row in grid_maze for spot in row}
    g_score[start_spot] = 0

    visited = set()

    # Dictionary to keep track of the most efficient path
    came_from = {spot: None for row in grid_maze for spot in row}

    while pq:
        current_distance, current_spot = heapq.heappop(pq)
        if current_spot in visited:
            continue
        visited.add(current_spot)

        # Mark the current spot as closed and draw it if needed
        if current_spot != start_spot and current_spot != end_spot:
            current_spot.make_closed()
            if draw_updates and window_mode:
                draw_spot(win=win, spot=current_spot)

        # If the end spot is reached, reconstruct the path
        if current_spot == end_spot:
            current = end_spot
            path = []
            while current:
                path.append(current)
                current = came_from[current]
            path.reverse()
            reconstruct_path(path, grid_maze, start_spot, end_spot, draw_updates, win, window_mode=window_mode)
            return path, visited

        # Explore the neighbors of the current spot
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
    Perform the limited depth-first search algorithm.

    Args:
        grid_maze (List[List[Spot]]): The grid maze containing spots.
        start_spot (Spot): The starting spot.
        end_spot (Spot): The ending spot.
        kwargs: Additional arguments like 'win', 'draw_updates', 'window_mode'.

    Returns:
        Tuple[List[Spot], Set[Spot]]: The path and visited spots.
    """
    win = kwargs.get('win')
    draw_updates = kwargs.get('draw_updates', True)
    window_mode = kwargs.get('window_mode', True)

    depth = 0
    stack = [(start_spot, None, depth)]  # Stack of (Spot, predecessor, depth)
    visited = set()

    # Dictionary to keep track of the most efficient path
    came_from = {spot: None for row in grid_maze for spot in row}
    path = []
    depth_limit = 100  # Initial depth limit

    while stack:
        if depth < depth_limit:
            current_spot, prev, depth = stack.pop()
        else:
            current_spot, prev, depth = stack.pop(0)
            depth_limit += int(depth_limit * 0.1)  # Increase depth limit by 10%

        if current_spot not in visited:
            visited.add(current_spot)
            came_from[current_spot] = prev

            # Mark the current spot as closed and draw it if needed
            if current_spot != start_spot and current_spot != end_spot:
                current_spot.make_closed()
                if draw_updates and window_mode:
                    draw_spot(win=win, spot=current_spot)

            # If the end spot is reached, reconstruct the path
            if current_spot == end_spot:
                while current_spot:
                    path.append(current_spot)
                    current_spot = came_from[current_spot]
                path.reverse()
                reconstruct_path(path, grid_maze, start_spot, end_spot, draw_updates, win, window_mode=window_mode)
                return path, visited

            # Explore the neighbors of the current spot
            for neighbor in current_spot.neighbors:
                if neighbor not in visited:
                    stack.append((neighbor, current_spot, depth + 1))
                    if neighbor != start_spot and neighbor != end_spot:
                        neighbor.make_next()
                        if draw_updates and window_mode:
                            draw_spot(win=win, spot=neighbor)

    return [], visited


def dfs(grid_maze: List[List[Spot]], start_spot: Spot, end_spot: Spot, **kwargs) -> Tuple[List[Spot], Set[Spot]]:
    """
    Perform the depth-first search algorithm.

    Args:
        grid_maze (List[List[Spot]]): The grid maze containing spots.
        start_spot (Spot): The starting spot.
        end_spot (Spot): The ending spot.
        kwargs: Additional arguments like 'win', 'draw_updates', 'window_mode'.

    Returns:
        Tuple[List[Spot], Set[Spot]]: The path and visited spots.
    """
    win = kwargs.get('win')
    draw_updates = kwargs.get('draw_updates', True)
    window_mode = kwargs.get('window_mode', True)

    stack = [(start_spot, None)]  # Stack of (Spot, predecessor)
    visited = set()

    # Dictionary to keep track of the most efficient path
    came_from = {spot: None for row in grid_maze for spot in row}
    path = []

    while stack:
        current_spot, prev = stack.pop()

        if current_spot not in visited:
            visited.add(current_spot)
            came_from[current_spot] = prev

            # Mark the current spot as closed and draw it if needed
            if current_spot != start_spot and current_spot != end_spot:
                current_spot.make_closed()
                if draw_updates and window_mode:
                    draw_spot(win=win, spot=current_spot)

            # If the end spot is reached, reconstruct the path
            if current_spot == end_spot:
                while current_spot:
                    path.append(current_spot)
                    current_spot = came_from[current_spot]
                path.reverse()
                reconstruct_path(path, grid_maze, start_spot, end_spot, draw_updates, win, window_mode=window_mode)
                return path, visited

            # Explore the neighbors of the current spot
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
    Perform the breadth-first search algorithm.

    Args:
        grid_maze (List[List[Spot]]): The grid maze containing spots.
        start_spot (Spot): The starting spot.
        end_spot (Spot): The ending spot.
        kwargs: Additional arguments like 'win', 'draw_updates', 'window_mode'.

    Returns:
        Tuple[List[Spot], Set[Spot]]: The path and visited spots.
    """
    win = kwargs.get('win')
    draw_updates = kwargs.get('draw_updates', True)
    window_mode = kwargs.get('window_mode', True)

    queue = [(start_spot, None)]  # Queue of (Spot, predecessor)
    visited = set()
    path = []

    # Dictionary to keep track of the most efficient path
    came_from = {spot: None for row in grid_maze for spot in row}

    while queue:
        current_spot, prev = queue.pop(0)

        if current_spot not in visited:
            visited.add(current_spot)
            came_from[current_spot] = prev

            # Mark the current spot as closed and draw it if needed
            if current_spot != start_spot and current_spot != end_spot:
                current_spot.make_closed()
                if draw_updates and window_mode:
                    draw_spot(win=win, spot=current_spot)

            # If the end spot is reached, reconstruct the path
            if current_spot == end_spot:
                while current_spot:
                    path.append(current_spot)
                    current_spot = came_from[current_spot]
                path.reverse()
                reconstruct_path(path, grid_maze, start_spot, end_spot, draw_updates, win, window_mode=window_mode)
                return path, visited

            # Explore the neighbors of the current spot
            for neighbor in current_spot.neighbors:
                if neighbor not in visited:
                    queue.append((neighbor, current_spot))
                    if neighbor != start_spot and neighbor != end_spot:
                        neighbor.make_next()
                        if draw_updates and window_mode:
                            draw_spot(win=win, spot=neighbor)

    return [], visited
