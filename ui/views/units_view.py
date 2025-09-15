
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ui.views.widgets.seeker import Seeker
from ui.views.widgets.smart_listbox import SmartListbox
from services.unit_service import UnitService
from dto.unit_dto import UnitDTO

class UnitView(tk.Frame):
    def __init__(self, parent): 
        super().__init__(parent, bd=4, relief="groove")
        self.unit_service = UnitService()
        self.selected_unit = UnitDTO()
       
        # frame definition
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        top_frame = tk.Frame(self, bd=4, relief="groove")
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        list_frame = tk.Frame(self, bd=4, relief="groove")
        list_frame.grid(row=1, column=0, sticky="nsew")

        command_frame = tk.Frame(self, bd=4, relief="groove")
        command_frame.grid(row=1, column=1, sticky="nsew")

        entry_frame = tk.Frame(self, bd=4, relief="groove")
        entry_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        
        # title
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=0)

        title_button = tk.Button(top_frame, text="Unidades", font=("TkCaptionFont", 12), relief="flat")
        title_button.grid(row=0, column=0, sticky="ew")

        close_button = tk.Button(top_frame, text="X", command=self.close)
        close_button.grid(row=0, column=1, sticky="e")

        # search frame
        search_frame = tk.Frame(command_frame, bd=2, relief="groove")
        search_frame.pack(expand=True, fill="both")

        search_label = tk.Label(search_frame, text="Busqueda:", anchor="e")
        search_label_keys = tk.Label(search_frame, width=20, anchor="w")
        search_label.pack(side="left")
        search_label_keys.pack(side="left")

        # buttons frame
        buttons_frame = tk.Frame(command_frame, bd=2, relief="groove")
        buttons_frame.pack(expand=True, fill="both")
        self.save_button = tk.Button(buttons_frame, text="Guardar", command=self.save_unit)
        self.save_button.pack(expand=True)
        self.save_button.config(state="disabled")

        self.delete_button = tk.Button(buttons_frame, text="Eliminar", command=self.delete_unit)
        self.delete_button.pack(expand=True)
        self.save_button.config(state="disabled")

        # formulario de entrada
        label = tk.Label(entry_frame, text="Nombre")
        label.grid(row=0, column=0, sticky="e", padx=5, pady=5)
        label = tk.Label(entry_frame, text="Abreviatura")
        label.grid(row=1, column=0, sticky="e", padx=5, pady=5)

        self.name_entry = tk.Entry(entry_frame)
        self.name_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.name_entry.bind("<Leave>", self.check_command_buttons)
        self.name_entry.bind("<Key>", self.check_command_buttons)

        self.short_name_entry = tk.Entry(entry_frame)
        self.short_name_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        self.short_name_entry.bind("<Leave>", self.check_command_buttons)
        self.short_name_entry.bind("<Key>", self.check_command_buttons)
        
        # variable tk que almacene lista elementos para ser mostrada en el listbox
        self.units_list = tk.Variable(value=[])
        self.id_list = []

        # lista de elementos
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.listbox = SmartListbox(list_frame, 
                                    listvariable=self.units_list,
                                    yscrollcommand=scrollbar.set,
                                    activestyle=tk.NONE)
        self.listbox.bind("<ButtonRelease-1>", self.on_select)
        self.listbox.bind("<Return>", self.on_select)
        # buscador para lista de elementos
        self.listbox_search = Seeker(self.listbox, search_label_keys)
        self.listbox.bind("<Key>", self.listbox_search.search)

        scrollbar.config(command=self.listbox.yview)

        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.pack(expand=True, fill=tk.BOTH)
        
        self.load_all()
        self.listbox.focus_set()

    def check_command_buttons(self, event):
        self.flush_values()
        if self.selected_unit.id:
            self.delete_button.config(state="normal")
            if self.selected_unit == self.unit_service.get_by_id(self.selected_unit.id):
                self.save_button.config(state="disabled")
            else:
                self.save_button.config(state="normal")
        else:
            self.delete_button.config(state="disabled")
            if self.selected_unit.name:
                self.save_button.config(state="normal")
            else:
                self.save_button.config(state="disabled")

    def flush_values(self):
        self.selected_unit.name = self.name_entry.get().strip()
        self.selected_unit.short_name = self.short_name_entry.get().strip()

    def load_all(self):
        try:
            units = self.unit_service.get_all()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        sorted_units = sorted(units, key=lambda unit: unit.name)
        names = [unit.name for unit in sorted_units]
        names.append("+ Nuevo...")
        self.units_list.set(names)
        self.id_list = [unit.id for unit in sorted_units]
        
    def save_unit(self):
        self.flush_values()
        try:
            self.selected_unit = self.unit_service.save(self.selected_unit)
            self.load_all()
            self.select_current()
            self.listbox.event_generate("<ButtonRelease-1>")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        

    def delete_unit(self):
        if self.selected_unit.id:
            if messagebox.askokcancel("Eliminar unidad", "¿Estas seguro de eliminar la unidad?"):
                try:
                    self.unit_service.delete(self.selected_unit.id)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
                self.selected_unit = UnitDTO()
                self.clear_fields()
                self.load_all()
                self.listbox.event_generate("<ButtonRelease-1>")

    def on_select(self, event):
        if self.discard_changes():
            try:
                index = self.listbox.curselection()[0]
                data = self.listbox.get(index)
                self.clear_fields()
                if data == "+ Nuevo...":
                    self.selected_unit = UnitDTO()
                else:
                    id = self.id_list[index]
                    self.selected_unit = self.unit_service.get_by_id(id)
                self.name_entry.insert(0, self.selected_unit.name)
                self.short_name_entry.insert(0, self.selected_unit.short_name)
            except IndexError:
                print("Exception")
            self.save_button.config(state="normal")
            self.delete_button.config(state="normal")
            self.check_command_buttons(event)
        self.select_current()


    def clear_fields(self):
        self.name_entry.delete(0, tk.END)
        self.short_name_entry.delete(0, tk.END)

    def select_current(self):
        list = self.units_list.get()
        self.listbox.select_clear(0, tk.END)
        if self.selected_unit.id:
            try:
                index = list.index(self.selected_unit.name)
                self.listbox.select_set(index)
            except ValueError:
                id = self.selected_unit.id
                if id:
                    name = self.unit_service.get_by_id(self.selected_unit.id).name
                    index = list.index(name)
                    self.listbox.select_set(index)
        else:
            self.listbox.select_set(tk.END)

    def close(self):
        if self.discard_changes():
            self.destroy()
        return

    def discard_changes(self):
        self.check_command_buttons(None)
        if self.save_button.cget("state") == "normal" and not messagebox.askokcancel("Cerrar ventana", "¿Estas seguro de descartar los cambios?"):
            return False
        return True