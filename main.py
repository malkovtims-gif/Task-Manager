#!/usr/bin/env python3
from controllers.menu_controller import MenuController

def main():
    try:
        app = MenuController()
        app.run()
    except KeyboardInterrupt:
        print("\n\n⚠️ Application interrupted.")

if __name__ == "__main__":
    main()
