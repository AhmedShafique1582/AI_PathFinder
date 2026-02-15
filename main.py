import pygame
import sys

# CONFIG
ROWS = 20
COLS = 20
CELL_SIZE = 30

WIDTH = COLS * CELL_SIZE
HEIGHT = ROWS * CELL_SIZE

# Colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (180, 180, 180)
LIGHTBLUE = (150,150,255)
BLUE = (0,0,255)  # final path color

# INIT
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("AI-PATHFINDER")
clock = pygame.time.Clock()

# GRID
grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
start = (0, 0)
target = (19, 19)

# WALLS
for i in range(2, 18):
    grid[10][i] = 1
    grid[11][i] = 1
    grid[i][9] = 1
    grid[i][10] = 1

# DRAW GRID
def draw_grid(path=[]):
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(
                col * CELL_SIZE,
                row * CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            if (row, col) == start:
                pygame.draw.rect(screen, GREEN, rect)
            elif (row, col) == target:
                pygame.draw.rect(screen, RED, rect)
            elif (row, col) in path:
                pygame.draw.rect(screen, BLUE, rect)
            elif grid[row][col] == 1:
                pygame.draw.rect(screen, BLACK, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            pygame.draw.rect(screen, GRAY, rect, 1)

# BFS function with animation
def bfs(start, target):
    from collections import deque
    queue = deque([start])
    visited = {start: None}
    path = []

    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = queue.popleft()

        if current != start and current != target:
            rect = pygame.Rect(current[1]*CELL_SIZE, current[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, LIGHTBLUE, rect)
            pygame.display.flip()
            pygame.time.delay(60)

        if current == target:
            # reconstruct path
            node = target
            while node:
                path.append(node)
                node = visited[node]
            path.reverse()
            return path

        row, col = current
        directions = [(-1,0),(1,0),(0,-1),(0,1),(1,1),(-1,-1),(1,-1),(-1,1)]
        for dr, dc in directions:
            r, c = row+dr, col+dc
            if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c]==0 and (r,c) not in visited:
                queue.append((r,c))
                visited[(r,c)] = current

# MAIN LOOP
running = True
path_found = False
path = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)
    draw_grid(path)
    pygame.display.flip()
    clock.tick(60)

    if not path_found:
        path = bfs(start, target)
        path_found = True
