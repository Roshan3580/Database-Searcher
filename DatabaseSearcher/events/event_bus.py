# DatabaseSearcher/events/event_bus.py

class EventRouter:
    def __init__(self):
        self._ui = None
        self._core = None
        self._debug = False
    def attach_ui(self, ui):
        self._ui = ui
    def attach_core(self, core):
        self._core = core
    def debug_on(self):
        self._debug = True
    def debug_off(self):
        self._debug = False
    def dispatch(self, evt):
        if self._debug:
            print(f'[UI->Core] {evt}')
        for resp in self._core.handle_event(evt):
            if self._debug:
                print(f'[Core->UI] {resp}')
            self._ui.receive_event(resp)
