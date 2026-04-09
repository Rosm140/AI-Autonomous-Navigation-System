import random


class DynamicObstacles:
    def __init__(self, grid, num_dynamic=5):
        self.grid = grid
        self.rows, self.cols = grid.shape
        self.dynamic_positions = []

        self._initialize_dynamic_obstacles(num_dynamic)

    def _initialize_dynamic_obstacles(self, num):
        """Place moving obstacles"""
        for _ in range(num):
            while True:
                r = random.randint(0, self.rows - 1)
                c = random.randint(0, self.cols - 1)

                if self.grid[r][c] == 0:
                    self.grid[r][c] = 2  # 2 = dynamic obstacle
                    self.dynamic_positions.append((r, c))
                    break

    def move_obstacles(self):
        """Move obstacles randomly"""
        new_positions = []

        for (r, c) in self.dynamic_positions:
            self.grid[r][c] = 0  # clear old position

            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(directions)

            moved = False

            for d in directions:
                nr = r + d[0]
                nc = c + d[1]

                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.grid[nr][nc] == 0:
                        self.grid[nr][nc] = 2
                        new_positions.append((nr, nc))
                        moved = True
                        break

            if not moved:
                self.grid[r][c] = 2
                new_positions.append((r, c))

        self.dynamic_positions = new_positions