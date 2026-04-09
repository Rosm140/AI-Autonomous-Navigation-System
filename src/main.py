from tracemalloc import start

import numpy as np

from grid import GridEnvironment
from obstacles import generate_obstacles
from astar import AStar
import planner
from visualization import Visualizer
from saver import OutputSaver
from planner import PathPlanner
import time


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
    print("🔄 Running A* Path Planning...")

    astar = AStar(env.grid, start, goal)
    path = astar.find_path()

    # Retry mechanism (important for reliability)
    attempts = 0
    max_attempts = 5

    while path is None and attempts < max_attempts:
        print(f"⚠️ No path found. Regenerating obstacles... (Attempt {attempts + 1})")

        env.grid = np.zeros((rows, cols), dtype=int)
        env.grid = generate_obstacles(env.grid, density, start, goal)

        astar = AStar(env.grid, start, goal)
        path = astar.find_path()

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

    # Step 4: Simulate Movement
    print("🚀 Starting Simulation...")

    visualizer = Visualizer(env.grid, start, goal, path)
    visualizer.simulate_movement(delay=0.2)


if __name__ == "__main__":
    run_simulation()