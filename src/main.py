import numpy as np
import matplotlib.pyplot as plt
import time

from grid import GridEnvironment
from obstacles import generate_obstacles
from visualization import Visualizer
from saver import OutputSaver
from dynamic_obstacles import DynamicObstacles
from planner import PathPlanner
from analytics import Analytics


# 🎮 UI Controller
class UIController:
    def __init__(self):
        self.running = False
        self.algorithm = "astar"
        self.reset = False

    def on_key(self, event):
        if event.key == ' ':
            self.running = not self.running
            print("▶ Running" if self.running else "⏸ Paused")

        elif event.key == 'r':
            self.reset = True
            print("🔄 Reset Triggered")

        elif event.key == 'a':
            self.algorithm = "astar"
            print("⚡ A* Selected")

        elif event.key == 'd':
            self.algorithm = "dijkstra"
            print("🐢 Dijkstra Selected")

        elif event.key == 'escape':
            print("❌ Exit")
            exit()


def run_simulation(rows=20, cols=20, density=0.25):

    print("🔄 Initializing Environment...")

    # Grid setup
    env = GridEnvironment(rows, cols)
    start = (0, 0)
    goal = (rows - 1, cols - 1)

    env.set_start(*start)
    env.set_goal(*goal)

    print("✅ Grid Created")

    # Obstacles
    env.grid = generate_obstacles(env.grid, density, start, goal)
    print("✅ Obstacles Added")

    planner = PathPlanner(env.grid)

    # -------- PERFORMANCE --------
    start_time = time.time()
    result_astar = planner.astar(start, goal)
    astar_time = time.time() - start_time

    start_time = time.time()
    result_dijkstra = planner.dijkstra(start, goal)
    dijkstra_time = time.time() - start_time

    print("\n📊 Performance Comparison:")
    print(f"A* Time: {astar_time:.6f}s")
    print(f"Dijkstra Time: {dijkstra_time:.6f}s")

    # Analytics
    analytics = Analytics()

    if result_astar:
        path_astar, visited_astar = result_astar
    else:
        path_astar, visited_astar = None, []

    analytics.plot_performance(astar_time, dijkstra_time)
    plt.pause(2)
    plt.close()

    if visited_astar:
        analytics.plot_heatmap(visited_astar, env.grid)
        plt.pause(2)
        plt.close()

    # -------- ENSURE PATH --------
    attempts = 0
    max_attempts = 5
    path = None

    while attempts < max_attempts:
        result = planner.astar(start, goal)

        if result:
            path, _ = result
            break

        print("⚠️ No path → regenerating...")
        env.grid = np.zeros((rows, cols), dtype=int)
        env.grid = generate_obstacles(env.grid, density, start, goal)
        planner = PathPlanner(env.grid)

        attempts += 1

    if path is None:
        print("❌ Failed to find path")
        return

    print("✅ Path Found!")

    # Save outputs
    saver = OutputSaver()
    saver.save_logs(path)
    saver.save_final_path_image(env.grid, path, start, goal)

    print(f"📍 Path Length: {len(path)}")

    # -------- SIMULATION --------
    print("🚀 Starting Simulation...")

    dyn_obs = DynamicObstacles(env.grid, num_dynamic=8)
    visualizer = Visualizer(env.grid, start, goal, path)

    current_position = start

    ui = UIController()

    fig = plt.figure(figsize=(6, 6))
    fig.canvas.mpl_connect('key_press_event', ui.on_key)

    for step in range(500):

        # -------- RESET --------
        if ui.reset:
            print("🔄 Resetting...")

            env.grid = np.zeros((rows, cols), dtype=int)
            env.grid = generate_obstacles(env.grid, density, start, goal)

            dyn_obs = DynamicObstacles(env.grid, num_dynamic=8)
            planner = PathPlanner(env.grid)

            current_position = start

            result = planner.astar(start, goal)
            path = result[0] if result else []

            ui.reset = False

        # -------- PAUSE --------
        if not ui.running:
            plt.pause(0.1)
            continue

        # Move obstacles
        dyn_obs.move_obstacles()

        # Algorithm switch
        if ui.algorithm == "astar":
            result = planner.astar(current_position, goal)
        else:
            result = planner.dijkstra(current_position, goal)

        if result is None:
            print("❌ Path blocked!")
            continue

        path, _ = result

        # Move robot
        if len(path) > 1:
            current_position = path[1]

        # Draw
        visualizer.current_position = current_position
        visualizer.draw_frame(path)

        plt.pause(0.2)

        if current_position == goal:
            print("✅ Goal Reached!")
            break

    plt.show()


if __name__ == "__main__":
    run_simulation()