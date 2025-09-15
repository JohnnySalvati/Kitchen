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

        # title
        top_frame = tk.Frame(self, bd=4, relief="groove")
        top_frame.pack(fill=tk.X, anchor=tk.N)
        
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=0)

        title_button = tk.Button(top_frame, text="Calculadora de ingredientes básicos", font=("TkCaptionFont", 12), relief="flat")
        title_button.grid(row=0, column=0, sticky="ew")

        close_button = tk.Button(top_frame, text="X", command=self.close)
        close_button.grid(row=0, column=1, sticky="e")

        list_frame = tk.Frame(self, bd=4, relief="groove")
        list_frame.pack(expand=True, fill=tk.BOTH, anchor=tk.N)
        
        self.completed_ingredients_list_var = tk.Variable()
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.ingredients_listbox = SmartListbox(
                                        list_frame,
                                        font=("Courier New", 10),
                                        exportselection=False,
                                        listvariable=self.completed_ingredients_list_var,
                                        yscrollcommand=scrollbar.set,
                                        activestyle=tk.NONE)
        self.ingredients_listbox.bind("<ButtonRelease-1>", self.on_select_unit)
        self.ingredients_listbox.bind("<Return>", self.on_select_unit)
 
        
        scrollbar.config(command=self.ingredients_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.ingredients_listbox.pack(expand=True, fill=tk.BOTH)

        basic_frame = tk.Frame(self, bd=4, relief="groove")
        basic_frame.pack(expand=True, fill=tk.BOTH, anchor=tk.N)

        self.basic_ingredients_list_var = tk.Variable(value=[])    
        scrollbar = ttk.Scrollbar(basic_frame, orient=tk.VERTICAL)
        self.basic_ingredients_listbox = SmartListbox(
                                        basic_frame,
                                        font=("Courier New", 15),
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
        
        total_frame = tk.Frame(self, bd=4, relief="groove")
        total_frame.pack(fill=tk.X, anchor=tk.S)

        # search frame
        search_frame = tk.Frame(total_frame, bd=2, relief="groove")
        search_frame.pack(expand=True, fill="both", side="left")

        search_label = tk.Label(search_frame, text="Busqueda:", anchor="e")
        search_label_keys = tk.Label(search_frame, width=20, anchor="w")
        search_label.pack(side="left")
        search_label_keys.pack(side="left")

        self.listbox_search = Seeker(self.ingredients_listbox, search_label_keys)
        self.ingredients_listbox.bind("<Key>", self.listbox_search.search)

        self.total_var = tk.StringVar(value="0.00")
        total_label = tk.Label( total_frame,
                                textvariable=self.total_var,
                                font= ("Courier New", 20),
                                width=20,
                                anchor=tk.E)
        total_label.pack(side="left")
        self.load_completed_ingredients()

    def load_completed_ingredients(self, event=None):
        try:
            completed_ingredients = self.recipe_service.get_all_completed()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        sorted_completed_ingredients = sorted(completed_ingredients, key=lambda ing: ing.name)
        self.completed_ingredients_list_var.set([f"{ing.result_quantity:>12,.2f} {ing.result_unit.name}".ljust(35) + f"de {ing.name}"
                                                 for ing in sorted_completed_ingredients])
        self.completed_ingredients_ids = [ing.id for ing in sorted_completed_ingredients]
        
    def on_select_unit(self, event):
        try:
            index = self.ingredients_listbox.curselection()[0]
            id = self.completed_ingredients_ids[index]
            try:
                basic_ingredients = self.recipe_service.basic_ingredients(self.recipe_service.get_by_id(id))
                self.basic_ingredients_list_var.set(self.calculation_list(basic_ingredients))
            except Exception as e:
                messagebox.showerror("Error", str(e))
        except IndexError:
            pass

    def calculation_list(self, basic):
        show_list = []
        total = 0
        for ingredient_id, unit_quantity in basic.items():
            for unit_id, quantity in unit_quantity.items():
                ingredient = self.recipe_service.get_ingredient(ingredient_id)
                unit_name = self.unit_service.get_by_id(unit_id).name
                price = self.recipe_service.get_price(ingredient.id, unit_id, quantity)
                total += price
                show_list.append(f"{quantity:>12,.2f} {unit_name}".ljust(25) + f"de {ingredient.name}".ljust(30) + f"= {price:>10,.2f}")
        self.total_var.set(f"{total:,.2f}")
        return show_list
    
    def close(self):
        self.destroy()
