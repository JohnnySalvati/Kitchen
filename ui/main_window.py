# main_window.py
import tkinter as tk
from ui.views.elements_view import *
from ui.views.recipes_view import *
from services.action_service import ActionService
from services.unit_service import UnitService
from dto.unit_dto import UnitDTO
from dto.action_dto import ActionDTO

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
        
    def add_button(self, parent, text, command):
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
        self.unit_service = UnitService()
        self.create_view(self.unit_service, 
                        UnitDTO,
                        [
                        {"label": "Nombre:", "field": "name"},
                        {"label": "Abreviatura:", "field": "short_name"}
                        ],
                        "Unidades"
                    )

    def action_crud(self):
        self.action_service = ActionService()
        self.create_view(self.action_service,
                         ActionDTO,
                        [{"label": "Nombre:", "field": "name"}],
                        "Acciones")

    def create_view(self, service, dto, field_definition, title):
        if hasattr(self, 'elements_view') and self.elements_view.winfo_exists():
            self.elements_view.destroy() 
        self.elements_view = ElementView(self.root, service, dto, field_definition, title)
        self.elements_view.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)  

    def recipe_crud(self):
        if hasattr(self, 'recipe_view') and self.recipe_view.winfo_exists():
            self.recipe_view.destroy()
        self.recipe_view = RecipeView(self.root)
        self.recipe_view.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)  

    
        
    