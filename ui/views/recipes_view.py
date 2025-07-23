# recipes_view.py
import tkinter as tk
from tkinter import ttk
from models.database import *

# self.recipe_view = RecipeView(self.root, Recipe,  [{"label": "Nombre", "field": "name"}], "Recetas")

class RecipeView(tk.Frame):
    def __init__(self, parent): 
        super().__init__(parent, bd=4, relief="groove")
        
        self.selected = None
        self.entries = {}
        # title
        title_bot = tk.Button(self, text="Recetas", relief="ridge")
        
        # frame definition
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        entry_frame = tk.Frame(self, bd=4, relief="groove")
        command_frame = tk.Frame(self, bd=4, relief="groove")
        list_frame = tk.Frame(self, bd=4, relief="groove")
       
        title_bot.grid(row=0, column=0, columnspan=2, sticky="ew")
        entry_frame.grid(row=1, column=0, sticky="nsew")
        command_frame.grid(row=1, column=1, sticky="nsew")
        list_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")

        # formulario de entrada
        label = tk.Label(entry_frame, text="Nombre:")
        entry = tk.Entry(entry_frame)

        label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)

        self.entries["name"] = entry
        
        # command buttons
        save_button = tk.Button(command_frame, text="Guardar", command=self.save_obj)
        delete_button = tk.Button(command_frame, text="Eliminar", command=self.delete_obj)
        close_button = tk.Button(command_frame, text="X", command=self.close)
        
        close_button.pack(anchor="ne")
        save_button.pack()
        delete_button.pack(pady=30)

        # variable tk que almacene lista elementos para ser mostrada en el listbox
        self.items_list = tk.Variable(value=[])    

        # lista de elementos
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(list_frame, listvariable=self.items_list, yscrollcommand=scrollbar.set, activestyle=tk.NONE)
        self.listbox.bind("<<ListboxSelect>>", self.on_select)
        scrollbar.config(command=self.listbox.yview)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(expand=True, fill=tk.BOTH)
        
        self.load_all()

    def load_all(self):
        elements = Recipe.get_all()
        items = [f"{element.id}: {element.name}" for element in elements]
        items.append("+ Nuevo...")
        self.items_list.set(items)
        
    def save_obj(self):
        name = self.entries["name"].get().strip()
        if not name:
            return
        if self.selected:
            setattr(self.selected, "name", self.entries["name"].get().strip())
            self.selected.save()
        else:
            # Crear un nuevo objeto con los datos del formulario
            obj = Recipe(self.entries["name"].get().strip(),[])
            obj.save()
        self.clear_fields()
        self.entries["name"].focus()
        self.load_all()

    def delete_obj(self):
        if self.selected:
            self.selected.delete()
            self.selected = None
            self.clear_fields()
            self.load_all()

    def on_select(self, event):
        try:
            index = self.listbox.curselection()[0]
            data = self.listbox.get(index)
            self.clear_fields()
            if data == "+ Nuevo...":
                self.selected = None
            else:
                id = int(data.split(":")[0])
                self.selected = Recipe.get_by_id(id)
                self.entries["name"].insert(0, getattr(self.selected, "name"))
            self.after(10, lambda: self.entries["name"].focus())
        except IndexError:
            pass

    def clear_fields(self):

        self.entries["name"].delete(0, tk.END)

    def close(self):
        self.destroy()
