import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gui import menu as menu_gui

if __name__ == "__main__":
    menu_gui.main()