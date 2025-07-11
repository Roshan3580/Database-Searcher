# gui.py
# All Tkinter GUI logic for DatabaseSearcher

import tkinter as tk
from tkinter import messagebox, filedialog
from events import *
from models import Continent, Country, Region

APP_TITLE = 'DatabaseSearcher'
WIN_W, WIN_H = 900, 650

class MainWindow(tk.Tk):
    def __init__(self, event_bus):
        super().__init__()
        self.event_bus = event_bus
        self.geometry(f'{WIN_W}x{WIN_H}')
        self.title(f'{APP_TITLE} - [no database loaded]')
        self.config(menu=MainMenu(self))
        self._active_panel = None
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.show_panel(EmptyPanel(self))

    def send(self, event):
        self.event_bus.dispatch(event)

    def receive(self, event):
        if isinstance(event, DBOpened):
            self.title(f'{APP_TITLE} - {event.path}')
            self.show_panel(EmptyPanel(self))
        elif isinstance(event, DBCloseNotice):
            self.title(f'{APP_TITLE} - [no database loaded]')
            self.show_panel(EmptyPanel(self))
        elif isinstance(event, AppShutdown):
            self.destroy()
        elif isinstance(event, AppError):
            messagebox.showerror('Error', event.message)
        elif isinstance(event, ContinentResult):
            self.show_panel(ContinentPanel(self, event.continent))
        elif isinstance(event, CountryResult):
            self.show_panel(CountryPanel(self, event.country))
        elif isinstance(event, RegionResult):
            self.show_panel(RegionPanel(self, event.region))
        elif isinstance(event, ContinentError):
            messagebox.showerror('Continent Error', event.reason)
        elif isinstance(event, CountryError):
            messagebox.showerror('Country Error', event.reason)
        elif isinstance(event, RegionError):
            messagebox.showerror('Region Error', event.reason)

    def show_panel(self, panel):
        if self._active_panel:
            self._active_panel.destroy()
        self._active_panel = panel
        self._active_panel.grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

class MainMenu(tk.Menu):
    def __init__(self, master):
        super().__init__(master)
        file_menu = tk.Menu(self, tearoff=0)
        file_menu.add_command(label='Open', command=self.open_db)
        file_menu.add_command(label='Close', command=self.close_db)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.exit_app)
        self.add_cascade(label='File', menu=file_menu)
        self.master = master

    def open_db(self):
        path = filedialog.askopenfilename(title='Open Database', filetypes=[('SQLite DB', '*.db *.sqlite *.mdb *.accdb')])
        if path:
            self.master.send(DBOpen(path))

    def close_db(self):
        self.master.send(DBClose())

    def exit_app(self):
        self.master.send(AppExit())

class EmptyPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        label = tk.Label(self, text='No database loaded. Use File > Open to begin.', font=('Arial', 16))
        label.pack(expand=True)

class ContinentPanel(tk.Frame):
    def __init__(self, parent, continent=None):
        super().__init__(parent)
        label = tk.Label(self, text='Continent Panel', font=('Arial', 14))
        label.pack(pady=10)
        # Add continent display/edit widgets here
        # Example:
        if continent:
            info = f"ID: {continent.gid}\nCode: {continent.code}\nName: {continent.name}"
            tk.Label(self, text=info, font=('Arial', 12)).pack(pady=5)

class CountryPanel(tk.Frame):
    def __init__(self, parent, country=None):
        super().__init__(parent)
        label = tk.Label(self, text='Country Panel', font=('Arial', 14))
        label.pack(pady=10)
        if country:
            info = f"ID: {country.gid}\nCode: {country.code}\nName: {country.name}\nContinent ID: {country.continent_id}\nWiki: {country.wiki}\nKeywords: {country.keywords}"
            tk.Label(self, text=info, font=('Arial', 12)).pack(pady=5)

class RegionPanel(tk.Frame):
    def __init__(self, parent, region=None):
        super().__init__(parent)
        label = tk.Label(self, text='Region Panel', font=('Arial', 14))
        label.pack(pady=10)
        if region:
            info = f"ID: {region.gid}\nCode: {region.code}\nLocal: {region.local}\nName: {region.name}\nContinent ID: {region.continent_id}\nCountry ID: {region.country_id}\nWiki: {region.wiki}\nKeywords: {region.keywords}"
            tk.Label(self, text=info, font=('Arial', 12)).pack(pady=5) 