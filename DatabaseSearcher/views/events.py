# DatabaseSearcher/views/events.py



def is_internal_event(event):
    return hasattr(event, '_INTERNAL')



class _InternalEvent:
    def __init__(self):
        self._INTERNAL = True



class ShowEditContinentsViewEvent(_InternalEvent):
    def __init__(self):
        super().__init__()



class ClearContinentsSearchListEvent(_InternalEvent):
    def __init__(self):
        super().__init__()



class NewContinentEvent(_InternalEvent):
    def __init__(self):
        super().__init__()



class StartEditingContinentEvent(_InternalEvent):
    def __init__(self):
        super().__init__()



class DiscardContinentEvent(_InternalEvent):
    def __init__(self):
        super().__init__()



class ShowEditCountriesViewEvent(_InternalEvent):
    def __init__(self):
        super().__init__()



class ClearCountriesSearchListEvent(_InternalEvent):
    def __init__(self):
        super().__init__()



class NewCountryEvent(_InternalEvent):
    def __init__(self):
        super().__init__()



class StartEditingCountryEvent(_InternalEvent):
    def __init__(self):
        super().__init__()



class DiscardCountryEvent(_InternalEvent):
    def __init__(self):
        super().__init__()



class ShowEditRegionsViewEvent(_InternalEvent):
    def __init__(self):
        super().__init__()



class ClearRegionsSearchListEvent(_InternalEvent):
    def __init__(self):
        super().__init__()



class NewRegionEvent(_InternalEvent):
    def __init__(self):
        super().__init__()



class StartEditingRegionEvent(_InternalEvent):
    def __init__(self):
        super().__init__()



class DiscardRegionEvent(_InternalEvent):
    def __init__(self):
        super().__init__()



class EnableDebugModeEvent(_InternalEvent):
    def __init__(self):
        super().__init__()



class DisableDebugModeEvent(_InternalEvent):
    def __init__(self):
        super().__init__()
