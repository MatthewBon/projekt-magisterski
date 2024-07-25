import time
from enums.colors import Colors as colors
import pygame
from queue import PriorityQueue, Queue
from utils import heuristic, reconstruct_path, calculate_blocks


def a_star(grid, start, end):
    start_time = time.time()
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = heuristic(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end)
            start.make_start()
            end.make_end()

            trace_length = calculate_blocks(grid)
            duration = time.time() - start_time

            return round(duration, 2), trace_length, came_from

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + heuristic(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.mark_next()

        if current != start:
            current.make_closed()

    return False


def dijkstra(grid, start, end):
    start_time = time.time()
    open_set = PriorityQueue()
    open_set.put((0, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[1]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, colors.LIME)
            start.make_start()
            end.make_end()
            trace_length = calculate_blocks(grid, colors.LIME)
            duration = time.time() - start_time

            return round(duration, 2), trace_length, came_from

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                if neighbor not in open_set_hash:
                    open_set.put((g_score[neighbor], neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.mark_next()

        if current != start:
            current.make_closed()

    return False


def bfs(grid, start, end):
    start_time = time.time()
    open_set = Queue()
    open_set.put(start)
    came_from = {}

    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end)

            start.make_start()
            end.make_end()

            trace_length = len(came_from)
            duration = time.time() - start_time

            return round(duration, 2), trace_length

        for neighbor in current.neighbors:
            if neighbor not in open_set_hash:
                came_from[neighbor] = current
                open_set.put(neighbor)
                open_set_hash.add(neighbor)
                neighbor.mark_next()

        if current != start:
            current.make_closed()

    return False
