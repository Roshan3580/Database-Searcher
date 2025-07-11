# DatabaseSearcher/views/main.py

import tkinter
import tkinter.messagebox
from DatabaseSearcher.events import *
from .continents import ContinentsView
from .countries import CountriesView
from .empty import EmptyView
from .events import *
from .event_handling import EventHandler
from .menus import MainMenu
from .regions import RegionsView

_WINDOW_W = 800
_WINDOW_H = 600
_APP_TITLE = 'DatabaseSearcher'
_NO_DB = '[no database loaded]'

class AppMainWindow(tkinter.Tk, EventHandler):
    def __init__(self, event_router):
        super().__init__()
        self.geometry(f'{_WINDOW_W}x{_WINDOW_H}')
        self.config(menu=MainMenu(self))
        self._router = event_router
        self._active_view = None
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def send_event(self, evt):
        if is_internal_event(evt):
            self.receive_event(evt)
        else:
            self._router.dispatch(evt)

    def start(self):
        self._change_view(EmptyView(self))
        self._show_db_path(None)
        self.mainloop()

    def receive_event(self, evt):
        if isinstance(evt, ShowEditContinentsViewEvent):
            self._change_view(ContinentsView(self))
        elif isinstance(evt, ShowEditCountriesViewEvent):
            self._change_view(CountriesView(self))
        elif isinstance(evt, ShowEditRegionsViewEvent):
            self._change_view(RegionsView(self))
        elif isinstance(evt, DatabaseOpenedEvent):
            self._show_db_path(evt.path())
        elif isinstance(evt, DatabaseClosedEvent):
            self._show_db_path(None)
            self._change_view(EmptyView(self))
        elif isinstance(evt, DatabaseOpenFailedEvent):
            self._show_db_path(None)
            self._change_view(EmptyView(self))
            tkinter.messagebox.showerror('Database Error', evt.reason())
        elif isinstance(evt, EnableDebugModeEvent):
            self._router.debug_on()
        elif isinstance(evt, DisableDebugModeEvent):
            self._router.debug_off()

    def after_event(self, evt):
        if isinstance(evt, EndApplicationEvent):
            self.destroy()
        elif isinstance(evt, ErrorEvent):
            tkinter.messagebox.showerror('App Error', evt.message())

    def _change_view(self, new_view):
        if self._active_view:
            self._active_view.destroy()
        self._active_view = new_view
        self._active_view.grid(row=0, column=0, sticky=tkinter.NSEW, padx=5, pady=5)

    def _show_db_path(self, db_path):
        if db_path:
            name = db_path.name
        else:
            name = _NO_DB
        self.title(f'{_APP_TITLE} - {name}')
