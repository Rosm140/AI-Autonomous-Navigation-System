import heapq
import numpy as np
import matplotlib.pyplot as plt


class AStar:
    def __init__(self, grid, start, goal):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.rows, self.cols = grid.shape

    def heuristic(self, a, b):
        """Manhattan Distance"""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def get_neighbors(self, node):
        """Get valid neighbors (up, down, left, right)"""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        neighbors = []

        for d in directions:
            r = node[0] + d[0]
            c = node[1] + d[1]

            if 0 <= r < self.rows and 0 <= c < self.cols:
                if self.grid[r][c] == 0:  # not obstacle
                    neighbors.append((r, c))

        return neighbors

    def find_path(self):
        """A* Algorithm"""
        open_list = []
        heapq.heappush(open_list, (0, self.start))

        came_from = {}
        g_cost = {self.start: 0}
        f_cost = {self.start: self.heuristic(self.start, self.goal)}

        while open_list:
            current = heapq.heappop(open_list)[1]

            if current == self.goal:
                return self.reconstruct_path(came_from, current)

            for neighbor in self.get_neighbors(current):
                tentative_g = g_cost[current] + 1

                if neighbor not in g_cost or tentative_g < g_cost[neighbor]:
                    came_from[neighbor] = current
                    g_cost[neighbor] = tentative_g
                    f_cost[neighbor] = tentative_g + self.heuristic(neighbor, self.goal)

                    heapq.heappush(open_list, (f_cost[neighbor], neighbor))

        return None  # No path found

    def reconstruct_path(self, came_from, current):
        """Backtrack path"""
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)

        path.reverse()
        return path


# 🔹 Visualization function
def visualize_path(grid, path, start, goal):
    plt.figure(figsize=(6, 6))
    plt.imshow(grid, cmap='gray_r')

    # Plot path
    if path:
        path_y = [p[0] for p in path]
        path_x = [p[1] for p in path]
        plt.plot(path_x, path_y, color='blue', linewidth=2, label='Path')

    # Start & Goal
    plt.scatter(start[1], start[0], c='green', s=100, label='Start')
    plt.scatter(goal[1], goal[0], c='red', s=100, label='Goal')

    plt.title("A* Path Planning")
    plt.legend()
    plt.grid(True)
    plt.show()


# 🔹 Test run
if __name__ == "__main__":
    from obstacles import generate_obstacles

    grid = np.zeros((20, 20), dtype=int)

    start = (0, 0)
    goal = (19, 19)

    grid = generate_obstacles(grid, density=0.3, start=start, goal=goal)

    astar = AStar(grid, start, goal)
    path = astar.find_path()

    if path:
        print("Path found:")
        print(path)
    else:
        print("No path found!")

    visualize_path(grid, path, start, goal)