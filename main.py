# main.py

from DatabaseSearcher import EventDispatcher
from DatabaseSearcher import CoreProcessor
from DatabaseSearcher import AppMainWindow

def launch_app():
    dispatcher = EventDispatcher()
    processor = CoreProcessor()
    window = AppMainWindow(dispatcher)
    dispatcher.attach_engine(processor)
    dispatcher.attach_view(window)
    window.start()

if __name__ == '__main__':
    launch_app()
