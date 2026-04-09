import numpy as np
import matplotlib.pyplot as plt

class GridEnvironment:
    def __init__(self, rows=20, cols=20):
        self.rows = rows
        self.cols = cols

        # Create grid (0 = empty)
        self.grid = np.zeros((rows, cols), dtype=int)

        self.start = None
        self.goal = None

    def add_obstacle(self, row, col):
        """Set obstacle at given position"""
        self.grid[row][col] = 1

    def set_start(self, row, col):
        """Set start position"""
        self.start = (row, col)

    def set_goal(self, row, col):
        """Set goal position"""
        self.goal = (row, col)

    def print_grid(self):
        """Print grid in console"""
        print("Grid Representation:")
        print(self.grid)

    def visualize(self):
        """Display grid using matplotlib"""
        plt.figure(figsize=(6, 6))
        plt.imshow(self.grid, cmap='gray_r')

        # Mark start (green)
        if self.start:
            plt.scatter(self.start[1], self.start[0], c='green', s=100, label='Start')

        # Mark goal (red)
        if self.goal:
            plt.scatter(self.goal[1], self.goal[0], c='red', s=100, label='Goal')

        plt.title("2D Grid Environment")
        plt.legend()
        plt.grid(True)
        plt.show()


# Test run (only runs if file executed directly)
if __name__ == "__main__":
    env = GridEnvironment()

    # Add some obstacles
    env.add_obstacle(5, 5)
    env.add_obstacle(5, 6)
    env.add_obstacle(5, 7)
    env.add_obstacle(10, 10)
    env.add_obstacle(12, 14)

    # Set start and goal
    env.set_start(0, 0)
    env.set_goal(19, 19)

    # Output
    env.print_grid()
    env.visualize()