import argparse
import sys
from src.pipeline import VisionPipeline

def parse_args():
    parser = argparse.ArgumentParser(description="Traffic Vision Analysis CLI")
    
    parser.add_argument("-i", "--input", required=True, 
                        help="Path to input video or image file")
                        
    parser.add_argument("-o", "--output", required=False, default=None,
                        help="Path to save output video or image")
                        
    parser.add_argument("--tasks", nargs="+", choices=['lane', 'vehicle'], 
                        required=True,
                        help="Tasks to perform. E.g., --tasks lane vehicle")
                        
    parser.add_argument("--display", action="store_true",
                        help="Show video preview window while processing (press 'q' to quit)")
                        
    return parser.parse_args()

def main():
    args = parse_args()
    
    print("="*50)
    print("Traffic Vision Analysis CLI")
    print("="*50)
    
    try:
        pipeline = VisionPipeline(
            input_path=args.input,
            output_path=args.output,
            tasks=args.tasks
        )
        
        pipeline.run(display=args.display)
        
    except Exception as e:
        print(f"Error during execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
