# elements_view.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ui.views.widgets.seeker import Seeker
from ui.views.widgets.smart_listbox import SmartListbox
from services.unit_service import UnitService
from services.unit_converter_service import UnitConverterService
from dto.unit_dto import UnitDTO
from dto.unit_converter_dto import UnitConverterDTO

class UnitConverter(tk.Frame):
    def __init__(self, parent): 
        super().__init__(parent, bd=4, relief="groove")
        self.unit_service = UnitService()
        self.selected_unit = UnitDTO()
        self.entries = {}
       
        # frame definition
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        top_frame = tk.Frame(self, bd=4, relief="groove")
        list_frame = tk.Frame(self, bd=4, relief="groove")
        self.command_frame = tk.Frame(self, bd=4, relief="groove")
       
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")
        list_frame.grid(row=1, column=0, sticky="nsew")
        self.command_frame.grid(row=1, column=1, sticky="nsew")
        
        # title
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=0)
        title_button = tk.Button(top_frame, text="Unidades de conversion", font=("TkCaptionFont", 12), relief="flat")
        close_button = tk.Button(top_frame, text="X", command=self.close)
        title_button.grid(row=0, column=0, sticky="ew")
        close_button.grid(row=0, column=1, sticky="e")

        # command buttons
        search_frame = tk.Frame(self.command_frame)
        search_label = tk.Label(search_frame, text="Busqueda:", anchor="e")
        self.search_label_keys = tk.Label(search_frame, width=20, anchor="w")
        search_label.pack(side="left")
        self.search_label_keys.pack(side="left")
        search_frame.pack(expand=True)
        
        self.save_button = tk.Button(self.command_frame, text="Guardar")
        self.save_button.pack(expand=True)
        self.delete_button = tk.Button(self.command_frame, text="Eliminar")
        self.delete_button.pack(expand=True)
        self.save_button.config(state="disabled")
        self.delete_button.config(state="disabled")
       
        # variable tk que almacene lista elementos para ser mostrada en el listbox
        self.unit_list_var = tk.Variable(value=[])    

        # lista de elementos
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.unit_listbox = SmartListbox(
                                        list_frame,
                                        exportselection=False,
                                        listvariable=self.unit_list_var,
                                        yscrollcommand=scrollbar.set,
                                        activestyle=tk.NONE)
        self.unit_listbox.bind("<ButtonRelease-1>", self.on_select_unit)
        self.unit_listbox.bind("<Return>", self.on_select_unit)
        self.unit_listbox.bind("<Enter>", self.load_unit_list)
 
        # buscador para lista de elementos
        self.listbox_search = Seeker(self.unit_listbox, self.search_label_keys)
        self.unit_listbox.bind("<Key>", self.listbox_search.search)

        scrollbar.config(command=self.unit_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.unit_listbox.pack(expand=True, fill=tk.BOTH)

        self.load_unit_list()
        self.unit_listbox.selection_set(0)
        # self.on_select_unit(None)
        
    def load_unit_list(self, event=None):
        try:
            units = self.unit_service.get_all()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        list = [f"{unit.id}: {unit.name}" for unit in units]
        self.unit_list_var.set(list)
        
    def on_select_unit(self, event):
        try:
            index = self.unit_listbox.curselection()[0]
            data = self.unit_listbox.get(index)
            id = int(data.split(":")[0])
            try:
                self.selected_unit = self.unit_service.get_by_id(id)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        except IndexError:
            pass
        finally:
            unit_converter_frame = UnitConverterFrame(self, bd=4, relief="groove")
            unit_converter_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
        
    def close(self):
        self.destroy()

class UnitConverterFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.unit_converter_list_var = tk.Variable(value=[])    
        self.unit_converter_service = UnitConverterService()
        self.unit_service = UnitService()
        self.selected_source_unit = parent.selected_unit
        self.parent = parent

        # destroy old buttons
        for widget in self.parent.command_frame.winfo_children():
            widget.destroy()

        # command buttons
        search_frame = tk.Frame(self.parent.command_frame)
        search_label = tk.Label(search_frame, text="Busqueda:", anchor="e")
        search_label_keys = tk.Label(search_frame, width=20, anchor="w")
        search_label.pack(side="left")
        search_label_keys.pack(side="left")
        search_frame.pack(expand=True)
        
        self.save_button = tk.Button(parent.command_frame, text="Guardar", command=self.save)
        self.save_button.pack(expand=True)
        self.delete_button = tk.Button(parent.command_frame, text="Eliminar", command=self.delete)
        self.delete_button.pack(expand=True)
        self.save_button.config(state="disabled")
        self.delete_button.config(state="disabled")

        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL)
        self.unit_converter_listbox = SmartListbox(
                                                    self,
                                                    exportselection = False, 
                                                    listvariable=self.unit_converter_list_var,
                                                    yscrollcommand=scrollbar.set,
                                                    activestyle=tk.NONE)
        self.unit_converter_listbox.bind("<ButtonRelease-1>", self.on_select_unit_converter)
        self.unit_converter_listbox.bind("<Return>", self.on_select_unit_converter)
        self.unit_converter_listbox.bind("<Enter>", self.load_unit_converter_list)
 
        # buscador para lista de elementos
        self.listbox_search = Seeker(self.unit_converter_listbox, search_label_keys)
        self.unit_converter_listbox.bind("<Key>", self.listbox_search.search)

        scrollbar.config(command=self.unit_converter_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.unit_converter_listbox.pack(expand=True, fill=tk.BOTH)

        entries_frame = tk.Frame(self, bd=4, relief="groove")
        entries_frame.pack(expand=True, fill=tk.BOTH)
        FONT = ("Arial", 14)
        one_label = tk.Label(entries_frame, text= "1", font=FONT)
        one_label.pack(side="left", pady=100, padx=(60,10))
        self.source_unit_var = tk.StringVar()
        self.source_unit_var.set(self.selected_source_unit.name)
        source_unit_label = tk.Label(entries_frame, textvariable=self.source_unit_var, font=FONT)
        source_unit_label.pack(side="left", pady=100, padx=10)
        eq_label = tk.Label(entries_frame, text= "=", font=FONT)
        eq_label.pack(side="left", pady=100, padx=10)
        self.quantity_var = tk.DoubleVar()
        quantity_entry = tk.Entry(entries_frame, textvariable=self.quantity_var, width=8, font=FONT)
        quantity_entry.pack(side="left", pady=100, padx=10)
        self.target_unit_var = tk.Variable()
        target_unit_combobox = ttk.Combobox(entries_frame, textvariable=self.target_unit_var, values=self.load_unit_values(), font=FONT)
        target_unit_combobox.pack(side="left", pady=100, padx=10)
        
        self.load_unit_converter_list()
        self.unit_converter_listbox.select_set(0)

    def load_unit_converter_list(self, event=None):
        try:
            units_converter = self.unit_converter_service.get_all(self.selected_source_unit.id)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        list = [f"{unit_converter.id}: ----> {unit_converter.target_unit.name}" for unit_converter in units_converter]
        list.append("+ Nuevo...")
        self.unit_converter_list_var.set(list)

    def load_unit_values(self):
        try:
            return [f"{u.id}: {u.name}" for u in self.unit_service.get_all() if u.id != self.selected_source_unit.id]
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return []

    def on_select_unit_converter(self, event):
        try:
            index = self.unit_converter_listbox.curselection()[0]
            data = self.unit_converter_listbox.get(index)
            if data == "+ Nuevo...":
                self.selected_unit_converter = UnitConverterDTO()
            else:
                id = int(data.split(":")[0])
                try:
                    self.selected_unit_converter = self.unit_converter_service.get_by_id(id)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
        except IndexError:
            pass
        finally:
            self.show_unit_converter()
            self.save_button.config(state="normal")
            self.delete_button.config(state="normal")

    def save(self):
        try:
            self.flush_values()
            self.unit_converter_service.save(self.selected_unit_converter)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        self.save_button.config(state="disabled")
        self.delete_button.config(state="disabled")

    def delete(self):
        try:
            self.unit_converter_service.delete(self.selected_unit_converter.id)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def flush_values(self):
        self.selected_unit_converter.source_unit = self.selected_source_unit
        self.selected_unit_converter.quantity = self.quantity_var.get()
        target_unit_id = int(self.target_unit_var.get().split(":")[0])
        self.selected_unit_converter.target_unit = self.unit_service.get_by_id(target_unit_id)

    def show_unit_converter(self):
        self.quantity_var.set(self.selected_unit_converter.quantity)
        unit = self.selected_unit_converter.target_unit
        self.target_unit_var.set(f"{unit.id}: {unit.name}" if unit.id else "")

