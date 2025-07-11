# DatabaseSearcher/events/database.py

from pathlib import Path

class DBOpenRequest:
    def __init__(self, db_path: Path):
        self._db_path = db_path
    def get_path(self) -> Path:
        return self._db_path
    def __repr__(self) -> str:
        return f'{type(self).__name__}: db_path = {repr(self._db_path)}'

class DBCloseRequest:
    def __repr__(self) -> str:
        return f'{type(self).__name__}'

class DBOpenedNotice:
    def __init__(self, db_path: Path):
        self._db_path = db_path
    def get_path(self) -> Path:
        return self._db_path
    def __repr__(self) -> str:
        return f'{type(self).__name__}: db_path = {repr(self._db_path)}'

class DBOpenFailedNotice:
    def __init__(self, reason: str):
        self._reason = reason
    def get_reason(self) -> str:
        return self._reason
    def __repr__(self) -> str:
        return f'{type(self).__name__}: reason = {repr(self._reason)}'

class DBCloseNotice:
    def __repr__(self) -> str:
        return f'{type(self).__name__}'
