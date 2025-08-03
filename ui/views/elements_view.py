# elements_view.py
import tkinter as tk
from tkinter import ttk
from models.database import *
from ui.views.widgets.seeker import Seeker
class ElementView(tk.Frame):
    """ 
    cls: es la clase para el CRUD
    field_definition: es un diccionario con los campos de la tabla ej: 
        field_definition = [
            {"label": "Nombre: ", "field": "name" },
            ...
            ]
    """
    def __init__(self, parent, cls, field_definition, title): 
        super().__init__(parent, bd=4, relief="groove")
        self.cls = cls
        self.selected = None
        self.entries = {}
       
        # frame definition
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        top_frame = tk.Frame(self, bd=4, relief="groove")
        list_frame = tk.Frame(self, bd=4, relief="groove")
        command_frame = tk.Frame(self, bd=4, relief="groove")
        entry_frame = tk.Frame(self, bd=4, relief="groove")
       
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        list_frame.grid(row=1, column=0, sticky="nsew")
        command_frame.grid(row=1, column=1, sticky="nsew")
        entry_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        
        # title
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=0)
        title_button = tk.Button(top_frame, text=title, font=("TkCaptionFont", 12), relief="flat")
        close_button = tk.Button(top_frame, text="X", command=self.close)

        title_button.grid(row=0, column=0, sticky="ew")
        close_button.grid(row=0, column=1, sticky="e")

        # formulario de entrada
        for i, field in enumerate(field_definition):
            label = tk.Label(entry_frame, text=field["label"])
            entry = tk.Entry(entry_frame)

            label.grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry.grid(row=i, column=1, sticky="w", padx=5, pady=5)

            self.entries[field["field"]] = entry
        
        # command buttons
        save_button = tk.Button(command_frame, text="Guardar", command=self.save_obj)
        delete_button = tk.Button(command_frame, text="Eliminar", command=self.delete_obj)

        search_frame = tk.Frame(command_frame)
        search_label = tk.Label(search_frame, text="Busqueda:", anchor="e")
        search_label_keys = tk.Label(search_frame, width=20, anchor="w")
        search_label.pack(side="left")
        search_label_keys.pack(side="left")

        search_frame.pack(expand=True)
        

        save_button.pack(expand=True)
        delete_button.pack(expand=True)

        # variable tk que almacene lista elementos para ser mostrada en el listbox
        self.items_list = tk.Variable(value=[])    

        # lista de elementos
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.listbox = tk.Listbox(list_frame, listvariable=self.items_list, yscrollcommand=scrollbar.set, activestyle=tk.NONE)
        self.listbox.bind("<ButtonRelease-1>", self.on_select)
        self.listbox.bind("<Return>", self.on_select)
        # buscador para lista de elementos
        self.listbox_search = Seeker(self.listbox, search_label_keys)
        self.listbox.bind("<Key>", self.listbox_search.search)

        scrollbar.config(command=self.listbox.yview)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(expand=True, fill=tk.BOTH)
        
        self.load_all()
        self.listbox.focus_set()

    def load_all(self):
        elements = self.cls.get_all()
        items = [f"{element.id}: {element.name}" for element in elements]
        items.append("+ Nuevo...")
        self.items_list.set(items)
        
    def save_obj(self):
        name = self.entries["name"].get().strip()
        if not name:
            return
        if self.selected:
            for field, entry in self.entries.items():
                setattr(self.selected, field, entry.get().strip())
            self.selected.save()
        else:
            # Crear un nuevo objeto con los datos del formulario
            kwargs = {field: entry.get().strip() for field, entry in self.entries.items()}
            obj = self.cls(**kwargs)
            obj.save()
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
                self.selected = self.cls.get_by_id(id)
                for field, entry in self.entries.items():
                    entry.insert(0, getattr(self.selected, field)) 
            self.after(10, lambda: self.entries["name"].focus())
        except IndexError:
            pass

    def clear_fields(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)

    def close(self):
        self.destroy()
