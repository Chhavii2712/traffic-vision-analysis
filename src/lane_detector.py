import cv2
import numpy as np
from src.config import *
from src.utils import region_of_interest, draw_lines

class LaneDetector:
    """Class to perform lane detection on frames."""
    
    def __init__(self):
        pass

    def detect(self, frame: np.ndarray) -> np.ndarray:
        """Processes a frame and returns it with lane lines drawn."""
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Blur the image for better edge detection
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Canny edge detection
        edges = cv2.Canny(blur, CANNY_THRESHOLD_1, CANNY_THRESHOLD_2)
        
        # Define region of interest (lower half of the image usually)
        height, width = edges.shape
        roi_vertices = np.array([[(0, height), (width / 2, height / 2 + 50), (width, height)]], dtype=np.int32)
        
        masked_edges = region_of_interest(edges, roi_vertices)
        
        # Hough Line Transform
        lines = cv2.HoughLinesP(
            masked_edges,
            rho=HOUGH_RHO,
            theta=HOUGH_THETA,
            threshold=HOUGH_THRESHOLD,
            minLineLength=HOUGH_MIN_LINE_LENGTH,
            maxLineGap=HOUGH_MAX_LINE_GAP
        )
        
        # Draw lines on original frame
        line_image = np.zeros_like(frame)
        if lines is not None:
            for x1, y1, x2, y2 in lines.reshape(-1, 4):
                cv2.line(line_image, (x1, y1), (x2, y2), (255, 0, 0), 5) # Blue lines
                
        # Combine the line image with original frame
        combined = cv2.addWeighted(frame, 0.8, line_image, 1.0, 0.0)
        return combined
