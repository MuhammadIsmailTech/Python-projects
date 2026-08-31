import pyautogui
import time

def take_screenshot():
    img = pyautogui.screenshot()
    filename = "screenshot.png"
    img.save(filename)
    print("Screenshot saved as:", filename)

def system_mouse_demo():
    print("Moving mouse in 3 seconds...")
    time.sleep(3)
    pyautogui.moveTo(200, 200, 1)
    pyautogui.moveTo(600, 400, 1)
    pyautogui.click()
    print("Mouse movement done.")
