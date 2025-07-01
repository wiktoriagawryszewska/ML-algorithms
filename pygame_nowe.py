import pygame
from queue import PriorityQueue

# Window configuration
WIDTH = 600  # Window width
WINDOW = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A*")

RED = (255, 100, 100)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (50, 50, 50)
PURPLE = (150, 50, 255)
GRAY = (200, 200, 200)
END_GRAY = (150, 150, 150)

# Single point on the grid
class Point:
    def __init__(self, row, column, width, total_rows):
        self.row = row
        self.column = column
        self.x = row * width
        self.y = column * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def position(self):
        return self.row, self.column

    def is_obstacle(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == BLUE

    def is_end(self):
        return self.color == RED

    def reset(self):
        self.color = WHITE

    def set_start(self):
        self.color = BLUE

    def set_obstacle(self):
        self.color = BLACK

    def set_end(self):
        self.color = RED

    def set_path(self):
        self.color = PURPLE

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.column].is_obstacle():
            self.neighbors.append(grid[self.row + 1][self.column])
        if self.row > 0 and not grid[self.row - 1][self.column].is_obstacle():
            self.neighbors.append(grid[self.row - 1][self.column])
        if self.column < self.total_rows - 1 and not grid[self.row][self.column + 1].is_obstacle():
            self.neighbors.append(grid[self.row][self.column + 1])
        if self.column > 0 and not grid[self.row][self.column - 1].is_obstacle():
            self.neighbors.append(grid[self.row][self.column - 1])

    def __lt__(self, other):
        return False


def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


# Function to reconstruct the path from end to start
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.set_path()
        draw()


# A* algorithm implementation
def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {point: float("inf") for row in grid for point in row}
    g_score[start] = 0
    f_score = {point: float("inf") for row in grid for point in row}
    f_score[start] = h(start.position(), end.position())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, end, draw)
            end.set_end()
            return True

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.position(), end.position())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)

        draw()

    print("No path found!")
    end.color = END_GRAY
    draw()
    return False


# Create grid of points
def create_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            point = Point(i, j, gap, rows)
            grid[i].append(point)
    return grid


# Draw grid lines
def draw_grid(window, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(window, GRAY, (0, i * gap), (width, i * gap))
        pygame.draw.line(window, GRAY, (i * gap, 0), (i * gap, width))


# Draw the entire window
def draw(window, grid, rows, width):
    window.fill(WHITE)
    for row in grid:
        for point in row:
            point.draw(window)
    draw_grid(window, rows, width)
    pygame.display.update()


# Get grid position from mouse position
def get_position(pos, rows, width):
    gap = width // rows
    y, x = pos
    row = y // gap
    column = x // gap
    return row, column


def main(window, width):
    ROWS = 25
    grid = create_grid(ROWS, width)

    start = None
    end = None

    running = True
    while running:
        draw(window, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, column = get_position(pos, ROWS, width)
                point = grid[row][column]
                if not start and point != end:
                    start = point
                    start.set_start()

                elif not end and point != start:
                    end = point
                    end.set_end()

                elif point != end and point != start:
                    point.set_obstacle()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, column = get_position(pos, ROWS, width)
                point = grid[row][column]
                point.reset()
                if point == start:
                    start = None
                elif point == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for point in row:
                            point.update_neighbors(grid)

                    algorithm(lambda: draw(window, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = create_grid(ROWS, width)

    pygame.quit()


main(WINDOW, WIDTH)
