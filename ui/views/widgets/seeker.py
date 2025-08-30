# this class build a seeker object for event management listboxes
try:
    import winsound
    def play_sound(filename):
        winsound.PlaySound(filename, winsound.SND_FILENAME)
except ImportError:
    from playsound import playsound
    def play_sound(filename):
        playsound(filename, block=False)

import re
import tkinter as tk
from tkinter import ttk 

class Seeker():
    def __init__(self, box, label ):
        self.buffer = ""
        self.box = box
        self.label = label
        if isinstance(box, tk.Listbox):
            self.show = self.show_listbox
            self.get = lambda : self.box.get(0, tk.END)
        if isinstance(box, ttk.Combobox):
            self.show = self.show_combobox
            self.get = lambda : self.box["values"]

    def search(self, event):
        if event.keysym in ("Up", "Down", "Left", "Right", "Prior", "Next", "Home", "End"):
            self.box.after(1500, self.clear_buffer)
            return
        sound = None
        if event.char.isprintable():
            self.buffer += event.char
            elements_list = self.get()
            # build the pattern by inserting .* between characters
            pattern = '.*'.join(map(re.escape, self.buffer))  # e.g. "rcpv" → r.*c.*p.*v
            regex = re.compile(pattern, re.IGNORECASE)   # case insensitive
            for index, item in enumerate(elements_list):
                if re.search(regex, item):
                    self.show(index)
                    self.box.after(2000, self.clear_buffer)
                    return "break"
            self.buffer = self.buffer[:-1]
            sound = 'tap.wav'
        elif event.keysym == "BackSpace":
            self.buffer = self.buffer[:-1]
        elif event.keysym == "Escape":
            sound = 'pop.wav'
            self.buffer = ""
        self.label.config(text=self.buffer)
        if sound:
            play_sound(sound)
        self.box.after(1500, self.clear_buffer)

    def clear_buffer(self):
        if self.buffer != "":
            self.buffer = ""
            self.show()
            play_sound('pop.wav')
        
    def show_listbox(self, index=None):
        if index is not None:
            self.box.selection_clear(0, tk.END)
            self.box.selection_set(index)
            self.box.activate(index)
            self.box.see(index)
        self.label.config(text=self.buffer)

    def show_combobox(self, index=None):
        if index is not None:
            self.box.current(index)
        self.label.config(text=self.buffer)
