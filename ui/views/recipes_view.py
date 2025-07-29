# recipes_vie
from playsound import playsound
import re
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from models.database import *
from ui.views.widgets.seeker import Seeker
from ui.views.widgets.entry_validators import *
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
        
        # agrego validaciones a los quantity entries
        vcmd = (self.register(only_float), "%P")
        
        self.source_ingredient_combobox = ttk.Combobox(source_frame, values=RecipeView.load_ingredient_values(), state="readonly")
        self.source_unit_combobox = ttk.Combobox(source_frame, values=RecipeView.load_unit_values(), state="readonly")
        self.source_quantity = tk.Entry(source_frame, validate="key", validatecommand=vcmd, width=5)
        self.action_combobox = ttk.Combobox(action_frame, values=RecipeView.load_action_values(), state="readonly")
        self.result_ingredient_combobox = ttk.Combobox(result_frame, values=RecipeView.load_ingredient_values(), state="readonly")
        self.result_unit_combobox = ttk.Combobox(result_frame, values=RecipeView.load_unit_values(), state="readonly")
        self.result_quantity = tk.Entry(result_frame, validate="key", validatecommand=vcmd, width=5)
        
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
        self.save_recipe_button = tk.Button(command_frame, text="Guardar Receta", command=self.save_recipe)
        self.delete_recipe_button = tk.Button(command_frame, text="Eliminar Receta", command=self.delete_recipe)
        self.save_step_button = tk.Button(command_frame, text="Guardar Paso", command=self.save_step)
        self.delete_step_button = tk.Button(command_frame, text="Eliminar Paso", command=self.delete_step)
        search_frame = tk.Frame(command_frame)
        search_label = tk.Label(search_frame, text="Busqueda:", anchor="e")
        search_label_keys = tk.Label(search_frame, width=20, anchor="w")
        search_label.pack(side="left")
        search_label_keys.pack(side="left")

        search_frame.pack(expand=True)
        self.save_recipe_button.pack(expand=True )
        self.delete_recipe_button.pack(expand=True)
        self.save_step_button.pack(expand=True )
        self.delete_step_button.pack(expand=True)
        
        # oculto los command buttons para step
        self.save_step_button.forget()
        self.delete_step_button.forget()

        # variable tk que almacene lista elementos para ser mostrada en el listbox
        self.recipe_list = tk.Variable(value=[])
        

        # lista de elementos
        recipe_scrollbar = ttk.Scrollbar(recipe_frame, orient=tk.VERTICAL)
        self.recipe_listbox = tk.Listbox(recipe_frame, listvariable=self.recipe_list, yscrollcommand=recipe_scrollbar.set, activestyle=tk.NONE)
        self.recipe_listbox.bind("<ButtonRelease-1>", self.on_select_recipe)
        self.recipe_listbox.bind("<Return>", self.on_select_recipe)
        recipe_scrollbar.config(command=self.recipe_listbox.yview)

        recipe_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.recipe_listbox.pack(expand=True, fill=tk.BOTH)

        # buscador para lista de recetas
        self.recipe_search = Seeker(self.recipe_listbox, search_label_keys)
        self.recipe_listbox.bind("<Key>", self.recipe_search.search)
        
        # variable tk que almacene lista elementos para ser mostrada en el step
        self.step_list = tk.Variable(value=[])    
        # lista de step
        step_scrollbar = ttk.Scrollbar(step_frame, orient=tk.VERTICAL)
        self.step_listbox = tk.Listbox(step_frame, listvariable=self.step_list, yscrollcommand=step_scrollbar.set, activestyle=tk.NONE)
        self.step_listbox.bind("<ButtonRelease-1>", self.on_select_step)
        self.step_listbox.bind("<Return>", self.on_select_step)
        step_scrollbar.config(command=self.step_listbox.yview)

        step_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.step_listbox.pack(expand=True, fill=tk.BOTH)

        # buscador para lista de pasos
        self.step_search = Seeker(self.step_listbox, search_label_keys)        
        self.step_listbox.bind("<Key>", self.step_search.search)

        self.load_recipe_list()
        self.recipe_listbox.focus_set()

    def update_ingredient_values(self, event=None):
        self.source_ingredient_combobox['values'] = RecipeView.load_ingredient_values()
        self.result_ingredient_combobox['values'] = RecipeView.load_ingredient_values()
    
    def update_action_values(self, event=None):
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

    def save_recipe(self):
        self.recipe_selected.name = self.entry_name.get().strip()
        if not self.recipe_selected.name:
            return
        self.recipe_selected.save()
        self.load_recipe_list()
        
    def save_step(self):
        step = Step(self.recipe_selected.id,
                        self.get_source_ingredient(),
                        self.get_source_unit(),
                        self.get_source_quantity(),
                        self.get_action(),
                        self.get_result_ingredient(),
                        self.get_result_unit(),
                        self.get_result_quantity(),
                        self.step_selected.id)
        step.save()
        # self.recipe_selected.add_step(step)
        self.load_step_list()
        
    def delete_recipe(self):
        if messagebox.askokcancel("Eliminar receta", "¿ Estas seguro que deseas eliminar la receta y sus pasos ?"):
            if self.recipe_selected.id:
                self.recipe_selected.delete()
                self.recipe_selected = None
                self.entry_name.delete(0, tk.END)
                self.load_recipe_list()

    def delete_step(self):
        selection = self.step_listbox.curselection()
        if not selection:
            return
        if messagebox.askokcancel("Eliminar paso", "¿ Estas seguro que deseas eliminar el paso ?"):
            index = selection[0]
            data = self.step_listbox.get(index)
            if data != "+ Nuevo...":
                id = int(data.split(":")[0])
                step = Step.get_by_id(id)
                self.recipe_selected.delete_step(step)
                self.clear_step_fields()
                self.load_step_list()
    
    def on_select_recipe(self, event):
        self.show_recipe_environment() # modifico el entorno para recipe
        index = self.recipe_listbox.curselection()[0]
        data = self.recipe_listbox.get(index)
        self.entry_name.delete(0, tk.END)
        self.step_search.clear()
        if data == "+ Nuevo...":
            self.recipe_selected = Recipe("")
        else:
            id = int(data.split(":")[0])
            self.recipe_selected = Recipe.get_by_id(id)
        self.entry_name.insert(0, self.recipe_selected.name)
        self.load_step_list()
        #self.after(10, lambda: self.entry_name.focus())
        
    def on_select_step(self, event):
        if self.recipe_selected.id == None: # si la receta no esta guardada no pueden cargarse pasos
            messagebox.showinfo("Antes de agregar pasos debes GUARDAR la receta")
            return
        self.show_step_environment() # modifico el entorno para step
        index = self.step_listbox.curselection()[0]
        data = self.step_listbox.get(index)
        self.clear_step_fields() 
        self.recipe_search.clear()
        if data == "+ Nuevo...":
            step = Step()
        else:
            id = int(data.split(":")[0])
            step = Step.get_by_id(id)
        self.source_ingredient_combobox.set(f"{step.ingredient.id}: {step.ingredient.name}")
        self.source_unit_combobox.set(f"{step.unit.id}: {step.unit.name}")
        self.source_quantity.insert(0, step.quantity)
        self.action_combobox.set(f"{step.action.id}: {step.action.name}")
        self.result_ingredient_combobox.set(f"{step.resultIngredient.id}: {step.resultIngredient.name}")
        self.result_unit_combobox.set(f"{step.resultUnit.id}: {step.resultUnit.name}")
        self.result_quantity.insert(0, step.resultQuantity)
        self.step_selected = step
    
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

    def show_step_environment(self):
        self.step_data_frame.pack(anchor="center", padx=5, pady=20) # muestro el frame con los datos del step 
        # muestro command buttons para step
        self.save_step_button.pack(expand=True )
        self.delete_step_button.pack(expand=True)
        # oculto los command buttons para recipe
        self.save_recipe_button.forget()
        self.delete_recipe_button.forget()
        self.entry_name.config(state="disabled")
    
    def show_recipe_environment(self):
        self.step_data_frame.forget()        # oculto el frame con los datos del step
        # muestro command buttons para recipe
        self.save_recipe_button.pack(expand=True )
        self.delete_recipe_button.pack(expand=True)
        # oculto los command buttons para step
        self.save_step_button.forget()
        self.delete_step_button.forget()
        self.entry_name.config(state="normal")

