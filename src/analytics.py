import matplotlib.pyplot as plt
import numpy as np


class Analytics:
    def __init__(self):
        pass

    def plot_performance(self, astar_time, dijkstra_time):
        """Bar chart comparison"""

        algorithms = ['A*', 'Dijkstra']
        times = [astar_time, dijkstra_time]

        plt.figure(figsize=(6, 4))
        plt.bar(algorithms, times)
        plt.title("Algorithm Performance Comparison")
        plt.xlabel("Algorithm")
        plt.ylabel("Time (seconds)")
        plt.grid(True)

        plt.show()

    def plot_heatmap(self, visited_nodes, grid):
        """Show explored nodes heatmap"""

        heatmap = np.zeros_like(grid, dtype=float)

        for node in visited_nodes:
            heatmap[node] += 1

        plt.figure(figsize=(6, 6))
        plt.imshow(heatmap, cmap='hot')
        plt.title("Exploration Heatmap")
        plt.colorbar()
        plt.show()