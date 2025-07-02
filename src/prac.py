import pyautogui


def get_screen_resolution():
    """
    Returns the screen resolution as a tuple (width, height).
    """
    screen_width, screen_height = pyautogui.size()  # Returns screen resolution (e.g., 1920, 1080)
    return screen_width, screen_height

def get_mouse_position():
    """
    Returns the current mouse position as a tuple (x, y).
    """
    mouse_x, mouse_y = pyautogui.position()  # Returns current mouse position
    return mouse_x, mouse_y

def locate_image(image_path, confidence=0.8):
    """
    Locates an image on the screen and returns its position as a tuple (x, y).
    If the image is not found, returns None.
    """
    try:
        position = pyautogui.locateCenterOnScreen(image_path, confidence=confidence)
        if position is not None:
            return position.x, position.y
        else:
            return None
    except Exception as e:
        print(f"Error locating image: {e}")
        return None

def move_mouse(x, y):
    """
    Moves the mouse to the specified (x, y) coordinates.
    """
    pyautogui.moveTo(x, y, duration=0.5)
    
import time

import pyautogui

# Optional: Add a delay between actions for stability
pyautogui.PAUSE = 0.5

def navigate_to_chrome_icon(image_path):
    try:
        # Ensure the screen is in the correct state (e.g., desktop visible)
        print("Looking for Chrome icon...")
        
        # Locate the center of the Chrome icon on the screen
        location = pyautogui.locateCenterOnScreen(image_path, confidence=0.8)
        
        if location:
            x, y = location
            print(f"Found Chrome icon at: ({x}, {y})")
            
            # Move the mouse to the icon's coordinates
            pyautogui.moveTo(x, y, duration=0.5)
            return f"Mouse moved to Chrome icon at ({x}, {y})"
        else:
            return "Chrome icon not found on the screen"
    except Exception as e:
        return f"Error: {str(e)}"


if __name__ == "__main__":
    # Example usage
    print("Screen Resolution:", get_screen_resolution())
    print("Mouse Position:", get_mouse_position())
    
    # Navigate to Chrome icon
    result = navigate_to_chrome_icon('chrome_icon.png')
    print(result)
    
    # Move mouse to a specific position (example)
    move_mouse(100, 200)
    print("Mouse moved to (100, 200)")
    
    # Locate an image on the screen
    image_position = locate_image('E:\Projects\desktop_gpt\image.png', confidence=0.8)
    if image_position:
        print(f"Image found at: {image_position}")
    else:
        print("Image not found")