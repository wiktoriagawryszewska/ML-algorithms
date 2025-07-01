import numpy as np
import math
import heapq

# Wczytanie siatki z pliku
file_path = r"C:\Users\Wiktoria\Downloads\ERI-c1-2024\grid.txt"
grid = np.loadtxt(file_path, dtype=int)

# Start i cel
start = (19, 0)
goal = (0, 19)

#przyblizony koszt 
def heuristic(pos, goal):
    return math.sqrt((goal[0] - pos[0]) ** 2 + (goal[1] - pos[1]) ** 2)

# implementacja A*
def find_path(grid, start, goal):
    rows, cols = grid.shape
    open_list = []  # Lista otwarta przechowuje pola do sprawdzenia
    heapq.heappush(open_list, (0, start))
    came_from = {}       # Śledzenie poprzednich pól
    g_cost = {start: 0}  # Koszt od startu do danego pola

    while open_list:
        _, current = heapq.heappop(open_list) # Pobierz pole z najniższym kosztem

        # Jeśli dotarliśmy do celu, odtwórz trasę
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            return path[::-1]

        # Sprawdź sąsiadów
        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Góra, dół, lewo, prawo
            neighbor = (x + dx, y + dy)

            if 0 <= neighbor[0] < rows and 0 <= neighbor[1] < cols and grid[neighbor] != 5:
                new_g_cost = g_cost[current] + 1 # Koszt od startu do sąsiada

                # Jeśli sąsiad nie jest na liście otwartej lub nowy koszt jest mniejszy
                if neighbor not in g_cost or new_g_cost < g_cost[neighbor]:
                    g_cost[neighbor] = new_g_cost
                    f_cost = new_g_cost + heuristic(neighbor, goal)
                    heapq.heappush(open_list, (f_cost, neighbor))
                    came_from[neighbor] = current

    return None  # Jeśli nie znaleziono trasy

# Uruchom algorytm
path = find_path(grid, start, goal)

grid_with_path = grid.copy()
# Zaznaczenie trasy w siatce
if path:
    for x, y in path:
        grid_with_path[x, y] = 3

# Wyświetlenie siatki
print("Siatka z trasą:")
for row in grid_with_path:
    print(" ".join(map(str, row)))

# Informacja o wyniku
if path:
    print("\nTrasa znaleziona")
else:
    print("\nNie znaleziono trasy")
