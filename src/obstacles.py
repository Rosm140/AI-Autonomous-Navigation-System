import numpy as np
import random

def generate_obstacles(grid, density=0.2, start=None, goal=None):
    """
    Generate random obstacles on the grid.

    Parameters:
    - grid: numpy 2D array
    - density: percentage of grid to fill with obstacles (0 to 1)
    - start: (row, col)
    - goal: (row, col)

    Returns:
    - updated grid with obstacles
    """
    
    

    rows, cols = grid.shape
    total_cells = rows * cols
    obstacle_count = int(total_cells * density)

    obstacles_added = 0

    while obstacles_added < obstacle_count:
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)

        # Avoid overwriting start/goal and existing obstacles
        if grid[r][c] == 0:
            if (start and (r, c) == start) or (goal and (r, c) == goal):
                continue

            grid[r][c] = 1
            obstacles_added += 1

    return grid


# Test run
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    grid = np.zeros((20, 20), dtype=int)

    start = (0, 0)
    goal = (19, 19)

    grid = generate_obstacles(grid, density=0.3, start=start, goal=goal)

    # Visualize
    plt.imshow(grid, cmap='gray_r')
    plt.scatter(start[1], start[0], c='green', s=100, label='Start')
    plt.scatter(goal[1], goal[0], c='red', s=100, label='Goal')
    plt.title("Obstacle Generation")
    plt.legend()
    plt.show()
    buffer = 2  # instead of 1