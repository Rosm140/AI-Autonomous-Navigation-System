import numpy as np
import matplotlib.pyplot as plt
import time
from saver import OutputSaver

class Visualizer:
    def __init__(self, grid, start, goal, path):
        self.grid = grid
        self.start = start
        self.goal = goal
        self.path = path
        self.current_position = start
        self.saver = OutputSaver()

    def draw_frame(self, path_so_far):
        """Draw single frame"""
        plt.clf()

        # Draw grid
        plt.imshow(self.grid, cmap='gray_r')

        # Draw path so far
        if path_so_far:
            y = [p[0] for p in path_so_far]
            x = [p[1] for p in path_so_far]
            plt.plot(x, y, color='red', linewidth=2, label='Path')

        # Draw start
        plt.scatter(self.start[1], self.start[0], c='green', s=100, label='Start')

        # Draw goal
        plt.scatter(self.goal[1], self.goal[0], c='blue', s=100, label='Goal')

        # Draw robot (current position)
        plt.scatter(self.current_position[1], self.current_position[0],
                    c='yellow', s=120, label='Robot')

        plt.title("Autonomous Robot Navigation")
        plt.legend(loc='upper right')
        plt.grid(True)

        # Replace imshow with custom coloring
        display_grid = self.grid.copy()

        # Dynamic obstacles → mark differently
        display_grid[display_grid == 2] = 0.5  # gray

        plt.imshow(display_grid, cmap='gray_r')

    def simulate_movement(self, delay=0.3):
        """Simulate robot moving step-by-step"""
        if not self.path:
            print("No path to simulate!")
            return

        plt.figure(figsize=(6, 6))

        path_so_far = []

        for i, step in enumerate(self.path):
            self.current_position = step
            path_so_far.append(step)

            self.draw_frame(path_so_far)
            self.saver.save_frame(i)

            plt.pause(delay)    

        plt.show()