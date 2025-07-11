# main.py

from DatabaseSearcher import AppEventBus
from DatabaseSearcher import DatabaseEngine
from DatabaseSearcher import MainWindow


def main():
    event_bus = AppEventBus()
    engine = DatabaseEngine()
    main_view = MainWindow(event_bus)

    event_bus.register_engine(engine)
    event_bus.register_view(main_view)

    main_view.run()


if __name__ == '__main__':
    main()
