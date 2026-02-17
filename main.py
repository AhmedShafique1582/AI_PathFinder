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
BLUE = (0,0,255)

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

# BFS
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

        # animation
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

# DFS
def dfs(start, target):
    from collections import deque
    stack = deque([start])
    visited = {start: None}
    path = []

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current = stack.pop()

        # animation
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
                stack.append((r,c))
                visited[(r,c)] = current

# DLS
def dls(start, target, limit):
    from collections import deque
    stack = deque([(start, 0)])
    visited = {start: None}
    path = []

    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        current, depth = stack.pop()

        # animation
        if current != start and current != target:
            rect = pygame.Rect(
                current[1]*CELL_SIZE,
                current[0]*CELL_SIZE,
                CELL_SIZE,
                CELL_SIZE
            )
            pygame.draw.rect(screen, LIGHTBLUE, rect)
            pygame.display.flip()
            pygame.time.delay(60)

        if current == target:
            node = target
            while node:
                path.append(node)
                node = visited[node]
            path.reverse()
            return path

        if depth == limit:
            continue

        row, col = current
        directions = [
            (-1,0),(1,0),(0,-1),(0,1),
            (1,1),(-1,-1),(1,-1),(-1,1)
        ]

        for dr, dc in directions:
            r, c = row + dr, col + dc
            if (
                0 <= r < ROWS and
                0 <= c < COLS and
                grid[r][c] == 0 and
                (r, c) not in visited
            ):
                stack.append(((r, c), depth + 1))
                visited[(r, c)] = current

    return None

#IDDFS
def iddfs(start, target,max_depth):
        for limit in range(max_depth + 1):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            result = dls(start, target, limit)
            if result is not None:
                return result
        return None

#BIDIRECTIONAL
def bidirectional(start, target):
    from collections import deque

    q1 = deque([start])
    q2 = deque([target])

    visited1 = {start: None}
    visited2 = {target: None}

    while q1 and q2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # start side
        cur1 = q1.popleft()
        # animation
        if cur1 != start and cur1 != target:
            rect = pygame.Rect(cur1[1] * CELL_SIZE, cur1[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, LIGHTBLUE, rect)
            pygame.display.flip()
            pygame.time.delay(60)

        if cur1 in visited2:
            path = []
            node = cur1
            while node:
                path.append(node)
                node = visited1[node]
            path.reverse()

            node = visited2[cur1]
            while node:
                path.append(node)
                node = visited2[node]
            return path

        r, c = cur1
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),(1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dr, dc in directions:
            nr, nc = r+dr, c+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc]==0 and (nr,nc) not in visited1:
                visited1[(nr,nc)] = cur1
                q1.append((nr,nc))

        # target side
        cur2 = q2.popleft()
        # animation
        if cur2 != start and cur2 != target:
            rect = pygame.Rect(cur2[1] * CELL_SIZE, cur2[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, LIGHTBLUE, rect)
            pygame.display.flip()
            pygame.time.delay(60)

        if cur2 in visited1:
            path = []
            node = cur2
            while node:
                path.append(node)
                node = visited1[node]
            path.reverse()

            node = visited2[cur2]
            while node:
                path.append(node)
                node = visited2[node]
            return path

        r, c = cur2
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)
        ]
        for dr, dc in directions:
            nr, nc = r+dr, c+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc]==0 and (nr,nc) not in visited2:
                visited2[(nr,nc)] = cur2
                q2.append((nr,nc))

    return None

def ucs(start, target):
    import heapq

    pq = [(0, start)]
    visited = {start: None}
    cost = {start: 0}

    while pq:
        cur_cost, cur = heapq.heappop(pq)
        node = cur

        # animation
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if node != start and node != target:
            rect = pygame.Rect(node[1]*CELL_SIZE, node[0]*CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, LIGHTBLUE, rect)
            pygame.display.flip()
            pygame.time.delay(60)

        if cur == target:
            path = []
            while cur:
                path.append(cur)
                cur = visited[cur]
            path.reverse()
            return path

        r, c = node
        directions = [
            (-1, 0), (1, 0), (0, -1), (0, 1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)
        ]
        for dr, dc in directions:
            nr, nc = r+dr, c+dc
            if 0 <= nr < ROWS and 0 <= nc < COLS and grid[nr][nc]==0:
                new_cost = cur_cost + 1
                if (nr,nc) not in cost or new_cost < cost[(nr,nc)]:
                    cost[(nr,nc)] = new_cost
                    visited[(nr,nc)] = node
                    heapq.heappush(pq, (new_cost, (nr,nc)))

    return None


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
        # path = dfs(start, target)
        # path = iddfs(start, target, max_depth=40)
        # path = bidirectional(start, target)
        # path = ucs(start, target)
    path_found = True
