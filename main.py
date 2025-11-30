import time
import cv2
import threading
from queue import Queue
from PIL import Image
from core.screen_capture import ScreenCapture
from core.vision_model import VisionModel
from config.settings import CAPTURE_FPS

def main_loop():
    print("Starting GameVoiceAI...")
    
    # Initialize modules
    try:
        screen_cap = ScreenCapture()
        vision_model = VisionModel()
    except Exception as e:
        print(f"Initialization failed: {e}")
        return

    # Control flags
    running = True
    
    # Queues for communication (optional for now, good for future)
    # image_queue = Queue(maxsize=1)
    
    print(f"Press Ctrl+C to stop. Capturing at {CAPTURE_FPS} FPS.")

    last_capture_time = 0
    capture_interval = 1.0 / CAPTURE_FPS

    try:
        while running:
            current_time = time.time()
            
            # Rate limiting
            if current_time - last_capture_time >= capture_interval:
                last_capture_time = current_time
                
                # 1. Capture Screen
                image = screen_cap.capture()
                
                # Optional: Show preview window (using OpenCV)
                # Convert PIL to OpenCV for display
                # cv_img = screen_cap.capture_numpy()
                # cv2.imshow("GameVoiceAI Preview", cv_img)
                # if cv2.waitKey(1) & 0xFF == ord('q'):
                #     break

                # 2. Analyze Image (Simple synchronous call for Phase 1)
                # Note: In a real scenario, this should be async or in a separate thread
                # to avoid blocking the capture loop if FPS is high.
                # For now, we print "Analyzing..." and wait.
                
                print("\n[System] Capturing frame...")
                
                # Skip analysis if API key is not set (to prevent errors in loop)
                if vision_model.client.api_key:
                    print("[AI] Analyzing image...")
                    description = vision_model.analyze_image(image, "Describe what is happening on the screen in one sentence.")
                    print(f"[AI]: {description}")
                else:
                    print("[System] API Key not found. Skipping analysis.")
            
            # Sleep briefly to reduce CPU usage
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        screen_cap.close()
        cv2.destroyAllWindows()
        print("GameVoiceAI Stopped.")

if __name__ == "__main__":
    main_loop()
