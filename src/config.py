# Configuration parameters for Traffic Vision Analysis

# General
DEFAULT_FPS = 30

# Lane Detection Parameters
CANNY_THRESHOLD_1 = 50
CANNY_THRESHOLD_2 = 150
HOUGH_RHO = 2
HOUGH_THETA = 3.141592653589793 / 180  # np.pi / 180
HOUGH_THRESHOLD = 50
HOUGH_MIN_LINE_LENGTH = 100
HOUGH_MAX_LINE_GAP = 50

# Vehicle Counting Parameters
MOG_HISTORY = 500
MOG_VAR_THRESHOLD = 50
MOG_DETECT_SHADOWS = True
MIN_CONTOUR_AREA = 500
COUNTING_LINE_Y_OFFSET = 0.6  # Percentage of image height where the line is placed
COUNTING_LINE_COLOR = (0, 255, 255) # Yellow
VEHICLE_BOX_COLOR = (0, 255, 0) # Green
