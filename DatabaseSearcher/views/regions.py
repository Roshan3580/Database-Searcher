# DatabaseSearcher/views/regions.py

import tkinter
import tkinter.messagebox
from DatabaseSearcher.events import *
from .event_handling import EventHandler
from .events import *

class RegionPanel(tkinter.Frame, EventHandler):
    def __init__(self, parent):
        super().__init__(parent)
        search_box = RegionSearchBox(self)
        search_box.grid(row=0, column=0, sticky=tkinter.NSEW)
        self._editor = None
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

    def receive_event(self, evt):
        if isinstance(evt, SaveRegionFailedEvent):
            tkinter.messagebox.showerror('Region Save Error', evt.reason())

    def after_event(self, evt):
        if isinstance(evt, CancelRegionEdit):
            self._swap_editor(None)
        elif isinstance(evt, AddRegionRequest):
            self._swap_editor(RegionEditor(self, True, True, None))
        elif isinstance(evt, BeginRegionEdit):
            self._swap_editor(RegionLoading(self))
        elif isinstance(evt, RegionLoadedEvent):
            self._swap_editor(RegionEditor(self, False, True, evt.region()))
        elif isinstance(evt, RegionSavedEvent):
            self._swap_editor(RegionEditor(self, False, False, evt.region()))

    def _swap_editor(self, editor):
        if self._editor:
            self._editor.destroy()
            self._editor = None
        if editor:
            self._editor = editor
            self._editor.grid(row=1, column=0, padx=5, pady=5, sticky=tkinter.NSEW)

class RegionSearchBox(tkinter.LabelFrame, EventHandler):
    def __init__(self, parent):
        super().__init__(parent, text='Find Region')
        code_lbl = tkinter.Label(self, text='Region Code:')
        code_lbl.grid(row=0, column=0, padx=5, pady=5, sticky=tkinter.E)
        self._code_var = tkinter.StringVar()
        self._code_var.trace_add('write', self._on_change)
        code_entry = tkinter.Entry(self, textvariable=self._code_var, width=10)
        code_entry.grid(row=0, column=1, sticky=tkinter.W, padx=5, pady=5)
        local_lbl = tkinter.Label(self, text='Local Code:')
        local_lbl.grid(row=1, column=0, padx=5, pady=5, sticky=tkinter.E)
        self._local_var = tkinter.StringVar()
        self._local_var.trace_add('write', self._on_change)
        local_entry = tkinter.Entry(self, textvariable=self._local_var, width=10)
        local_entry.grid(row=1, column=1, sticky=tkinter.W, padx=5, pady=5)
        name_lbl = tkinter.Label(self, text='Region Name:')
        name_lbl.grid(row=2, column=0, sticky=tkinter.E, padx=5, pady=5)
        self._name_var = tkinter.StringVar()
        self._name_var.trace_add('write', self._on_change)
        name_entry = tkinter.Entry(self, textvariable=self._name_var, width=30)
        name_entry.grid(row=2, column=1, sticky=tkinter.EW, padx=5, pady=5)
        self._search_btn = tkinter.Button(self, text='Find', state=tkinter.DISABLED, command=self._do_search)
        self._search_btn.grid(row=3, column=1, sticky=tkinter.E, padx=5, pady=5)
        spacer = tkinter.Label(self, text='')
        spacer.grid(row=4, column=1, sticky=tkinter.NSEW, padx=5, pady=5)
        self._listbox = tkinter.Listbox(self, height=4, activestyle=tkinter.NONE, selectmode=tkinter.SINGLE)
        self._listbox.bind('<<ListboxSelect>>', self._on_select)
        self._listbox.grid(row=0, column=2, rowspan=4, columnspan=1, sticky=tkinter.NSEW, padx=5, pady=5)
        self._ids = []
        btn_frame = tkinter.Frame(self)
        btn_frame.grid(row=5, column=2, sticky=tkinter.E, padx=5, pady=5)
        self._new_btn = tkinter.Button(btn_frame, text='Add New', command=self._new)
        self._new_btn.grid(row=0, column=0, padx=5, pady=5)
        self._edit_btn = tkinter.Button(btn_frame, text='Edit Selected', state=tkinter.DISABLED, command=self._edit)
        self._edit_btn.grid(row=0, column=1, padx=5, pady=5)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=0)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=2)

    def _do_search(self):
        self.send_event(ClearRegionResults())
        self.send_event(StartRegionSearchEvent(self._get_code(), self._get_local(), self._get_name()))

    def _get_code(self):
        code = self._code_var.get().strip()
        return code if code else None

    def _get_local(self):
        local = self._local_var.get().strip()
        return local if local else None

    def _get_name(self):
        name = self._name_var.get().strip()
        return name if name else None

    def _get_selected_id(self):
        idx, *_ = self._listbox.curselection()
        return self._ids[idx]

    def _on_change(self, *args):
        if self._code_var.get().strip() or self._local_var.get().strip() or self._name_var.get().strip():
            self._search_btn['state'] = tkinter.NORMAL
        else:
            self._search_btn['state'] = tkinter.DISABLED
        return True

    def _on_select(self, event):
        if event.widget.curselection():
            self._edit_btn['state'] = tkinter.NORMAL
        else:
            self._edit_btn['state'] = tkinter.DISABLED

    def _new(self):
        self.send_event(CancelRegionEdit())
        self.send_event(AddRegionRequest())

    def _edit(self):
        self.send_event(CancelRegionEdit())
        self.send_event(BeginRegionEdit())
        self.send_event(LoadRegionEvent(self._get_selected_id()))

    def receive_event(self, evt):
        if isinstance(evt, ClearRegionResults):
            self._listbox.delete(0, tkinter.END)
            self._ids = []
            self._edit_btn['state'] = tkinter.DISABLED
        elif isinstance(evt, RegionSearchResultEvent):
            label = f'{evt.region().region_code} | {evt.region().name}'
            self._listbox.insert(tkinter.END, label)
            self._ids.append(evt.region().region_id)

class RegionLoading(tkinter.LabelFrame, EventHandler):
    def __init__(self, parent):
        super().__init__(parent)
        loading = tkinter.Label(self, text='Please wait, loading...')
        loading.grid(row=0, column=0, padx=5, pady=5, sticky=tkinter.W)

class RegionEditor(tkinter.LabelFrame, EventHandler):
    def __init__(self, parent, is_new, can_edit, region):
        if is_new:
            title = 'Create Region'
        elif can_edit:
            title = 'Update Region'
        else:
            title = 'Region Saved!'
        super().__init__(parent, text=title)
        self._is_new = is_new
        self._rid = region.region_id if region else None
        code = region.region_code if region and region.region_code else ''
        local = region.local_code if region and region.local_code else ''
        name = region.name if region and region.name else ''
        continent_id = region.continent_id if region and region.continent_id else 0
        country_id = region.country_id if region and region.country_id else 0
        wiki = region.wikipedia_link if region and region.wikipedia_link else ''
        keywords = region.keywords if region and region.keywords else ''
        self._code_var = tkinter.StringVar(value=code)
        self._local_var = tkinter.StringVar(value=local)
        self._name_var = tkinter.StringVar(value=name)
        self._continent_var = tkinter.StringVar(value=str(continent_id))
        self._country_var = tkinter.StringVar(value=str(country_id))
        self._wiki_var = tkinter.StringVar(value=wiki)
        self._keywords_var = tkinter.StringVar(value=keywords)
        id_lbl = tkinter.Label(self, text='ID:')
        id_lbl.grid(row=0, column=0, padx=5, pady=5, sticky=tkinter.E)
        id_val = tkinter.Label(self, text=f'{self._rid if self._rid else "(New)"}')
        id_val.grid(row=0, column=1, padx=5, pady=5, sticky=tkinter.W)
        code_lbl = tkinter.Label(self, text='Code:')
        code_lbl.grid(row=1, column=0, padx=5, pady=5, sticky=tkinter.E)
        if can_edit:
            code_entry = tkinter.Entry(self, textvariable=self._code_var, width=10)
        else:
            code_entry = tkinter.Label(self, textvariable=self._code_var)
        code_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tkinter.W)
        local_lbl = tkinter.Label(self, text='Local:')
        local_lbl.grid(row=2, column=0, padx=5, pady=5, sticky=tkinter.E)
        if can_edit:
            local_entry = tkinter.Entry(self, textvariable=self._local_var, width=10)
        else:
            local_entry = tkinter.Label(self, textvariable=self._local_var)
        local_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tkinter.W)
        name_lbl = tkinter.Label(self, text='Name:')
        name_lbl.grid(row=3, column=0, padx=5, pady=5, sticky=tkinter.E)
        if can_edit:
            name_entry = tkinter.Entry(self, textvariable=self._name_var, width=30)
        else:
            name_entry = tkinter.Label(self, textvariable=self._name_var)
        name_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tkinter.W)
        continent_lbl = tkinter.Label(self, text='Continent ID:')
        continent_lbl.grid(row=4, column=0, padx=5, pady=5, sticky=tkinter.E)
        if can_edit:
            continent_entry = tkinter.Entry(self, textvariable=self._continent_var, width=10)
        else:
            continent_entry = tkinter.Label(self, textvariable=self._continent_var)
        continent_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tkinter.W)
        country_lbl = tkinter.Label(self, text='Country ID:')
        country_lbl.grid(row=5, column=0, padx=5, pady=5, sticky=tkinter.E)
        if can_edit:
            country_entry = tkinter.Entry(self, textvariable=self._country_var, width=10)
        else:
            country_entry = tkinter.Label(self, textvariable=self._country_var)
        country_entry.grid(row=5, column=1, padx=5, pady=5, sticky=tkinter.W)
        wiki_lbl = tkinter.Label(self, text='Wikipedia:')
        wiki_lbl.grid(row=6, column=0, padx=5, pady=5, sticky=tkinter.E)
        if can_edit:
            wiki_entry = tkinter.Entry(self, textvariable=self._wiki_var, width=50)
        else:
            wiki_entry = tkinter.Label(self, textvariable=self._wiki_var)
        wiki_entry.grid(row=6, column=1, padx=5, pady=5, sticky=tkinter.W)
        keywords_lbl = tkinter.Label(self, text='Keywords:')
        keywords_lbl.grid(row=7, column=0, padx=5, pady=5, sticky=tkinter.E)
        if can_edit:
            keywords_entry = tkinter.Entry(self, textvariable=self._keywords_var, width=50)
        else:
            keywords_entry = tkinter.Label(self, textvariable=self._keywords_var)
        keywords_entry.grid(row=7, column=1, padx=5, pady=5, sticky=tkinter.W)
        btn_frame = tkinter.Frame(self)
        btn_frame.grid(row=9, column=1, padx=5, pady=5, sticky=tkinter.SE)
        if can_edit:
            save_btn = tkinter.Button(btn_frame, text='Save', command=self._save)
            save_btn.grid(row=0, column=0, padx=5, pady=5)
        discard_btn = tkinter.Button(btn_frame, text='Cancel', command=self._discard)
        discard_btn.grid(row=0, column=1, padx=5, pady=5)
        self.rowconfigure(0, weight=0)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=0)
        self.rowconfigure(3, weight=0)
        self.rowconfigure(4, weight=0)
        self.rowconfigure(5, weight=0)
        self.rowconfigure(6, weight=0)
        self.rowconfigure(7, weight=0)
        self.rowconfigure(8, weight=1)
        self.rowconfigure(9, weight=0)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

    def _save(self):
        region = self._make_region()
        if region:
            if self._is_new:
                self.send_event(SaveNewRegionEvent(region))
            else:
                self.send_event(SaveRegionEvent(region))

    def _discard(self):
        self.send_event(CancelRegionEdit())

    def _make_region(self):
        errors = []
        try:
            continent_id = int(self._continent_var.get())
        except ValueError:
            errors.append('Continent ID must be an integer')
        try:
            country_id = int(self._country_var.get())
        except ValueError:
            errors.append('Country ID must be an integer')
        if errors:
            tkinter.messagebox.showerror('Region Save Error', '\n'.join(errors))
            return None
        else:
            return Region(
                self._rid, self._code_var.get(), self._local_var.get(),
                self._name_var.get(), continent_id, country_id,
                self._wiki_var.get(), self._keywords_var.get())
