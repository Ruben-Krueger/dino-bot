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

class Obstacle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

class Position:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        
class DinoPlayer:
    def __init__(self, ui_callback=None):
        try:
            self.ui_callback = ui_callback if ui_callback else print
            # Initialize Chrome driver
            self.driver = webdriver.Chrome()
            self.driver.get("https://chromedino.com/")

            # Set window size for consistent gameplay
            self.driver.set_window_size(800, 400)
            self.running = False

            self.obstacles = []
            self.dino_position = None
            
            # Initialize ActionChains as a class property
            self.actions = ActionChains(self.driver)

        
        except Exception as e:
            self.ui_callback("\nError during initialization:")
            traceback.print_exc()
            sys.exit(1)
        
    def log(self, message):
        self.ui_callback(message)
        
    def stop_game(self):
        self.running = False
        try:
            self.driver.quit()
        except Exception as e:
            self.log("\nError while closing browser:")
            traceback.print_exc()


    def get_screenshot(self):
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
        return screenshot

    def get_game_state(self):
        return {
            'obstacles': self.obstacles,
            'dino_position': self.dino_position,
            'is_running': self.running
            }


    def get_pixel_data(self, screenshot):
        # Convert to grayscale
        gray = screenshot.convert('L')
        
        # Get the pixel data
        pixels = np.array(gray)
        return pixels

    def get_elements(self, pixels):
        pass

    def did_round_end(self, pixels):
        pass


    def play_round(self):
        screenshot = self.get_screenshot()

        self.log("Captured screenshot")

        pixels = self.get_pixel_data(screenshot)

        elements = self.get_elements(pixels)
        
        # Define the region to check for obstacles (adjust these values based on testing)
        obstacle_region = pixels[150:200, 100:200]
        
        # If we detect dark pixels (obstacles) in our region of interest
        # This is currently dumb and detects the dino player as an obstacle
        if np.any(obstacle_region < 100):  # Threshold for dark pixels
            self.log("Obstacle detected")
            # Jump!
            self.actions.send_keys(Keys.SPACE).perform()
            self.log("Jumped")
            time.sleep(0.1)  # Small delay to prevent multiple jumps
        
        time.sleep(0.01)  # Small delay to prevent excessive CPU usage
    
    def start_game(self):
        try:
            self.running = True
            # Wait for the game to load
            time.sleep(2)
            # Press space to start
            self.actions.send_keys(Keys.SPACE).perform()
            self.log("Game started!")
                
        except Exception as e:
            self.log(f"Error during game startup: {e}")
            traceback.print_exc()


    def play_game(self):
        self.log("Playing game")

        while self.running:
            try:
                self.play_round()
            except Exception as e:
                self.log("\nError during gameplay loop:")
                traceback.print_exc()
                self.stop_game()  # Only stop the game if there's an error

                break  # Only break on error

if __name__ == "__main__":
    try:
        player = DinoPlayer()
        player.start_game()
        player.play_game()
    except Exception as e:
        print("\nUnhandled error:")
        traceback.print_exc()
        sys.exit(1) 