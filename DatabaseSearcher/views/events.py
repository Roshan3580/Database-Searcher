# DatabaseSearcher/views/events.py

def is_ui_event(evt):
    return hasattr(evt, '_UI_EVENT')

class _UIEventBase:
    def __init__(self):
        self._UI_EVENT = True

class ShowContinentsPanel(_UIEventBase):
    def __init__(self):
        super().__init__()

class ClearContinentResults(_UIEventBase):
    def __init__(self):
        super().__init__()

class AddContinentRequest(_UIEventBase):
    def __init__(self):
        super().__init__()

class BeginContinentEdit(_UIEventBase):
    def __init__(self):
        super().__init__()

class CancelContinentEdit(_UIEventBase):
    def __init__(self):
        super().__init__()

class ShowCountriesPanel(_UIEventBase):
    def __init__(self):
        super().__init__()

class ClearCountryResults(_UIEventBase):
    def __init__(self):
        super().__init__()

class AddCountryRequest(_UIEventBase):
    def __init__(self):
        super().__init__()

class BeginCountryEdit(_UIEventBase):
    def __init__(self):
        super().__init__()

class CancelCountryEdit(_UIEventBase):
    def __init__(self):
        super().__init__()

class ShowRegionsPanel(_UIEventBase):
    def __init__(self):
        super().__init__()

class ClearRegionResults(_UIEventBase):
    def __init__(self):
        super().__init__()

class AddRegionRequest(_UIEventBase):
    def __init__(self):
        super().__init__()

class BeginRegionEdit(_UIEventBase):
    def __init__(self):
        super().__init__()

class CancelRegionEdit(_UIEventBase):
    def __init__(self):
        super().__init__()

class EnableEventDebug(_UIEventBase):
    def __init__(self):
        super().__init__()

class DisableEventDebug(_UIEventBase):
    def __init__(self):
        super().__init__()
