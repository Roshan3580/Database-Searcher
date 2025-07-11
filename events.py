# events.py
# All event classes and the event bus for DatabaseSearcher

class AppExit: pass
class AppShutdown: pass
class AppError:
    def __init__(self, message):
        self.message = message
class DBOpen:
    def __init__(self, path):
        self.path = path
class DBOpened:
    def __init__(self, path):
        self.path = path
class DBClose: pass
class DBCloseNotice: pass

# Continent events
class ContinentQuery:
    def __init__(self, code=None, name=None):
        self.code = code
        self.name = name
class ContinentFetch:
    def __init__(self, gid):
        self.gid = gid
class ContinentAdd:
    def __init__(self, continent):
        self.continent = continent
class ContinentEdit:
    def __init__(self, continent):
        self.continent = continent
class ContinentResult:
    def __init__(self, continent):
        self.continent = continent
class ContinentError:
    def __init__(self, reason):
        self.reason = reason

# Country events
class CountryQuery:
    def __init__(self, code=None, name=None):
        self.code = code
        self.name = name
class CountryFetch:
    def __init__(self, gid):
        self.gid = gid
class CountryAdd:
    def __init__(self, country):
        self.country = country
class CountryEdit:
    def __init__(self, country):
        self.country = country
class CountryResult:
    def __init__(self, country):
        self.country = country
class CountryError:
    def __init__(self, reason):
        self.reason = reason

# Region events
class RegionQuery:
    def __init__(self, code=None, local=None, name=None):
        self.code = code
        self.local = local
        self.name = name
class RegionFetch:
    def __init__(self, gid):
        self.gid = gid
class RegionAdd:
    def __init__(self, region):
        self.region = region
class RegionEdit:
    def __init__(self, region):
        self.region = region
class RegionResult:
    def __init__(self, region):
        self.region = region
class RegionError:
    def __init__(self, reason):
        self.reason = reason

# Event bus/router
class EventBus:
    def __init__(self):
        self._ui = None
        self._backend = None
        self._debug = False
    def attach_ui(self, ui):
        self._ui = ui
    def attach_backend(self, backend):
        self._backend = backend
    def debug_on(self):
        self._debug = True
    def debug_off(self):
        self._debug = False
    def dispatch(self, event):
        if self._debug:
            print(f'[UI->Backend] {event}')
        for resp in self._backend.process(event):
            if self._debug:
                print(f'[Backend->UI] {resp}')
            self._ui.receive(resp) 