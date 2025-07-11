# DatabaseSearcher/views/event_handling.py

import tkinter

class EventMixin:
    def send_event(self, evt):
        widget = self
        if not isinstance(widget, tkinter.Widget):
            pass
        while widget.master is not None:
            widget = widget.master
        if widget is not None:
            widget.send_event(evt)

    def receive_event(self, evt):
        self.on_receive(evt)
        if isinstance(self, (tkinter.Tk, tkinter.Widget)):
            for child in self.winfo_children():
                if not child.winfo_exists():
                    continue
                if isinstance(child, EventMixin):
                    child.receive_event(evt)
        self.after_receive(evt)

    def on_receive(self, evt):
        pass

    def after_receive(self, evt):
        pass
