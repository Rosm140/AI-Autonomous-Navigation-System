from tracemalloc import start

import numpy as np

from grid import GridEnvironment
from obstacles import generate_obstacles
import planner
from visualization import Visualizer
from saver import OutputSaver
import time
from dynamic_obstacles import DynamicObstacles
from planner import PathPlanner

def run_simulation(rows=20, cols=20, density=0.25):
    """
    Full pipeline:
    Grid → Obstacles → A* Path → Movement Simulation
    """

    print("🔄 Initializing Environment...")
    
    # Step 1: Create Grid
    env = GridEnvironment(rows, cols)

    start = (0, 0)
    goal = (rows - 1, cols - 1)

    env.set_start(*start)
    env.set_goal(*goal)

    print("✅ Grid Created")

    # Step 2: Generate Obstacles
    print("🔄 Generating Obstacles...")

    env.grid = generate_obstacles(
        env.grid,
        density=density,
        start=start,
        goal=goal
    )

    print("✅ Obstacles Added")
    
    # Step 3: Run A* Path Planning
    planner = PathPlanner(env.grid)

    # 🔹 A*
    start_time = time.time()
    path_astar = planner.astar(start, goal)
    astar_time = time.time() - start_time

    # 🔹 Dijkstra
    start_time = time.time()
    path_dijkstra = planner.dijkstra(start, goal)
    dijkstra_time = time.time() - start_time

    print("\n📊 Performance Comparison:")
    print(f"A* Time: {astar_time:.6f}s")
    print(f"Dijkstra Time: {dijkstra_time:.6f}s")
  

    # Step 3: Run Path Planning
    planner = PathPlanner(env.grid)

    # Initial path
    path = planner.astar(start, goal)
    # Retry mechanism (important for reliability)
    attempts = 0
    max_attempts = 5
    
    while path is None and attempts < max_attempts:
        print(f"⚠️ No path found. Regenerating obstacles... (Attempt {attempts + 1})")

        env.grid = np.zeros((rows, cols), dtype=int)
        env.grid = generate_obstacles(env.grid, density, start, goal)

        attempts += 1

    if path is None:
        print("❌ Failed to find path after multiple attempts.")
        return

    print("✅ Path Found!")
    saver = OutputSaver()

    # Save logs
    saver.save_logs(path)

    # Save final image
    saver.save_final_path_image(env.grid, path, start, goal)
    print(f"📍 Path Length: {len(path)}")

    print("🚀 Starting Dynamic Simulation...")

    # Initialize dynamic obstacles
    dyn_obs = DynamicObstacles(env.grid, num_dynamic=8)

    # Use planner (NOT old AStar)
    planner = PathPlanner(env.grid)

    # Start with A* path
    path = planner.astar(start, goal)

    visualizer = Visualizer(env.grid, start, goal, path)

    current_position = start

    for step in range(100):  # simulation steps
        # Move dynamic obstacles
        dyn_obs.move_obstacles()

        # Recalculate path from current position
        path = planner.astar(current_position, goal)

        if path is None:
            print("❌ No path due to dynamic obstacles!")
            break

        # Move one step forward
        if len(path) > 1:
            current_position = path[1]

        # Update visualization
        visualizer.current_position = current_position
        visualizer.draw_frame(path)

        import matplotlib.pyplot as plt
        plt.pause(0.2)

        # Stop if reached goal
        if current_position == goal:
            print("✅ Goal Reached!")
            break

    plt.show()
    
       
if __name__ == "__main__":
    run_simulation()