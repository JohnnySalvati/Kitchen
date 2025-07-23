import tkinter as tk

root = tk.Tk()

for i, style in enumerate(["flat", "raised", "sunken", "ridge", "groove", "solid"]):
    f = tk.Frame(root, bd=3, relief=style)
    f.pack(padx=5, pady=5, fill="x")
    tk.Label(f, text=style).pack()

root.mainloop()