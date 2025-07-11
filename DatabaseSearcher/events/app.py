# DatabaseSearcher/events/app.py

class AppErrorEvent:
    def __init__(self, msg: str):
        self._msg = msg
    def get_message(self) -> str:
        return self._msg
    def __repr__(self) -> str:
        return f'{type(self).__name__}: msg = {repr(self._msg)}'

class AppQuitRequest:
    def __repr__(self) -> str:
        return f'{type(self).__name__}'

class AppShutdownEvent:
    def __repr__(self) -> str:
        return f'{type(self).__name__}'
