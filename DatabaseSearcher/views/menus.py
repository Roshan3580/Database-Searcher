# DatabaseSearcher/views/menus.py

import tkinter
import tkinter.filedialog
from DatabaseSearcher.events import *
from .events import *
from .event_handling import EventHandler

_DB_DIALOG_TITLE = 'Select Database File'

class MenuBase(tkinter.Menu, EventHandler):
    def __init__(self, master):
        super().__init__(master, tearoff=0)

class AppMenuBar(MenuBase):
    def __init__(self, master):
        super().__init__(master)
        self.add_cascade(label='File', menu=FileMenu(self))
        self.add_cascade(label='Debug', menu=DebugMenu(self))

    def receive_event(self, evt):
        if isinstance(evt, DBOpenedNotice):
            self.insert_cascade(index=1, label='Edit', menu=EditMenu(self))
        elif isinstance(evt, DBCloseNotice):
            self.delete('Edit')

class FileMenu(MenuBase):
    def __init__(self, master):
        super().__init__(master)
        self.add_command(label='Open', state=tkinter.NORMAL, command=self._open_db)
        self.add_command(label='Close', state=tkinter.DISABLED, command=self._close_db)
        self.add_command(label='Exit', command=self._exit_app)

    def _open_db(self):
        file_path = tkinter.filedialog.askopenfilename(
            title=_DB_DIALOG_TITLE,
            initialdir=Path.cwd())
        if file_path:
            self.send_event(DBOpenRequest(Path(file_path)))

    def _close_db(self):
        self.send_event(DBCloseRequest())

    def _exit_app(self):
        self.send_event(AppQuitRequest())

    def receive_event(self, evt):
        if isinstance(evt, DBOpenedNotice):
            self.entryconfig('Open', state=tkinter.DISABLED)
            self.entryconfig('Close', state=tkinter.NORMAL)
        elif isinstance(evt, DBCloseNotice):
            self.entryconfig('Open', state=tkinter.NORMAL)
            self.entryconfig('Close', state=tkinter.DISABLED)

class EditMenu(MenuBase):
    def __init__(self, master):
        super().__init__(master)
        self.add_command(label='Continents', command=self._edit_continents)
        self.add_command(label='Countries', command=self._edit_countries)
        self.add_command(label='Regions', command=self._edit_regions)

    def _edit_continents(self):
        self.send_event(ShowContinentsPanel())

    def _edit_countries(self):
        self.send_event(ShowCountriesPanel())

    def _edit_regions(self):
        self.send_event(ShowRegionsPanel())

class DebugMenu(MenuBase):
    def __init__(self, master):
        super().__init__(master)
        self._debug_flag = tkinter.IntVar(self, 0)
        self.add_checkbutton(
            label='Show Events', variable=self._debug_flag,
            command=self._toggle_debug)

    def _toggle_debug(self):
        if self._debug_flag.get():
            self.send_event(EnableEventDebug())
        else:
            self.send_event(DisableEventDebug())
