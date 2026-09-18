import cv2
import sys
from src.io_handler import IOHandler
from src.lane_detector import LaneDetector
from src.vehicle_counter import VehicleCounter
from src.config import DEFAULT_FPS

class VisionPipeline:
    """Orchestrates the entire CV pipeline."""
    
    def __init__(self, input_path: str, output_path: str, tasks: list):
        self.io = IOHandler(input_path, output_path)
        self.tasks = tasks
        
        self.lane_detector = None
        self.vehicle_counter = None
        
        if 'lane' in self.tasks:
            self.lane_detector = LaneDetector()
        if 'vehicle' in self.tasks:
            self.vehicle_counter = VehicleCounter()
            
    def run(self, display: bool = False):
        """Runs the vision pipeline over the input."""
        
        # Read first frame to setup writer properly
        gen = self.io.read_frame()
        try:
            first_frame = next(gen)
        except StopIteration:
            print("No frames found in the input.")
            return

        h, w = first_frame.shape[:2]
        self.io.setup_video_writer(frame_size=(w, h), fps=DEFAULT_FPS)
        
        print(f"Starting processing... (Input: {self.io.input_path})")
        print(f"Tasks: {self.tasks}")
        
        frame_idx = 0
        # Process first frame
        self._process_and_write(first_frame, display)
        
        # Process remaining frames
        for frame in gen:
            frame_idx += 1
            if frame_idx % 30 == 0:
                print(f"Processed {frame_idx} frames...")
            self._process_and_write(frame, display)
            
        print("Processing complete!")
        if self.vehicle_counter:
            print(f"Final Vehicle Count: {self.vehicle_counter.vehicle_count}")
            
        self.io.close()
        cv2.destroyAllWindows()
        
    def _process_and_write(self, frame, display):
        processed = frame.copy()
        
        if self.lane_detector:
            processed = self.lane_detector.detect(processed)
            
        if self.vehicle_counter:
            processed = self.vehicle_counter.detect_and_count(processed)
            
        if display:
            cv2.imshow('Traffic Vision Analysis', processed)
            # Break on 'q' press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                self.io.close()
                cv2.destroyAllWindows()
                sys.exit(0)
                
        self.io.write_frame(processed)
