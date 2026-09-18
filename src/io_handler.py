import cv2
import os
import sys

class IOHandler:
    """Handles reading from video files/images and writing outputs."""
    
    def __init__(self, input_path: str, output_path: str = None):
        self.input_path = input_path
        self.output_path = output_path
        self.is_video = False
        self.cap = None
        self.out = None
        
        self._init_io()
        
    def _init_io(self):
        if not os.path.exists(self.input_path):
            raise FileNotFoundError(f"Input path does not exist: {self.input_path}")
            
        # Basic check if it's an image or video based on extension
        ext = os.path.splitext(self.input_path)[1].lower()
        if ext in ['.mp4', '.avi', '.mov', '.mkv']:
            self.is_video = True
            self.cap = cv2.VideoCapture(self.input_path)
            if not self.cap.isOpened():
                raise ValueError("Could not open video file.")
        elif ext in ['.jpg', '.jpeg', '.png', '.bmp']:
            self.is_video = False
        else:
            raise ValueError(f"Unsupported file format: {ext}")
            
    def setup_video_writer(self, frame_size, fps=30):
        if self.output_path and self.is_video:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            self.out = cv2.VideoWriter(self.output_path, fourcc, fps, frame_size)
            
    def read_frame(self):
        """Generator that yields frames."""
        if self.is_video:
            while self.cap.isOpened():
                ret, frame = self.cap.read()
                if not ret:
                    break
                yield frame
        else:
            frame = cv2.imread(self.input_path)
            if frame is not None:
                yield frame

    def write_frame(self, frame):
        """Writes frame to output video if writer is initialized."""
        if self.out:
            self.out.write(frame)
        elif self.output_path and not self.is_video:
            cv2.imwrite(self.output_path, frame)
            
    def close(self):
        """Releases resources."""
        if self.cap:
            self.cap.release()
        if self.out:
            self.out.release()
