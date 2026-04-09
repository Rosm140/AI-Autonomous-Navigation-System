import cv2
import numpy as np


class VisionSystem:
    def __init__(self, source=0):
        """
        source:
        0 → webcam
        or path to image/video file
        """
        self.cap = cv2.VideoCapture(source)

    def detect_color_objects(self):
        """Detect red-colored objects (simple obstacle simulation)"""

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            # Convert to HSV color space
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # Define red color range
            lower_red1 = np.array([0, 120, 70])
            upper_red1 = np.array([10, 255, 255])

            lower_red2 = np.array([170, 120, 70])
            upper_red2 = np.array([180, 255, 255])

            # Mask for red
            mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
            mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

            mask = mask1 + mask2
            kernel = np.ones((5, 5), np.uint8)
            mask = cv2.dilate(mask, kernel, iterations=2)
            mask = cv2.erode(mask, kernel, iterations=1)
            # Find contours (detected objects)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                area = cv2.contourArea(cnt)

                if area > 1500:  # filter noise
                    x, y, w, h = cv2.boundingRect(cnt)

                    # Draw rectangle
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(frame, f"Obstacle ({area})", (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Show frames
            cv2.imshow("Camera Feed", frame)
            cv2.imshow("Mask", mask)

            # Exit key
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()


# 🔹 Test run
if __name__ == "__main__":
    vision = VisionSystem(0)  # webcam
    vision.detect_color_objects()