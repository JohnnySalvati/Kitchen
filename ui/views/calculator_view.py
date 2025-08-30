import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ui.views.widgets.seeker import Seeker
from ui.views.widgets.smart_listbox import SmartListbox
from services.recipe_service import RecipeService
from services.unit_service import UnitService

class CalculatorView(tk.Frame):
    def __init__(self, parent): 
        super().__init__(parent, bd=4, relief="groove")
        self.recipe_service = RecipeService()
        self.unit_service = UnitService()

        # frame definition
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        top_frame = tk.Frame(self, bd=4, relief="groove")
        list_frame = tk.Frame(self, bd=4, relief="groove")
        
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        list_frame.grid(row=1, column=0, sticky="nsew")
        
        # title
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=0)
        title_button = tk.Button(top_frame, text="Calculadora de ingredientes básicos", font=("TkCaptionFont", 12), relief="flat")
        close_button = tk.Button(top_frame, text="X", command=self.close)
        title_button.grid(row=0, column=0, sticky="ew")
        close_button.grid(row=0, column=1, sticky="e")

        self.completed_ingredients_list_var = tk.Variable(value=self.load_completed_ingredients())    

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.ingredients_listbox = SmartListbox(
                                        list_frame,
                                        exportselection=False,
                                        listvariable=self.completed_ingredients_list_var,
                                        yscrollcommand=scrollbar.set,
                                        activestyle=tk.NONE)
        self.ingredients_listbox.bind("<ButtonRelease-1>", self.on_select_unit)
        self.ingredients_listbox.bind("<Return>", self.on_select_unit)
 
        # buscador para lista de elementos
        #self.listbox_search = Seeker(self.ingredients_listbox, self.search_label_keys)
        #self.ingredients_listbox.bind("<Key>", self.listbox_search.search)

        scrollbar.config(command=self.ingredients_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.ingredients_listbox.pack(expand=True, fill=tk.BOTH)

        self.basic_ingredients_list_var = tk.Variable(value=[])    

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.basic_ingredients_listbox = SmartListbox(
                                        list_frame,
                                        exportselection=False,
                                        listvariable=self.basic_ingredients_list_var,
                                        yscrollcommand=scrollbar.set,
                                        activestyle=tk.NONE)
        self.basic_ingredients_listbox.bind("<ButtonRelease-1>", self.on_select_unit)
        self.basic_ingredients_listbox.bind("<Return>", self.on_select_unit)
 
        # buscador para lista de elementos
        #self.listbox_search = Seeker(self.basic_ingredients_listbox, self.search_label_keys)
        #self.basic_ingredients_listbox.bind("<Key>", self.listbox_search.search)

        scrollbar.config(command=self.basic_ingredients_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.basic_ingredients_listbox.pack(expand=True, fill=tk.BOTH)


    def load_completed_ingredients(self, event=None):
        try:
            completed_ingredients = self.recipe_service.get_all_completed()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        return [f"{ing.id}: {ing.name}" for ing in completed_ingredients]
        
    def on_select_unit(self, event):
        try:
            index = self.ingredients_listbox.curselection()[0]
            data = self.ingredients_listbox.get(index)
            id = int(data.split(":")[0])
            try:
                basic = self.recipe_service.basic_ingredients(self.recipe_service.get_by_id(id))
                show_list = []
                for ingredient_id, unit_quantity in basic.items():
                    for unit_id, quantity in unit_quantity.items():
                        ingredient_name = self.recipe_service.get_ingredient(ingredient_id).name
                        unit_name = self.unit_service.get_by_id(unit_id).name
                        show_list.append(f"{quantity} {unit_name} de {ingredient_name}")
                self.basic_ingredients_list_var.set(show_list)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        except IndexError:
            pass
        
    def close(self):
        self.destroy()
