# main_window.py
import tkinter as tk
from ui.views.elements_view import *

class KitchenApp():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("K I T C H E N")
        self.root.minsize(800, 600)
        self.root.geometry("800x600")
        
    def add_frame(self, bd, relief, padx, pady):
        frame = tk.Frame(
                    self.root,
                    bd=bd,
                    relief=relief,
                    padx=padx,
                    pady=pady
                    )
        frame.pack(side=tk.LEFT, anchor="nw", padx=10, pady=10)
        return frame
        
    def add_button(self, parent, text, command=None):
        btn = tk.Button(
            parent,
            text=text,
            bd=4,
            relief="raised",
            pady=5,
            command=command)
        btn.pack(fill="both", pady=5)
        return btn        
    
    def unit_crud(self):
        self.create_view(Unit, 
                        [
                        {"label": "Nombre", "field": "name"},
                        {"label": "Abreviatura", "field": "short_name"}
                        ]
                    )

    def action_crud(self):
        self.create_view(Action, [{"label": "Nombre", "field": "name"}])

    def ingredient_crud(self):
        self.create_view(Ingredient, [{"label": "Nombre", "field": "name"}])
    
    def recipe_crud(self):
        self.create_view(Recipe, [{"label": "Nombre", "field": "name"}])

    def create_view(self, cls, field_definition):
        if hasattr(self, 'elements_view') and self.elements_view.winfo_exists():
            self.elements_view.destroy()
        self.elements_view = ElementView(self.root, cls, field_definition)
        self.elements_view.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)  
 
        
    
    