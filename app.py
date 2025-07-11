# app.py
# Entry point for DatabaseSearcher

from events import EventBus
from backend import DataBackend
from gui import MainWindow


def main():
    bus = EventBus()
    backend = DataBackend()
    window = MainWindow(bus)
    bus.attach_ui(window)
    bus.attach_backend(backend)
    window.mainloop()

if __name__ == '__main__':
    main() 