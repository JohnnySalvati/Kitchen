# main_window.py
import tkinter as tk
from ui.views.elements_view import *
from ui.views.recipes_view import *
class KitchenApp():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(" 🔪 K I T C H E N   A S S I S T A N T")
        self.root.minsize(1024, 900)
        self.root.geometry("1024x900")
        self.root.state("zoomed")
        
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
            font=("TkMenuFont", 10),
            command=command)
        btn.pack(fill="both", pady=5)
        return btn        
    
    def unit_crud(self):
        self.create_view(Unit, 
                        [
                        {"label": "Nombre:", "field": "name"},
                        {"label": "Abreviatura:", "field": "short_name"}
                        ],
                        "Unidades"
                    )

    def action_crud(self):
        self.create_view(Action, [{"label": "Nombre:", "field": "name"}], "Acciones")

    def ingredient_crud(self):
        self.create_view(Ingredient, [{"label": "Nombre:", "field": "name"}], "Ingredientes")

    def recipe_crud(self):
        if hasattr(self, 'recipe_view') and self.recipe_view.winfo_exists():
            self.recipe_view.destroy()
        self.recipe_view = RecipeView(self.root)
        self.recipe_view.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)  

    def create_view(self, cls, field_definition, title):
        if hasattr(self, 'elements_view') and self.elements_view.winfo_exists():
            self.elements_view.destroy() 
        self.elements_view = ElementView(self.root, cls, field_definition, title)
        self.elements_view.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)  
    
        
    