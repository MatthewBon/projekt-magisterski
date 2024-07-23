
import pygame
from grid import generate_grid_maze, draw
from algorithms import a_star


WIDTH = 1400


def run_algorithm(algorithm, draw_alg_trace, grid, start, end):
    algorithm(draw_alg_trace, grid, start, end)


def main(width):
    rows = 85
    if not rows % 2:
        rows += 1
    gap = width // rows
    width = rows * gap
    win = pygame.display.set_mode((width, width))
    pygame.display.set_caption("Path Finding Algorithm")
    grid, start, end = generate_grid_maze(rows, gap)
    draw(win, grid)
    run = True

    while run:
        draw(win, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    algorithms = {
                        "A*": a_star,
                    }
                    for name, algorithm in algorithms.items():
                        start.make_start()
                        end.make_end()
                        draw(win, grid)
                        for row in grid:
                            for spot in row:
                                spot.update_neighbors(grid)
                        run_algorithm(algorithm, lambda: draw(win, grid), grid, start, end)

    pygame.quit()


if __name__ == "__main__":
    main(WIDTH)
