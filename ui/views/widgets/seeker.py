# this class build a seeker object for event management listboxes
import winsound
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
            # build the pattern by inserting .* between characters
            pattern = '.*'.join(map(re.escape, self.buffer))  # e.g. "rcpv" → r.*c.*p.*v
            regex = re.compile(pattern, re.IGNORECASE)   # case insensitive
            for index, item in enumerate(lista):
                if re.search(regex, item):
                    self.show(index)
                    return "break"
            self.buffer = self.buffer[:-1]
            winsound.PlaySound('tap.wav', winsound.SND_FILENAME)
        elif event.keysym == "BackSpace":
            self.buffer = self.buffer[:-1]
        elif event.keysym == "Escape":
            winsound.PlaySound('pop.wav', winsound.SND_FILENAME)
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
