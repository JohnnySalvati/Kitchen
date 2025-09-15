import tkinter as tk

def only_int(value):
    return value.isdigt() or value == ""

def only_float(value):
    if value == "":
        return True
    try:
        float(value.replace(",", ""))
        return True
    except ValueError:
        return False
    
def format_2dec(event):
    entry = event.widget
    try:
        value = float(entry.get().replace(",", ""))
        entry.delete(0, tk.END)
        entry.insert(0, f"{value:,.2f}")
    except ValueError:
        pass 