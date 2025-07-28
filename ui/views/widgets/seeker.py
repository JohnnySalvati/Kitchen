# esta clase construye un buscador para ser utilizado en eventos de objetos listbox
import re
import tkinter as tk

class Seeker():
    def __init__(self, listbox, label ):
        self.buffer = ""
        self.listbox = listbox
        self.label = label

    def search(self, event):
        if event.keysym in ("Up", "Down", "Left", "Right", "Prior", "Next", "Home", "End"):
            return
        if event.char.isprintable():
            self.buffer += event.char
            lista = self.listbox.get(0, tk.END)
            # Construyo el patrón intercalando .* entre caracteres
            pattern = '.*'.join(map(re.escape, self.buffer))  # ej: "rcpv" → r.*c.*p.*v
            regex = re.compile(pattern, re.IGNORECASE)   # insensible a mayúsculas
            for index, item in enumerate(lista):
                if re.search(regex, item):
                    self.show(index)
                    return "break"
            self.buffer = self.buffer[:-1]
            #playsound("tap.wav")
        elif event.keysym == "BackSpace":
            self.buffer = self.buffer[:-1]
        elif event.keysym == "Escape":
            self.buffer = ""
        self.label.config(text=self.buffer)

    def clear(self):
        self.buffer = ""
        self.show()
        
    def show(self, index=None):
        if index is not None:
            self.listbox.selection_clear(0, tk.END)
            self.listbox.selection_set(index)
            self.listbox.activate(index)
            self.listbox.see(index)
        self.label.config(text=self.buffer)
