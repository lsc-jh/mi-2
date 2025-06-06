
import pygame
import os
from collections import deque
from enemy_spawner import EnemySpawner

GROUND_TYPE = "0"
PATH_TYPE = "1"
ARCH_TOWER_TYPE = "2"

def get_abs_path(filename):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), filename))

def load_map(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
    return [line.strip().split() for line in lines]

TILE_SIZE = 64
FPS = 60

def draw_map(screen, grid):
    colors = {
        PATH_TYPE: (50, 50, 50),
        GROUND_TYPE: (0, 105, 5)
    }
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            tile = grid[row][col]
            color = colors.get(tile, (255, 0, 0))
            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            )

def extract_path(grid):
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    start = None
    for row in range(rows):
        if grid[row][0] == PATH_TYPE:
            start = (row, 0)
            break
        else:
            continue

    if not start:
        raise ValueError("No starting point found in the grid.")

    path = []
    q = deque([start])
    visited[start[0]][start[1]] = True

    while q:
        r, c = q.popleft()
        x = c * TILE_SIZE + TILE_SIZE // 2
        y = r * TILE_SIZE + TILE_SIZE // 2
        path.append((x, y))

        for dir_r, dir_c in directions:
            new_r, new_c = r + dir_r, c + dir_c
            if 0 <= new_r < rows and 0 <= new_c < cols and not visited[new_r][new_c]:
                if grid[new_r][new_c] == PATH_TYPE:
                    visited[new_r][new_c] = True
                    q.append((new_r, new_c))

    return path

def main():
    grid = load_map(get_abs_path('map.txt'))

    window_size = (TILE_SIZE * len(grid[0]), TILE_SIZE * len(grid))

    pygame.init()
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption('Tower Defense Game')
    clock = pygame.time.Clock()

    path = extract_path(grid)
    spawner = EnemySpawner(path)

    running = True
    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        draw_map(screen, grid)
        spawner.update(dt)
        spawner.draw(screen)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
