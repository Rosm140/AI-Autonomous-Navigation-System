import os
import matplotlib.pyplot as plt


class OutputSaver:
    def __init__(self):
        self.base_path = "outputs"

        self.image_path = os.path.join(self.base_path, "images")
        self.frame_path = os.path.join(self.base_path, "frames")
        self.log_path = os.path.join(self.base_path, "logs")

        self._create_dirs()

    def _create_dirs(self):
        os.makedirs(self.image_path, exist_ok=True)
        os.makedirs(self.frame_path, exist_ok=True)
        os.makedirs(self.log_path, exist_ok=True)

    def save_final_path_image(self, grid, path, start, goal):
        """Save final path visualization"""
        plt.figure(figsize=(6, 6))
        plt.imshow(grid, cmap='gray_r')

        if path:
            y = [p[0] for p in path]
            x = [p[1] for p in path]
            plt.plot(x, y, color='red', linewidth=2)

        plt.scatter(start[1], start[0], c='green', s=100)
        plt.scatter(goal[1], goal[0], c='blue', s=100)

        file_path = os.path.join(self.image_path, "final_path.png")
        plt.title("Final Path")
        plt.savefig(file_path)
        plt.close()

        print(f"📸 Saved final path image: {file_path}")

    def save_frame(self, frame_index):
        """Save current matplotlib frame"""
        file_path = os.path.join(self.frame_path, f"frame_{frame_index}.png")
        plt.savefig(file_path)

    def save_logs(self, path):
        """Save path and steps"""
        file_path = os.path.join(self.log_path, "path_log.txt")

        with open(file_path, "w") as f:
            f.write("Path Coordinates:\n")
            for step in path:
                f.write(f"{step}\n")

            f.write(f"\nTotal Steps: {len(path)}\n")

        print(f"📝 Saved log file: {file_path}")