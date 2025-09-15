# recipes_vie
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from services.unit_service import UnitService
from services.recipe_service import RecipeService
from services.source_service import SourceService
from ui.views.widgets.seeker import Seeker
from ui.views.widgets.smart_listbox import SmartListbox
from ui.views.widgets.entry_validators import only_float
from ui.views.widgets.entry_validators import format_2dec
from dto.recipe_dto import RecipeDTO
from dto.source_dto import SourceDTO
from dto.unit_dto import UnitDTO
class RecipeView(tk.Frame):
    def __init__(self, parent): 
        super().__init__(parent, bd=4, relief="groove")
        # Services instances
        self.unit_service = UnitService()
        self.recipe_service = RecipeService()
        self.source_service = SourceService()
        self.selected_recipe = RecipeDTO()
        self.search_label_keys = tk.Label()

        self.recipe_names_var = tk.Variable(value=[]) 
        self.unit_names_var = tk.Variable(value=[])
        self.ingredient_names_var = tk.Variable(value=[])
        
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
        recipe_scrollbar = ttk.Scrollbar(recipe_frame, orient=tk.VERTICAL)
        self.recipe_listbox = SmartListbox(recipe_frame,
                                            exportselection=False,
                                            listvariable=self.recipe_names_var,
                                            yscrollcommand=recipe_scrollbar.set,
                                            activestyle=tk.NONE)
        recipe_scrollbar.config(command=self.recipe_listbox.yview)
        recipe_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.recipe_listbox.bind("<ButtonRelease-1>", self.on_select_recipe)
        self.recipe_listbox.bind("<Return>", self.on_select_recipe)
        self.recipe_listbox.bind("<Enter>", self.load_recipe_list)
        self.recipe_listbox.pack(expand=True, fill=tk.BOTH)
        
        # frame para los comandos
        command_frame = tk.Frame(self, bd=4, relief="groove")
        command_frame.grid(row=1, column=1, sticky="nsew")
            # frame para la busqueda
        search_frame = tk.Frame(command_frame, bd=1, relief="groove")
        search_frame.pack(expand=True)
    
        self.save_recipe_button = tk.Button(command_frame, text="Guardar Receta", command=self.save_recipe)
        self.save_recipe_button.bind("<Enter>", self.check_command_buttons)
        self.save_recipe_button.pack(expand=True )
        self.delete_recipe_button = tk.Button(command_frame, text="Eliminar Receta", command=self.delete_recipe)
        self.delete_recipe_button.bind("<Enter>", self.check_command_buttons)
        self.delete_recipe_button.pack(expand=True)
            # frame para la busqueda
        search_label = tk.Label(search_frame, text="Busqueda:", anchor="e", padx=5)
        self.search_label_keys = tk.Label(search_frame, width=20, anchor="w")
        search_label.pack(side="left")
        self.search_label_keys.pack(side="left")
        self.recipe_search = Seeker(self.recipe_listbox, self.search_label_keys) # buscador para lista de recetas
        self.recipe_listbox.bind("<Key>", self.recipe_search.search)

        # frame del formulario de entrada
        entry_frame = tk.Frame(self, bd=4, relief="groove")
        entry_frame.grid(row=3, column=0, columnspan=2, sticky="nsew")

        vcmd = (self.register(only_float), "%P") 

            # frame for recipe data
        recipe_frame = tk.LabelFrame(entry_frame, text="Receta", bd=2, relief="ridge")
        recipe_frame.pack(anchor="nw", padx=5, pady=20)

        label = tk.Label(recipe_frame, text="Cantidad:")
        label.grid(row=0, column=0, sticky="e", padx=(40, 5), pady=5)
        label = tk.Label(recipe_frame, text="Unidad:")
        label.grid(row=0, column=2, sticky="e", padx=(40, 5), pady=5)
        label = tk.Label(recipe_frame, text="Nombre:")
        label.grid(row=0, column=4, sticky="e", padx=(40, 5), pady=5)
        label = tk.Label(recipe_frame, text="Precio:")
        label.grid(row=0, column=6, sticky="e", padx=(40, 5), pady=5)
        self.result_quantity_var = tk.StringVar(value=f"{0:,.2f}")
        self.result_quantity = ttk.Entry(recipe_frame,
                                        textvariable=self.result_quantity_var,
                                        validate="key",
                                        validatecommand=vcmd,
                                        width=9,
                                        justify="right")     
        self.result_quantity.grid(row=0, column=1, sticky="w", padx=(5, 40), pady=5)
        self.result_quantity.bind("<FocusOut>", format_2dec)
        self.result_quantity.bind("<Leave>", self.check_command_buttons)
        
        self.result_unit_combobox = ttk.Combobox(recipe_frame, values=self.load_unit_values(), state="readonly")
        self.result_unit_combobox.bind("<Button-1>", self.load_unit_values) 
        self.result_unit_combobox.bind("<Leave>", self.check_command_buttons) 
        self.result_unit_search = Seeker(self.result_unit_combobox, self.search_label_keys)
        self.result_unit_combobox.bind("<Key>", self.result_unit_search.search)
        self.result_unit_combobox.grid(row=0, column=3, sticky="w", padx=(5, 40), pady=5)
        
        self.name_var = tk.StringVar()
        self.entry_name = ttk.Entry(recipe_frame,
                                    textvariable=self.name_var,
                                    width=50)
        self.entry_name.bind("<Leave>", self.check_command_buttons)
        self.entry_name.grid(row=0, column=5, sticky="w", padx=(5, 40), pady=5)
        
        self.price_var = tk.StringVar(value=f"{0:,.2f}")
        self.entry_price = ttk.Entry(recipe_frame,
                                    textvariable=self.price_var,
                                    validate="key",
                                    validatecommand=vcmd,
                                    width=15,
                                    justify="right")
        self.entry_price.grid(row=0, column=7, sticky="w", padx=(5, 40), pady=5 )
        self.entry_price.bind("<FocusOut>", format_2dec)
        self.entry_price.bind("<Leave>", self.check_command_buttons)
                        # frame para los sources
        self.source_frame = tk.LabelFrame(entry_frame, text="Ingredientes", bd=2, relief="ridge")
        self.source_frame.pack(anchor="nw", padx=5, pady=20)
        self.source_frame.columnconfigure(0, weight=0)
        self.source_frame.columnconfigure(1, weight=2)
        self.source_frame.columnconfigure(2, weight=2)
        self.source_frame.columnconfigure(3, weight=2)
        self.source_frame.columnconfigure(4, weight=0)
        self.show_sources()

        self.load_recipe_list()
        self.recipe_listbox.select_set(0)
        self.recipe_listbox.activate(0)
        self.recipe_listbox.event_generate("<ButtonRelease-1>")
       
    def load_ingredient_values(self, event=None):
        # descarto la posibilidad de tomar como ingrediente el que se esta definiendo
        try:
            ingredients =  self.recipe_service.get_ingredient_all()
            sorted_ingredients = sorted(ingredients, key=lambda ing: ing.name)
            names = [i.name for i in sorted_ingredients if not (self.selected_recipe and i.name == self.selected_recipe.name)] 
            self.ingredient_ids = [i.id for i in sorted_ingredients if not (self.selected_recipe and i.name == self.selected_recipe.name)] 
            self.ingredient_names_var.set(names)
            return names
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return []

    def load_unit_values(self, event=None):
        try:
            units = self.unit_service.get_all()
            sorted_units = sorted(units, key=lambda u: u.name)
            unit_names = [u.name for u in sorted_units]
            self.unit_ids = [u.id for u in sorted_units]
            self.unit_names_var.set(unit_names)
            return unit_names
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return []

    def load_recipe_list(self, event=None):
        recipes = self.recipe_service.get_ingredient_all()
        sorted_recipes = sorted(recipes, key=lambda r: r.name)
        names = [recipe.name for recipe in sorted_recipes]
        self.recipe_ids = [recipe.id for recipe in sorted_recipes]
        names.append("+ Nuevo...")
        self.recipe_names_var.set(names)

    def save_recipe(self):
        self.flush_values()
        try:
            self.recipe_service.save(self.selected_recipe)
            self.load_recipe_list()
            self.recipe_listbox.focus_set()
            self.recipe_listbox.select_clear(0, tk.END)
            index = self.recipe_names_var.get().index(self.selected_recipe.name)
            self.recipe_listbox.selection_set(index)
            self.recipe_listbox.event_generate("<ButtonRelease-1>")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        
    def delete_recipe(self):
        if self.selected_recipe.id:
            if messagebox.askokcancel("Eliminar receta", "¿ Estas seguro que deseas eliminar la receta y sus pasos ?"):
                try:
                    self.recipe_service.delete(self.selected_recipe.id)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                self.selected_recipe = RecipeDTO()
                self.show_sources()
                self.set_vars()
                self.load_recipe_list()
                self.on_select_recipe(None)

    def on_select_recipe(self, event):
        if self.discard_changes():
            index = self.recipe_listbox.curselection()[0]
            data = self.recipe_listbox.get(index)
            if data == "+ Nuevo...":
                self.selected_recipe = RecipeDTO()
            else:
                id = self.recipe_ids[index]
                self.selected_recipe = self.recipe_service.get_by_id(id)
            self.set_vars()
            self.show_sources()
            self.check_price()
            self.save_recipe_button.config(state="normal")
            self.delete_recipe_button.config(state="normal")
            self.check_command_buttons(event)

    def set_vars(self):
        self.result_quantity_var.set(value=f"{self.selected_recipe.result_quantity:,.2f}")
        result_unit = self.selected_recipe.result_unit
        self.result_unit_combobox.set(result_unit.name if result_unit.id else '')
        self.name_var.set(self.selected_recipe.name)
        self.price_var.set(value=f"{self.selected_recipe.price:,.2f}")

    def show_sources(self):
         # Limpio los widgets existentes del frame
        for widget in self.source_frame.winfo_children():
            widget.destroy()
        # Reinicio la lista de comboboxes
        self.comboboxes = []
        # Redibujo los headers (etiquetas de columna)
        label = tk.Label(self.source_frame, text="Ingrediente")
        label.grid(row=0, column=1, padx=170, pady=5)
        label = tk.Label(self.source_frame, text="Unidad")
        label.grid(row=0, column=2, padx=60, pady=5)
        label = tk.Label(self.source_frame, text="Cantidad")
        label.grid(row=0, column=3, padx=60, pady=5)
        for row, source in enumerate(self.selected_recipe.sources):
            ingredient_combobox = ttk.Combobox(self.source_frame, width=60, values=self.load_ingredient_values(), state="readonly")
            ingredient_combobox.bind("<Enter>", self.load_ingredient_values) 
            ingredient_combobox.bind("<Leave>", self.check_command_buttons)
            ingredient_search = Seeker(ingredient_combobox, self.search_label_keys)
            ingredient_combobox.bind("<Key>", ingredient_search.search)
            ingredient_combobox.grid(row=row + 1, column=1, padx=(0,5), pady=5)

            unit_combobox = ttk.Combobox(self.source_frame, values=self.load_unit_values(), state="readonly")
            unit_combobox.bind("<Enter>", self.load_unit_values)
            unit_combobox.bind("<Leave>", self.check_command_buttons)
            unit_search = Seeker(unit_combobox, self.search_label_keys)
            unit_combobox.bind("<Key>", unit_search.search)
            unit_combobox.grid(row=row + 1, column=2, padx=5, pady=5)

            vcmd = (self.register(only_float), "%P")
            quantity = tk.Entry(self.source_frame,
                                validate="key",
                                validatecommand=vcmd,
                                width=9,
                                justify="right")
            quantity.grid(row=row + 1, column=3, padx=(5,0), pady=5)
            quantity.bind("<FocusOut>", format_2dec)
            quantity.bind("<FocusOut>", self.check_command_buttons(None))

            del_source_button = tk.Button(self.source_frame, text="-", command=lambda r=row: self.del_source(r))
            del_source_button.grid(row=row + 1, column=4, padx=(0,10), pady=5)
            self.comboboxes.append({"ingredient": ingredient_combobox,
                                    "unit": unit_combobox,
                                    "quantity": quantity,
                                    "del_button": del_source_button
                                    })
            if source.ingredient.id:
                ingredient_combobox.set(source.ingredient.name)
            else:
                ingredient_combobox.set('')
            if source.unit.id:
                unit_combobox.set(source.unit.name)
            else:
                unit_combobox.set('')
            quantity.insert(0, f"{source.quantity:,.2f}")
        add_source_button = tk.Button(self.source_frame, text="+", command=self.add_blank_source)
        add_source_button.grid(row=len(self.selected_recipe.sources)+1, column=0, padx=(10,0), pady=5)

    def add_blank_source(self):
        self.flush_values()
        self.selected_recipe.sources.append(SourceDTO(self.selected_recipe.id))
        self.show_sources()
        self.check_price()

    def del_source(self, row):
        self.flush_values()
        del self.selected_recipe.sources[row]
        del self.comboboxes[row]
        self.show_sources()
        self.check_price()

    def check_price(self):
        if len(self.comboboxes) == 0:
            self.entry_price.config(state="normal")
        else:
            self.entry_price.config(state="disabled")
            self.selected_recipe.price = 0

    def flush_values(self): 
        self.flush_result_unit()
        self.selected_recipe.result_quantity = float(self.result_quantity.get().replace(",", ""))
        self.selected_recipe.name = self.entry_name.get().strip()
        self.selected_recipe.price = float(self.entry_price.get().replace(",", ""))
        for row, widgets in enumerate(self.comboboxes):
            self.selected_recipe.sources[row].quantity = float(self.comboboxes[row]["quantity"].get().replace(",", ""))
            self.flush_source_unit(row)
            self.flush_source_ingredient(row)

    def flush_result_unit(self):
        try:
            index = self.result_unit_combobox.current()
            if index == -1:
                id = None
            else:
                id = self.unit_ids[index]
            try:
                self.selected_recipe.result_unit = self.unit_service.get_by_id(id)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        except:
            pass

    def flush_source_unit(self, row):
        try:
            index = self.comboboxes[row]["unit"].current()
            if index == -1:
                id = None
            else:
                id = self.unit_ids[index]
            try:
                self.selected_recipe.sources[row].unit = self.unit_service.get_by_id(id)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        except:
            pass

    def flush_source_ingredient(self, row):
        try:
            index = self.comboboxes[row]["ingredient"].current()
            if index == -1:
                id = None
            else:
                id = self.ingredient_ids[index]
            self.selected_recipe.sources[row].ingredient = self.recipe_service.get_ingredient(id)
        except:
            pass

    def close(self):
        if self.discard_changes():
            self.destroy()
        
    def discard_changes(self):
        self.check_command_buttons(None)
        if self.save_recipe_button.cget("state") == "normal" and not messagebox.askokcancel("Receta modificada", "¿Estas seguro de descartar los cambios?"):
            return False
        return True
    
    def check_command_buttons(self, event):
        self.flush_values()
        if self.selected_recipe.id:
            self.delete_recipe_button.config(state="normal")
            if self.selected_recipe == self.recipe_service.get_by_id(self.selected_recipe.id):
                self.save_recipe_button.config(state="disabled")
            else:
                self.save_recipe_button.config(state="normal")
        else:
            self.delete_recipe_button.config(state="disabled")
            if (self.selected_recipe.result_quantity and 
                self.selected_recipe.result_unit and
                self.selected_recipe.name != ""):
                self.save_recipe_button.config(state="normal")
            else:
                self.save_recipe_button.config(state="disabled")
