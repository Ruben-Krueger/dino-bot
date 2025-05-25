from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from PIL import Image
import numpy as np
import io
import traceback
import sys
import base64

class DinoPlayer:
    def __init__(self):
        try:
            # Initialize Chrome driver
            self.driver = webdriver.Chrome()
            self.driver.get("https://chromedino.com/")
            # Set window size for consistent gameplay
            self.driver.set_window_size(800, 400)
        except Exception as e:
            print("\nError during initialization:")
            traceback.print_exc()
            sys.exit(1)
        
    def start_game(self):
        try:
            # Wait for the game to load
            time.sleep(2)
            # Press space to start
            actions = ActionChains(self.driver)
            actions.send_keys(Keys.SPACE).perform()
            print("Game started!")
            
            while True:
                try:
                    # Get the game canvas
                    canvas = self.driver.find_element(By.TAG_NAME, "canvas")
                    
                    # Take a screenshot of the canvas
                    canvas_base64 = self.driver.execute_script(
                        "return arguments[0].toDataURL('image/png').substring(22);", 
                        canvas
                    )
                    
                    # Decode base64 image
                    image_data = base64.b64decode(canvas_base64)
                    
                    # Convert the screenshot to a PIL Image
                    screenshot = Image.open(io.BytesIO(image_data))
                    
                    # Convert to grayscale
                    gray = screenshot.convert('L')
                    
                    # Get the pixel data
                    pixels = np.array(gray)
                    
                    # Define the region to check for obstacles (adjust these values based on testing)
                    obstacle_region = pixels[150:200, 100:200]
                    
                    # If we detect dark pixels (obstacles) in our region of interest
                    if np.any(obstacle_region < 100):  # Threshold for dark pixels
                        print("Obstacle detected")
                        # Jump!
                        actions.send_keys(Keys.SPACE).perform()
                        print("Jumped")
                        time.sleep(0.1)  # Small delay to prevent multiple jumps
                    
                    time.sleep(0.01)  # Small delay to prevent excessive CPU usage
                    
                except Exception as e:
                    print("\nError during gameplay loop:")
                    traceback.print_exc()
                    break
                
        except Exception as e:
            print("\nError during game startup:")
            traceback.print_exc()
        finally:
            try:
                self.driver.quit()
            except Exception as e:
                print("\nError while closing browser:")
                traceback.print_exc()

if __name__ == "__main__":
    try:
        player = DinoPlayer()
        player.start_game()
    except Exception as e:
        print("\nUnhandled error:")
        traceback.print_exc()
        sys.exit(1) 