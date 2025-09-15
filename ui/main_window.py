# main_window.py
import tkinter as tk
from ui.views.units_view import *
from ui.views.recipes_view import *
from ui.views.unit_converter_view import *
from ui.views.calculator_view import *
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
        if hasattr(self, 'elements_view') and self.elements_view.winfo_exists():
            self.elements_view.destroy() 
        self.elements_view = UnitView(self.root)
        self.elements_view.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)  

    def unit_converter_crud(self):
        if hasattr(self, 'unit_converter_view') and self.unit_converter_view.winfo_exists():
            self.unit_converter_view.destroy()
        self.unit_converter_view = UnitConverter(self.root)
        self.unit_converter_view.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)  

    def recipe_crud(self):
        if hasattr(self, 'recipe_view') and self.recipe_view.winfo_exists():
            self.recipe_view.destroy()
        self.recipe_view = RecipeView(self.root)
        self.recipe_view.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)  

    def basic_ingredients(self):
        if hasattr(self, 'calculator_view') and self.calculator_view.winfo_exists():
            self.calculator_view.destroy()
        self.calculator_view = CalculatorView(self.root)
        self.calculator_view.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH)  
