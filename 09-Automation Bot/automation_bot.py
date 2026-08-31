import pyautogui
import time
from tasks.file_manager import *
from tasks.browser_tasks import *
from tasks.system_tasks import *

def menu():
    print("\n=== Automation Bot ===")
    print("1. Create Folder")
    print("2. Create File")
    print("3. Rename Item")
    print("4. Delete Item")
    print("5. Take Screenshot")
    print("6. Google Search")
    print("7. Open Website")
    print("8. Mouse Move Demo")
    print("9. Quit")

while True:
    menu()
    choice = input("Choose option: ")

    if choice == "1":
        create_folder(input("Folder name: "))

    elif choice == "2":
        create_file(input("File name: "))

    elif choice == "3":
        rename_item(input("Old name: "), input("New name: "))

    elif choice == "4":
        delete_item(input("Item name to delete: "))

    elif choice == "5":
        take_screenshot()

    elif choice == "6":
        google_search(input("Search query: "))

    elif choice == "7":
        open_website(input("URL: "))

    elif choice == "8":
        system_mouse_demo()

    elif choice == "9":
        print("Goodbye!")
        break

    else:
        print("Invalid option")
