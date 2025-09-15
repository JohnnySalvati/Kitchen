import tkinter as tk

class SmartListbox(tk.Listbox):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, selectmode=tk.SINGLE, **kwargs)
        self.has_focus = False
        self.bind('<FocusIn>', lambda e: self._set_focus(True))
        self.bind('<FocusOut>', lambda e: self._set_focus(False))
        
    def _set_focus(self, focused):
        self.has_focus = focused
        self._update_colors()
        
    def _update_colors(self):
        if self.has_focus:
            self.configure(
                selectbackground='#0078d4',  # Azul Windows moderno
                selectforeground='white'
            )
        else:
            self.configure(
                selectbackground='#d0d0d0',  # Gris desaturado
                selectforeground='black'
            )