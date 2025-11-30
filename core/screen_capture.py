import mss
import mss.tools
import numpy as np
import time
from typing import Optional, Tuple
from PIL import Image
from config.settings import MONITOR_INDEX

class ScreenCapture:
    def __init__(self, monitor_index: int = MONITOR_INDEX):
        """
        Initialize screen capture.
        :param monitor_index: Index of the monitor to capture (1-based).
        """
        self.monitor_index = monitor_index
        self.sct = mss.mss()
        
        # Validate monitor index
        if self.monitor_index > len(self.sct.monitors) - 1:
            raise ValueError(f"Monitor index {self.monitor_index} out of range. Available: {len(self.sct.monitors) - 1}")
        
        self.monitor = self.sct.monitors[self.monitor_index]
        print(f"Initialized ScreenCapture on Monitor {self.monitor_index}: {self.monitor}")

    def capture(self, save_path: Optional[str] = None) -> Image.Image:
        """
        Capture the screen.
        :param save_path: Optional path to save the screenshot.
        :return: PIL Image object.
        """
        # Capture the screen
        sct_img = self.sct.grab(self.monitor)
        
        # Convert to PIL Image
        img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
        
        if save_path:
            img.save(save_path)
            
        return img

    def capture_numpy(self) -> np.ndarray:
        """
        Capture the screen and return as a numpy array (OpenCV compatible).
        :return: Numpy array (BGR format).
        """
        sct_img = self.sct.grab(self.monitor)
        return np.array(sct_img)

    def close(self):
        self.sct.close()

if __name__ == "__main__":
    # Simple test
    try:
        cap = ScreenCapture()
        print("Capturing screen...")
        img = cap.capture("test_screenshot.png")
        print(f"Screenshot saved to test_screenshot.png, size: {img.size}")
        cap.close()
    except Exception as e:
        print(f"Error: {e}")
