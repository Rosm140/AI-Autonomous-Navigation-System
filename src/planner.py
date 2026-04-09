import heapq


class PathPlanner:
    def __init__(self, grid):
        self.grid = grid
        self.rows, self.cols = grid.shape

    def get_neighbors(self, node):
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []

        for d in directions:
            r = node[0] + d[0]
            c = node[1] + d[1]

            if 0 <= r < self.rows and 0 <= c < self.cols:
               if self.grid[r][c] != 1 and self.grid[r][c] != 2:  # 1 = static obstacle, 2 = dynamic obstacle
                    neighbors.append((r, c))

        return neighbors

    def heuristic(self, a, b):
        """Manhattan distance (for A*)"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # 🔹 A* Algorithm
    def astar(self, start, goal):
        open_list = []
        heapq.heappush(open_list, (0, start))

        came_from = {}
        g_cost = {start: 0}

        while open_list:
            current = heapq.heappop(open_list)[1]

            if current == goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.get_neighbors(current):
                new_cost = g_cost[current] + 1

                if neighbor not in g_cost or new_cost < g_cost[neighbor]:
                    g_cost[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, goal)

                    heapq.heappush(open_list, (priority, neighbor))
                    came_from[neighbor] = current

        return None

    # 🔹 Dijkstra Algorithm
    def dijkstra(self, start, goal):
        open_list = []
        heapq.heappush(open_list, (0, start))

        came_from = {}
        cost = {start: 0}

        while open_list:
            current_cost, current = heapq.heappop(open_list)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.get_neighbors(current):
                new_cost = cost[current] + 1

                if neighbor not in cost or new_cost < cost[neighbor]:
                    cost[neighbor] = new_cost
                    heapq.heappush(open_list, (new_cost, neighbor))
                    came_from[neighbor] = current

        return None

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)

        path.reverse()
        return path