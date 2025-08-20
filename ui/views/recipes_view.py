# recipes_vie
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from services.action_service import ActionService
from services.unit_service import UnitService
from services.recipe_service import RecipeService
from services.source_service import SourceService
from services.step_service import StepService
from ui.views.widgets.seeker import Seeker
from ui.views.widgets.smart_listbox import SmartListbox
from ui.views.widgets.entry_validators import *
from dto.recipe_dto import RecipeDTO
from dto.source_dto import SourceDTO
from dto.step_dto import StepDTO
class RecipeView(tk.Frame):
    def __init__(self, parent): 
        super().__init__(parent, bd=4, relief="groove")
        # Services instances
        self.action_service = ActionService()
        self.unit_service = UnitService()
        self.recipe_service = RecipeService()
        self.source_service = SourceService()
        self.step_service = StepService()
        self.selected_recipe = RecipeDTO()
        self.selected_step = StepDTO()
        self.search_label_keys = tk.Label()
        
        # frame definition
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=4)
        
        top_frame = tk.Frame(self, bd=4, relief="groove")
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=0)
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        # title
        title_button = tk.Button(top_frame, text="Recetas", font=("TkCaptionFont", 12), relief="flat")
        close_button = tk.Button(top_frame, text="X", command=self.close)
        title_button.grid(row=0, column=0, sticky="ew")
        close_button.grid(row=0, column=1, sticky="e")

        # frame para las recetas
        recipe_frame = tk.Frame(self, bd=4, relief="groove")
        recipe_frame.grid(row=1, column=0, sticky="nsew")
        self.recipe_list = tk.Variable(value=[]) # variable tk que almacene lista recetas para ser mostrada en el listbox
        recipe_scrollbar = ttk.Scrollbar(recipe_frame, orient=tk.VERTICAL)
        self.recipe_listbox = SmartListbox(recipe_frame,
                                            exportselection=False,
                                            listvariable=self.recipe_list,
                                            yscrollcommand=recipe_scrollbar.set,
                                            activestyle=tk.NONE)
        recipe_scrollbar.config(command=self.recipe_listbox.yview)
        recipe_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.recipe_listbox.bind("<ButtonRelease-1>", self.on_select_recipe)
        self.recipe_listbox.bind("<Return>", self.on_select_recipe)
        self.recipe_listbox.pack(expand=True, fill=tk.BOTH)
        
        # frame para los comandos
        command_frame = tk.Frame(self, bd=4, relief="groove")
        command_frame.grid(row=1, column=1, sticky="nsew")
            # frame para la busqueda
        search_frame = tk.Frame(command_frame, bd=1, relief="groove")
        search_frame.pack(expand=True)
    
        self.save_recipe_button = tk.Button(command_frame, text="Guardar Receta", command=self.save_recipe)
        self.save_recipe_button.pack(expand=True )
        self.delete_recipe_button = tk.Button(command_frame, text="Eliminar Receta", command=self.delete_recipe)
        self.delete_recipe_button.pack(expand=True)
        self.save_step_button = tk.Button(command_frame, text="Guardar Paso", command=self.save_step)
        self.save_step_button.pack(expand=True )
        self.delete_step_button = tk.Button(command_frame, text="Eliminar Paso", command=self.delete_step)
        self.delete_step_button.pack(expand=True)
            # frame para la busqueda
        search_label = tk.Label(search_frame, text="Busqueda:", anchor="e", padx=5)
        self.search_label_keys = tk.Label(search_frame, width=20, anchor="w")
        search_label.pack(side="left")
        self.search_label_keys.pack(side="left")
        self.recipe_search = Seeker(self.recipe_listbox, self.search_label_keys) # buscador para lista de recetas
        self.recipe_listbox.bind("<Key>", self.recipe_search.search)
        # oculto los command buttons para step
        self.save_step_button.forget()
        self.delete_step_button.forget()

        # frame para los pasos
        step_frame = tk.LabelFrame(self, text="Pasos", bd=4, relief="groove")
        step_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.step_list_var = tk.Variable(value=[])    # variable tk que almacene lista steps para ser mostrada en el step
        step_scrollbar = ttk.Scrollbar(step_frame, orient=tk.VERTICAL)
        self.step_listbox = SmartListbox(step_frame,
                                        exportselection=False,
                                        listvariable=self.step_list_var,
                                        yscrollcommand=step_scrollbar.set,
                                        activestyle=tk.NONE)
        step_scrollbar.config(command=self.step_listbox.yview)
        step_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.step_listbox.bind("<ButtonRelease-1>", self.on_select_step)
        self.step_listbox.bind("<Return>", self.on_select_step)
        self.step_search = Seeker(self.step_listbox, self.search_label_keys)        # buscador para lista de pasos
        self.step_listbox.bind("<Key>", self.step_search.search)
        self.step_listbox.pack(expand=True, fill=tk.BOTH)

        # frame del formulario de entrada
        entry_frame = tk.Frame(self, bd=4, relief="groove")
        entry_frame.grid(row=3, column=0, columnspan=2, sticky="nsew")

        vcmd = (self.register(only_float), "%P") # defino comando para validaciones

            # frame para el nombre de la receta
        recipe_name_frame = tk.LabelFrame(entry_frame, text="Receta", bd=2, relief="ridge")
        recipe_name_frame.pack(anchor="nw", padx=5, pady=20)
        label = tk.Label(recipe_name_frame, text="Nombre:")
        label.grid(row=0, column=0, sticky="e", padx=(40, 5), pady=5)
        label = tk.Label(recipe_name_frame, text="Precio:")
        label.grid(row=0, column=2, sticky="e", padx=(40, 5), pady=5)
        self.name_var = tk.StringVar()
        self.entry_name = ttk.Entry(recipe_name_frame, textvariable=self.name_var, width=40)
        self.entry_name.grid(row=0, column=1, sticky="w", padx=(5, 40), pady=5)
        self.price_var = tk.DoubleVar()
        self.entry_price = ttk.Entry(recipe_name_frame, textvariable=self.price_var, validate="key", validatecommand=vcmd, width=12)
        self.entry_price.grid(row=0, column=3, sticky="w", padx=(5, 40), pady=5 )
        self.is_complete = tk.Label(recipe_name_frame, text=" COMPLETA ", bg="#7da883", fg="#06631A")
        
            # frame para datos de los pasos
        self.step_data_frame = tk.LabelFrame(entry_frame,text="Paso", bd=2, relief="ridge")
        self.step_data_frame.grid_columnconfigure(0, weight=2)
        self.step_data_frame.grid_columnconfigure(1, weight=1)
        self.step_data_frame.grid_columnconfigure(2, weight=1)
        self.step_data_frame.grid_rowconfigure(0, weight=1) # para lograr centrado vertical
        self.step_data_frame.grid_rowconfigure(2, weight=1) # para lograr centrado vertical
                # frame para los sources
        self.source_frame = tk.LabelFrame(self.step_data_frame, text="Original", bd=2, relief="ridge")
        self.source_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.source_frame.columnconfigure(0, weight=0)
        self.source_frame.columnconfigure(1, weight=2)
        self.source_frame.columnconfigure(2, weight=2)
        self.source_frame.columnconfigure(3, weight=2)
        self.source_frame.columnconfigure(4, weight=0)
                # actions frame
        action_frame = tk.Frame(self.step_data_frame, bd=2, relief="ridge")
        action_frame.grid(row=1, column=1, padx=20, pady=10)

        label = tk.Label(action_frame, text="Accion:")
        label.grid(row=0, column=0, sticky="e",  padx=(40, 5), pady=5)

        self.action_combobox = ttk.Combobox(action_frame, values=self.load_action_values(), state="readonly")
        self.action_combobox.bind("<Button-1>", self.update_action_values) # agrego llamadas para actualizar valores de los combobox cuando reciben el foco
        self.action_search = Seeker(self.action_combobox, self.search_label_keys)
        self.action_combobox.bind("<Key>", self.action_search.search)
        self.action_combobox.grid(row=0, column=1, sticky="w", padx=(5, 40), pady=5)
                # results frame
        result_frame = tk.LabelFrame(self.step_data_frame, text="Resultante", bd=2, relief="ridge")
        result_frame.grid(row=1, column=2, padx=20, pady=10)
        label = tk.Label(result_frame, text="Ingrediente:")
        label.grid(row=0, column=0, sticky="e", padx=(40, 5), pady=5)
        label = tk.Label(result_frame, text="Unidad:")
        label.grid(row=1, column=0, sticky="e", padx=(40, 5), pady=5)
        label = tk.Label(result_frame, text="Cantidad:")
        label.grid(row=2, column=0, sticky="e", padx=(40, 5), pady=5)

        self.result_ingredient_combobox = ttk.Combobox(result_frame, values=self.load_result_ingredient_values(), state="readonly")
        self.result_ingredient_combobox.bind("<Button-1>", self.update_result_ingredient_values) # agrego llamada para actualizar valores cuando recibe el foco
        self.result_ingredient_search = Seeker(self.result_ingredient_combobox, self.search_label_keys)
        self.result_ingredient_combobox.bind("<Key>", self.result_ingredient_search.search)
        self.result_ingredient_combobox.grid(row=0, column=1, sticky="w", padx=(5, 40), pady=5)

        self.result_unit_combobox = ttk.Combobox(result_frame, values=self.load_unit_values(), state="readonly")
        self.result_unit_combobox.bind("<Button-1>", self.update_result_unit_values) # agrego llamada para actualizar valores cuando recibe el foco
        self.result_unit_search = Seeker(self.result_unit_combobox, self.search_label_keys)
        self.result_unit_combobox.bind("<Key>", self.result_unit_search.search)
        self.result_unit_combobox.grid(row=1, column=1, sticky="w", padx=(5, 40), pady=5)

        self.result_quantity_var = tk.DoubleVar()
        self.result_quantity = ttk.Entry(result_frame, textvariable=self.result_quantity_var, validate="key", validatecommand=vcmd, width=5)        # agrego validaciones a los quantity entries
        self.result_quantity.grid(row=2, column=1, sticky="w", padx=(5, 40), pady=5)

        self.load_recipe_list()
        self.recipe_listbox.focus_set()

    def update_ingredient_values(self, event, row):
        self.comboboxes[row]["ingredient"]["values"] = self.load_ingredient_values()

    def update_result_ingredient_values(self, event=None):
        self.result_ingredient_combobox['values'] = self.load_result_ingredient_values()
    
    def update_action_values(self, event=None):
        self.action_combobox['values'] = self.load_action_values()
    
    def update_unit_values(self, event, row):
        self.comboboxes[row]["unit"]['values'] = self.load_unit_values()
    
    def update_result_unit_values(self, event=None):
        self.result_unit_combobox['values'] = self.load_unit_values()
        
    def load_ingredient_values(self):
        # descarto la posibilidad de tomar como ingrediente el que se esta definiendo
        try:
            return [f"{i.id}: {i.name}" for i in self.recipe_service.get_ingredient_all() if not (self.selected_recipe and i.name == self.selected_recipe.name)] 
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return []

    def load_result_ingredient_values(self):
        if self.selected_step:
             # es el ultimo step incluimos el ingrediente original para poder completar la receta
            if not self.selected_recipe.steps or self.selected_step.id == self.selected_recipe.steps[-1].id or not self.selected_step.id:
                try:
                    return [f"{i.id}: {i.name}" for i in self.recipe_service.get_ingredient_all()] 
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                    return []
        return self.load_ingredient_values() # si no es la ultima no esta permitido el ingrediente original
    
    def load_action_values(self):
        try:
            return [f"{a.id}: {a.name}" for a in self.action_service.get_all()]
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return []
   
    def load_unit_values(self):
        try:
            return [f"{u.id}: {u.name}" for u in self.unit_service.get_all()]
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return []

    def load_recipe_list(self):
        recipes = self.recipe_service.get_ingredient_all()
        items = [f"{recipe.id}: {recipe.name}" for recipe in recipes]
        items.append("+ Nuevo...")
        self.recipe_list.set(items)

    def load_step_list(self):
        items = [
            f"{step.id}: " 
            f"{step.resultIngredient.name}: "
            f"{step.action.name}"
            for step in self.selected_recipe.steps
        ]
        items.append("+ Nuevo...")
        self.step_list_var.set(items)

    def save_recipe(self):
        self.set_name()
        self.set_price()
        try:
            self.recipe_service.save(self.selected_recipe)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        self.name_var.set('')
        self.price_var.set(float())
        self.load_recipe_list()
        self.recipe_listbox.focus_set()
        self.recipe_listbox.event_generate("<ButtonRelease-1>")
        self.show_recipe_environment()
        
    def save_step(self):
        try:
            self.flush_step_values()
            try:
                self.step_service.save(self.selected_step)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        except Exception:
            messagebox.showwarning("Debes llenar todos los datos antes de guardar el paso")
        self.selected_recipe = self.recipe_service.get_by_id(self.selected_recipe.id)
        if not self.recipe_service.is_complete(self.selected_recipe):
            self.price_var.set(float())
            self.save_recipe()
        self.load_step_list()
        self.step_listbox.focus_set()
        self.step_listbox.event_generate("<ButtonRelease-1>")
        self.show_step_environment()
        
    def delete_recipe(self):
        if self.selected_recipe.id:
            if messagebox.askokcancel("Eliminar receta", "¿ Estas seguro que deseas eliminar la receta y sus pasos ?"):
                try:
                    self.recipe_service.delete(self.selected_recipe.id)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                self.selected_recipe = RecipeDTO()
                self.name_var.set('')
                self.price_var.set(float())
                self.load_recipe_list()
                self.on_select_recipe(None)

    def delete_step(self):
        selection = self.step_listbox.curselection()
        if not selection:
            return
        index = selection[0]
        data = self.step_listbox.get(index)
        if data != "+ Nuevo...":
            if messagebox.askokcancel("Eliminar paso", "¿ Estas seguro que deseas eliminar el paso ?"):
                id = int(data.split(":")[0])
                try:
                    self.step_service.delete(id)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                self.clear_step_fields()
                self.load_step_list()
                self.show_recipe_environment()
                self.on_select_recipe(None)
                if not self.recipe_service.is_complete(self.selected_recipe):
                    self.price_var.set(float())
                    self.save_recipe()

    def on_select_recipe(self, event):
        index = self.recipe_listbox.curselection()[0]
        data = self.recipe_listbox.get(index)
        self.selected_step = StepDTO()
        if data == "+ Nuevo...":
            self.selected_recipe = RecipeDTO()
        else:
            id = int(data.split(":")[0])
            self.selected_recipe = self.recipe_service.get_by_id(id)
        self.name_var.set(self.selected_recipe.name)
        self.price_var.set(self.selected_recipe.price)
        self.load_step_list()
        self.show_recipe_environment() # modifico el entorno para recipe
        
    def on_select_step(self, event):
        if not self.selected_recipe or not self.selected_recipe.id: # si la receta no esta guardada no pueden cargarse pasos
            messagebox.showinfo("Antes de agregar pasos debes GUARDAR la receta")
            return
        self.clear_step_fields() 
        index = self.step_listbox.curselection()[0]
        data = self.step_listbox.get(index)
        if data == "+ Nuevo...":
            step = StepDTO(recipe_id=self.selected_recipe.id)
        else:
            id = int(data.split(":")[0])
            try:
                step = self.step_service.get_by_id(id)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        self.comboboxes = []
        self.selected_step = step
        self.show_sources()
        self.set_step_comboboxes(step)

    def set_step_comboboxes(self, step):
        if step.action.id:
            self.action_combobox.set(f"{step.action.id}: {step.action.name}")
        else:
            self.action_combobox.set('')
        if step.resultIngredient.id:
            self.result_ingredient_combobox.set(f"{step.resultIngredient.id}: {step.resultIngredient.name}")
        else:
            self.result_ingredient_combobox.set('')
        if step.resultUnit.id:
            self.result_unit_combobox.set(f"{step.resultUnit.id}: {step.resultUnit.name}")
        else:
            self.result_unit_combobox.set('')
        if step.resultQuantity:
            self.result_quantity_var.set(step.resultQuantity)
        self.show_step_environment() # modifico el entorno para step
    
    def clear_step_fields(self):
        self.action_combobox.set([])
        self.result_ingredient_combobox.set([])
        self.result_unit_combobox.set([])
        self.result_quantity_var.set(0)

    def show_step_environment(self):
        self.step_data_frame.pack(expand=True, fill="both", padx=50, pady=20) # muestro el frame con los datos del step 
        # muestro command buttons para step
        self.save_step_button.pack(expand=True )
        self.delete_step_button.pack(expand=True)
        # oculto los command buttons para recipe
        self.save_recipe_button.forget()
        self.delete_recipe_button.forget()
        self.entry_name.config(state="disabled")
        self.set_complete()
        self.entry_price.config(state="readonly")

    def show_recipe_environment(self):
        self.step_data_frame.forget()        # oculto el frame con los datos del step
        # muestro command buttons para recipe
        self.save_recipe_button.pack(expand=True )
        self.delete_recipe_button.pack(expand=True)
        # oculto los command buttons para step
        self.save_step_button.forget()
        self.delete_step_button.forget()
        self.entry_name.config(state="normal")
        self.set_complete()

    def set_complete(self):
        try:
            if self.recipe_service.is_complete(self.selected_recipe):
                self.is_complete.grid(row=0, column=4, padx=20)
                if self.recipe_service.has_ingredients(self.selected_recipe):
                    self.entry_price.config(state="readonly")
                else:
                    self.entry_price.config(state="normal")
            else:
                self.entry_price.config(state="readonly")
                self.is_complete.grid_remove()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def show_sources(self):
        step = self.selected_step
         # Limpio los widgets existentes del frame
        for widget in self.source_frame.winfo_children():
            widget.destroy()
        # Reinicio la lista de comboboxes
        self.comboboxes = []
        # Redibujo los headers (etiquetas de columna)
        label = tk.Label(self.source_frame, text="Ingrediente:")
        label.grid(row=0, column=1, padx=5, pady=5)
        label = tk.Label(self.source_frame, text="Unidad:")
        label.grid(row=0, column=2, padx=5, pady=5)
        label = tk.Label(self.source_frame, text="Cantidad:")
        label.grid(row=0, column=3, padx=5, pady=5)
        for row, source in enumerate(step.sources):
            ingredient_combobox = ttk.Combobox(self.source_frame, values=self.load_ingredient_values(), state="readonly")
            ingredient_combobox.bind("<Button-1>", lambda event, r=row: self.update_ingredient_values(event, r))  # agrego llamadas para actualizar valores de los combobox cuando reciben el foco
            ingredient_search = Seeker(ingredient_combobox, self.search_label_keys)
            ingredient_combobox.bind("<Key>", ingredient_search.search)
            ingredient_combobox.grid(row=row + 1, column=1, padx=(0,5), pady=5)

            unit_combobox = ttk.Combobox(self.source_frame, values=self.load_unit_values(), state="readonly")
            unit_combobox.bind("<Button-1>", lambda event, r=row: self.update_unit_values(event, r)) # agrego llamadas para actualizar valores de los combobox cuando reciben el foco
            unit_search = Seeker(unit_combobox, self.search_label_keys)
            unit_combobox.bind("<Key>", unit_search.search)
            unit_combobox.grid(row=row + 1, column=2, padx=5, pady=5)

            # agrego validaciones a los quantity entries
            vcmd = (self.register(only_float), "%P")
            quantity = tk.Entry(self.source_frame, validate="key", validatecommand=vcmd, width=5)
            quantity.grid(row=row + 1, column=3, padx=(5,0), pady=5)
            del_source_button = tk.Button(self.source_frame, text="-", command=lambda r=row: self.del_source(r))
            del_source_button.grid(row=row + 1, column=4, padx=(0,10), pady=5)
            self.comboboxes.append({"ingredient": ingredient_combobox,
                                    "unit": unit_combobox,
                                    "quantity": quantity,
                                    "del_button": del_source_button
                                    })
            if source.ingredient.id:
                ingredient_combobox.set(f"{source.ingredient.id}: {source.ingredient.name}")
            else:
                ingredient_combobox.set('')
            if source.unit.id:
                unit_combobox.set(f"{source.unit.id}: {source.unit.name}")
            else:
                unit_combobox.set('')
            quantity.insert(0, source.quantity)
        add_source_button = tk.Button(self.source_frame, text="+", command=self.add_blank_source)
        add_source_button.grid(row=len(step.sources)+1, column=0, padx=(10,0), pady=5)

    def add_blank_source(self):
        self.flush_step_values()
        self.selected_step.sources.append(SourceDTO(self.selected_step.id))
        self.show_sources()

    def del_source(self, row):
        self.flush_step_values()
        del self.selected_step.sources[row]
        del self.comboboxes[row]
        self.show_sources()

    def flush_step_values(self): # fuerza actualizar self.selected_step
        for row, widgets in enumerate(self.comboboxes):
            self.set_ingredient(row)
            self.set_unit(row)
            self.set_quantity(row)
        self.set_action()
        self.set_result_ingredient()
        self.set_result_unit()
        self.set_result_quantity()

    def set_name(self):
        self.selected_recipe.name = self.entry_name.get().strip()

    def set_price(self):
        self.selected_recipe.price = float(self.entry_price.get())
        
    def set_ingredient(self, row):
        try:
            id = int(self.comboboxes[row]["ingredient"].get().split(":")[0])
            self.selected_step.sources[row].ingredient = self.recipe_service.get_ingredient(id)
        except:
            pass

    def set_unit(self, row):
        try:
            id = int(self.comboboxes[row]["unit"].get().split(":")[0])
            try:
                self.selected_step.sources[row].unit = self.unit_service.get_by_id(id)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        except:
            pass

    def set_quantity(self, row):
        q = float(self.comboboxes[row]["quantity"].get())
        self.selected_step.sources[row].quantity = q

    def set_action(self):
        try:
            id = int(self.action_combobox.get().split(":")[0])
            try:
                self.selected_step.action = self.action_service.get_by_id(id)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        except:
            pass

    def set_result_ingredient(self):
        try:
            id = int(self.result_ingredient_combobox.get().split(":")[0])
            try:
                self.selected_step.resultIngredient = self.recipe_service.get_ingredient(id)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        except:
            pass

    def set_result_unit(self):
        try:
            id = int(self.result_unit_combobox.get().split(":")[0])
            try:
                self.selected_step.resultUnit = self.unit_service.get_by_id(id)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        except:
            pass
    
    def set_result_quantity(self):
        q = float(self.result_quantity.get())
        self.selected_step.resultQuantity = q
    
    def close(self):
        self.destroy()
