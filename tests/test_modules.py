import numpy as np
import pytest
from src.utils import resize_frame
from src.lane_detector import LaneDetector
from src.vehicle_counter import VehicleCounter

def test_resize_frame():
    """Test that resize maintains aspect ratio and sets correct width."""
    mock_frame = np.zeros((1080, 1920, 3), dtype=np.uint8)
    resized = resize_frame(mock_frame, width=800)
    
    assert resized.shape[1] == 800
    # 1080 / 1920 = 0.5625 -> 800 * 0.5625 = 450
    assert resized.shape[0] == 450
    
def test_lane_detector_init():
    """Test lane detector instantiates correctly."""
    ld = LaneDetector()
    assert ld is not None
    
def test_lane_detector_process():
    """Test lane detector processes frame without crashing."""
    ld = LaneDetector()
    mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    out_frame = ld.detect(mock_frame)
    
    assert out_frame.shape == mock_frame.shape
    
def test_vehicle_counter_init():
    """Test vehicle counter instantiates correctly."""
    vc = VehicleCounter()
    assert vc.vehicle_count == 0
    assert vc.line_y is None
    
def test_vehicle_counter_process():
    """Test vehicle counter processes frame without crashing."""
    vc = VehicleCounter()
    mock_frame = np.zeros((480, 640, 3), dtype=np.uint8)
    out_frame = vc.detect_and_count(mock_frame)
    
    assert out_frame.shape == mock_frame.shape
    assert vc.line_y == int(480 * 0.6) # From config OFFSET
