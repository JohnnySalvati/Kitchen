# recipes_view.py
import tkinter as tk
from tkinter import ttk
from models.database import *
class RecipeView(tk.Frame):
    def __init__(self, parent): 
        super().__init__(parent, bd=4, relief="groove")
        self.recipe_selected = None
        self.step_selected = None        

        # frame definition
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=1)
        
        top_frame = tk.Frame(self, bd=4, relief="groove")
        recipe_frame = tk.Frame(self, bd=4, relief="groove")
        command_frame = tk.Frame(self, bd=4, relief="groove")
        step_frame = tk.LabelFrame(self, text="Pasos", bd=4, relief="groove")
        entry_frame = tk.Frame(self, bd=4, relief="groove")
       
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        recipe_frame.grid(row=1, column=0, sticky="nsew")
        command_frame.grid(row=1, column=1, sticky="nsew")
        step_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        entry_frame.grid(row=3, column=0, columnspan=2, sticky="nsew")

        # title
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=0)
        title_button = tk.Button(top_frame, text="Recetas", font=("TkCaptionFont", 12), relief="flat")
        close_button = tk.Button(top_frame, text="X", command=self.close)

        title_button.grid(row=0, column=0, sticky="ew")
        close_button.grid(row=0, column=1, sticky="e")

        # frames del formulario de entrada
        recipe_name_frame = tk.LabelFrame(entry_frame, text="Receta", bd=2, relief="ridge")
        self.step_data_frame = tk.LabelFrame(entry_frame,text="Paso", bd=2, relief="ridge")
        self.step_data_frame.grid_columnconfigure(0, weight=1)
        self.step_data_frame.grid_columnconfigure(1, weight=1)
        self.step_data_frame.grid_columnconfigure(2, weight=1)

        source_frame = tk.LabelFrame(self.step_data_frame, text="Original", bd=2, relief="ridge")
        action_frame = tk.Frame(self.step_data_frame, bd=2, relief="ridge")
        result_frame = tk.LabelFrame(self.step_data_frame, text="Resultante", bd=2, relief="ridge")

        recipe_name_frame.pack(anchor="nw", padx=5, pady=20)

        source_frame.grid(row=1, column=0, sticky="nse", padx=20, pady=10)
        action_frame.grid(row=1, column=1, padx=20, pady=10)
        result_frame.grid(row=1, column=2, sticky="nsw", padx=20, pady=10)

        # formulario de entrada

        label = tk.Label(recipe_name_frame, text="Nombre:")
        label.grid(row=0, column=0, sticky="e", padx=(40, 5), pady=5)
        self.entry_name = tk.Entry(recipe_name_frame, width=40)
        self.entry_name.grid(row=0, column=1, sticky="w", padx=(5, 40), pady=5)

        label = tk.Label(source_frame, text="Ingrediente:")
        label.grid(row=0, column=0, sticky="e", padx=(40, 5), pady=5)
        label = tk.Label(source_frame, text="Unidad:")
        label.grid(row=1, column=0, sticky="e", padx=(40, 5), pady=5)
        label = tk.Label(source_frame, text="Cantidad:")
        label.grid(row=2, column=0, sticky="e", padx=(40, 5), pady=5)
        label = tk.Label(action_frame, text="Accion:")
        label.grid(row=0, column=0, sticky="e", padx=(40, 5), pady=5)
        label = tk.Label(result_frame, text="Ingrediente:")
        label.grid(row=0, column=0, sticky="e", padx=(40, 5), pady=5)
        label = tk.Label(result_frame, text="Unidad:")
        label.grid(row=1, column=0, sticky="e", padx=(40, 5), pady=5)
        label = tk.Label(result_frame, text="Cantidad:")
        label.grid(row=2, column=0, sticky="e", padx=(40, 5), pady=5)

        self.source_ingredient_combobox = ttk.Combobox(source_frame, values=RecipeView.load_ingredient_values(), state="readonly")
        self.source_unit_combobox = ttk.Combobox(source_frame, values=RecipeView.load_unit_values(), state="readonly")
        self.source_quantity = tk.Entry(source_frame, width=5)
        self.action_combobox = ttk.Combobox(action_frame, values=RecipeView.load_action_values(), state="readonly")
        self.result_ingredient_combobox = ttk.Combobox(result_frame, values=RecipeView.load_ingredient_values(), state="readonly")
        self.result_unit_combobox = ttk.Combobox(result_frame, values=RecipeView.load_unit_values(), state="readonly")
        self.result_quantity = tk.Entry(result_frame, width=5)

        # agrego llamadas para actualizar valores de los combobox cuando reciben el foco
        self.source_ingredient_combobox.bind("<Button-1>", self.update_ingredient_values)
        self.source_unit_combobox.bind("<Button-1>", self.update_unit_values)
        self.action_combobox.bind("<Button-1>", self.update_action_values)
        self.result_ingredient_combobox.bind("<Button-1>", self.update_ingredient_values)
        self.result_unit_combobox.bind("<Button-1>", self.update_unit_values)

        self.source_ingredient_combobox.grid(row=0, column=1, sticky="w", padx=(5, 40), pady=5)
        self.source_unit_combobox.grid(row=1, column=1, sticky="w", padx=(5, 40), pady=5)
        self.source_quantity.grid(row=2, column=1, sticky="w", padx=(5, 40), pady=5)
        self.action_combobox.grid(row=0, column=1, sticky="w", padx=(5, 40), pady=5)
        self.result_ingredient_combobox.grid(row=0, column=1, sticky="w", padx=(5, 40), pady=5)
        self.result_unit_combobox.grid(row=1, column=1, sticky="w", padx=(5, 40), pady=5)
        self.result_quantity.grid(row=2, column=1, sticky="w", padx=(5, 40), pady=5)

        # command buttons
        save_button = tk.Button(command_frame, text="Guardar", command=self.save_obj)
        delete_button = tk.Button(command_frame, text="Eliminar", command=self.delete_obj)

        save_button.pack(expand=True )
        delete_button.pack(expand=True)

        # variable tk que almacene lista elementos para ser mostrada en el listbox
        self.recipe_list = tk.Variable(value=[])    
        # lista de elementos
        recipe_scrollbar = ttk.Scrollbar(recipe_frame, orient=tk.VERTICAL)
        self.recipe_listbox = tk.Listbox(recipe_frame, listvariable=self.recipe_list, yscrollcommand=recipe_scrollbar.set, activestyle=tk.NONE)
        self.recipe_listbox.bind("<ButtonRelease-1>", self.on_select_recipe)
        recipe_scrollbar.config(command=self.recipe_listbox.yview)

        recipe_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.recipe_listbox.pack(expand=True, fill=tk.BOTH)
        
        # variable tk que almacene lista elementos para ser mostrada en el step
        self.step_list = tk.Variable(value=[])    
        # lista de step
        step_scrollbar = ttk.Scrollbar(step_frame, orient=tk.VERTICAL)
        self.step_listbox = tk.Listbox(step_frame, listvariable=self.step_list, yscrollcommand=step_scrollbar.set, activestyle=tk.NONE)
        self.step_listbox.bind("<ButtonRelease-1>", self.on_select_step)
        step_scrollbar.config(command=self.step_listbox.yview)

        step_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.step_listbox.pack(expand=True, fill=tk.BOTH)
        
        self.load_recipe_list()

    def update_ingredient_values(self, event=None):
        self.source_ingredient_combobox['values'] = RecipeView.load_ingredient_values()
        self.result_ingredient_combobox['values'] = RecipeView.load_ingredient_values()
    
    def update_action_values(self, event=None):
        self.action_combobox['values'] = RecipeView.load_action_values()
        self.action_combobox['values'] = RecipeView.load_action_values()
    
    def update_unit_values(self, event=None):
        self.source_unit_combobox['values'] = RecipeView.load_unit_values()
        self.result_unit_combobox['values'] = RecipeView.load_unit_values()
        
    @staticmethod
    def load_ingredient_values():
        return [f"{i.id}: {i.name}" for i in Ingredient.get_all()]
    
    @staticmethod
    def load_action_values():
        return [f"{a.id}: {a.name}" for a in Action.get_all()]
    
    @staticmethod
    def load_unit_values():
        return [f"{u.id}: {u.name}" for u in Unit.get_all()]

    def load_recipe_list(self):
        recipes = Recipe.get_all()
        items = [f"{recipe.id}: {recipe.name}" for recipe in recipes]
        items.append("+ Nuevo...")
        self.recipe_list.set(items)

    def load_step_list(self):
        items = [f"{step.id}: {step.ingredient.name}: {step.action.name}" for step in self.recipe_selected.steps]
        items.append("+ Nuevo...")
        self.step_list.set(items)
            
    def save_obj(self):
        name = self.entry_name.get().strip()
        if not name:
            return
        if self.recipe_selected:
            self.recipe_selected.name = self.entry_name.get().strip()
            obj = self.recipe_selected
        else:
            # Crear un nuevo objeto con los datos del formulario
            obj = Recipe(self.entry_name.get().strip(),[])
        obj.save()
        if self.step_selected:
            obj.add_step(self.step_selected)
        else:
            step = Step(obj.id,
                        self.get_source_ingredient(),
                        self.get_source_unit(),
                        self.get_source_quantity(),
                        self.get_action(),
                        self.get_result_ingredient(),
                        self.get_result_unit(),
                        self.get_result_quantity(),
                        )
            obj.add_step(step)
        self.entry_name.focus()
        self.load_recipe_list()

    def delete_obj(self):
        if self.recipe_selected:
            self.recipe_selected.delete()
            self.recipe_selected = None
            self.entry_name.delete(0, tk.END)
            self.load_recipe_list()

    def on_select_recipe(self, event):
        try:
            self.step_data_frame.forget() # oculto el frame con los datos del step 
            index = self.recipe_listbox.curselection()[0]
            data = self.recipe_listbox.get(index)
            self.entry_name.delete(0, tk.END)
            if data == "+ Nuevo...":
                self.recipe_selected = None
            else:
                id = int(data.split(":")[0])
                self.recipe_selected = Recipe.get_by_id(id)
                self.entry_name.insert(0, self.recipe_selected.name)
                self.load_step_list()
            self.after(10, lambda: self.entry_name.focus())
        except IndexError:
            pass
    
    def on_select_step(self, event):
        try:
            self.step_data_frame.pack(anchor="center", padx=5, pady=20) # muestro el frame con los datos del step 
            index = self.step_listbox.curselection()[0]
            data = self.step_listbox.get(index)
            self.clear_step_fields() 
            if data == "+ Nuevo...":
                step = None
            else:
                id = int(data.split(":")[0])
                step = Step.get_by_id(id)
                self.source_ingredient_combobox.set(f"{step.ingredient.id}: {step.ingredient.name}")
                self.source_unit_combobox.set(f"{step.unit.id}: {step.unit.name}")
                self.source_quantity.insert(0, step.quantity)
                self.action_combobox.set(f"{step.action.id}: {step.action.name}")
                self.result_ingredient_combobox.set(f"{step.resultIngredient.id}: {step.ingredient.name}")
                self.result_unit_combobox.set(f"{step.resultUnit.id}: {step.resultUnit.name}")
                self.result_quantity.insert(0, step.resultQuantity)
            self.step_selected = step
        except IndexError:
            pass
    
    def clear_step_fields(self):
        self.source_ingredient_combobox.set("")
        self.source_unit_combobox.set("")
        self.source_quantity.delete(0, tk.END)
        self.action_combobox.set("")
        self.result_ingredient_combobox.set("")
        self.result_unit_combobox.set("")
        self.result_quantity.delete(0, tk.END)

    def close(self):
        self.destroy()

    def get_source_ingredient(self):
        id = int(self.source_ingredient_combobox.get().split(":")[0])
        return Ingredient.get_by_id(id)

    def get_result_ingredient(self):
        id = int(self.result_ingredient_combobox.get().split(":")[0])
        return Ingredient.get_by_id(id)

    def get_source_unit(self):
        id = int(self.source_unit_combobox.get().split(":")[0])
        return Unit.get_by_id(id)

    def get_result_unit(self):
        id = int(self.result_unit_combobox.get().split(":")[0])
        return Unit.get_by_id(id)

    def get_source_quantity(self):
        q = float(self.source_quantity.get())
        return q
    
    def get_result_quantity(self):
        q = float(self.result_quantity.get())
        return q
    
    def get_action(self):
        id = int(self.action_combobox.get().split(":")[0])
        return Action.get_by_id(id)

    
    