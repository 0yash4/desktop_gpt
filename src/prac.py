from pywinauto.application import Application
from pywinauto.mouse import move, click
from pywinauto.keyboard import send_keys
from pywinauto import Desktop

# Connect to the desktop (use visible_only=False to get all windows)
desktop = Desktop(backend="uia")  # or "win32"
for w in desktop.windows():
    print(w.window_text(), w.class_name())
