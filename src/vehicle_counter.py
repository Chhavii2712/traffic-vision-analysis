import cv2
import numpy as np
from src.config import *

class VehicleCounter:
    """Class to perform vehicle detection and counting on frames."""
    
    def __init__(self):
        self.bg_subtractor = cv2.createBackgroundSubtractorMOG2(
            history=MOG_HISTORY,
            varThreshold=MOG_VAR_THRESHOLD,
            detectShadows=MOG_DETECT_SHADOWS
        )
        self.vehicle_count = 0
        self.centers = [] # Store centers of detected vehicles
        self.line_y = None

    def _get_center(self, x, y, w, h):
        return (int(x + w / 2), int(y + h / 2))

    def detect_and_count(self, frame: np.ndarray) -> np.ndarray:
        """Processes a frame, counts vehicles crossing a line, and draws boxes."""
        height, width = frame.shape[:2]
        
        # Set the counting line based on image height
        if self.line_y is None:
            self.line_y = int(height * COUNTING_LINE_Y_OFFSET)
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Apply background subtraction
        fg_mask = self.bg_subtractor.apply(gray)
        
        # Thresholding to remove shadows
        _, th = cv2.threshold(fg_mask, 254, 255, cv2.THRESH_BINARY)
        
        # Morphological operations to clean up mask
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        closing = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel)
        opening = cv2.morphologyEx(closing, cv2.MORPH_OPEN, kernel)
        dilation = cv2.dilate(opening, kernel, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        valid_centers = []
        
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > MIN_CONTOUR_AREA:
                x, y, w, h = cv2.boundingRect(cnt)
                center = self._get_center(x, y, w, h)
                valid_centers.append(center)
                
                # Draw bounding box and center
                cv2.rectangle(frame, (x, y), (x + w, y + h), VEHICLE_BOX_COLOR, 2)
                cv2.circle(frame, center, 4, (0, 0, 255), -1)
                
        # Counting logic
        for center in valid_centers:
            cx, cy = center
            # Check if vehicle crossed the line (allowing a small margin)
            if (self.line_y - 6) < cy < (self.line_y + 6):
                # Ensure we haven't already counted this vehicle recently
                already_counted = False
                for old_cx, old_cy in self.centers:
                    # If an existing center is close, we already counted it
                    if abs(cx - old_cx) < 50 and abs(cy - old_cy) < 50:
                        already_counted = True
                        break
                        
                if not already_counted:
                    self.vehicle_count += 1
                    # Draw a line indicator that a count happened
                    cv2.line(frame, (0, self.line_y), (width, self.line_y), (0, 0, 255), 5)
                    
        # Update history of centers to prevent double counting
        self.centers = valid_centers
        
        # Draw the base counting line
        cv2.line(frame, (0, self.line_y), (width, self.line_y), COUNTING_LINE_COLOR, 2)
        
        # Put count text on frame
        cv2.putText(frame, f"Vehicle Count: {self.vehicle_count}", (50, 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
                    
        return frame
