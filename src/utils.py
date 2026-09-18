import cv2
import numpy as np

def resize_frame(frame: np.ndarray, width: int = 800) -> np.ndarray:
    """Resize an image maintaining aspect ratio."""
    h, w = frame.shape[:2]
    aspect_ratio = h / w
    new_h = int(width * aspect_ratio)
    return cv2.resize(frame, (width, new_h))

def region_of_interest(img: np.ndarray, vertices: np.ndarray) -> np.ndarray:
    """
    Applies an image mask.
    Only keeps the region of the image defined by the polygon
    formed from `vertices`. The rest of the image is set to black.
    """
    mask = np.zeros_like(img)
    # Define a 3 channel or 1 channel color to fill the mask with depending on the input image
    if len(img.shape) > 2:
        channel_count = img.shape[2]
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255
        
    # filling pixels inside the polygon defined by "vertices" with the fill color    
    cv2.fillPoly(mask, vertices, ignore_mask_color)
    
    # returning the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)
    return masked_image

def draw_lines(img: np.ndarray, lines: np.ndarray, color=(0, 0, 255), thickness=3) -> np.ndarray:
    """
    Draws lines on an image.
    """
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    if lines is not None:
        for line in lines:
            for x1, y1, x2, y2 in line:
                cv2.line(line_img, (x1, y1), (x2, y2), color, thickness)
    
    return cv2.addWeighted(img, 1.0, line_img, 0.9, 0.0)
