# elements_view.py
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ui.views.widgets.seeker import Seeker
from ui.views.widgets.smart_listbox import SmartListbox
from ui.views.widgets.entry_validators import only_float
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
        self.unit_converter_frame = None
        FONT = ("CourierNew", 10)
      
        # frame definition
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

        top_frame = tk.Frame(self, bd=4, relief="groove")
        top_frame.grid(row=0, column=0, columnspan=2, sticky="ew")

        list_frame = tk.Frame(self, bd=4, relief="groove")
        list_frame.grid(row=1, column=0, sticky="nsew")

        self.command_frame = tk.Frame(self, bd=4, relief="groove")
        self.command_frame.grid(row=1, column=1, sticky="nsew")
        
        # title
        top_frame.columnconfigure(0, weight=1)
        top_frame.columnconfigure(1, weight=0)

        title_button = tk.Button(top_frame, text="Unidades de conversion", font=("TkCaptionFont", 12), relief="flat")
        title_button.grid(row=0, column=0, sticky="ew")

        close_button = tk.Button(top_frame, text="X", command=self.close)
        close_button.grid(row=0, column=1, sticky="e")

        # search frame
        search_frame = tk.Frame(self.command_frame, bd=2, relief="groove")
        search_frame.pack(expand=True, fill="both")

        search_label = tk.Label(search_frame, text="Busqueda:", anchor="e")
        search_label.pack(side="left")

        self.search_label_keys = tk.Label(search_frame, width=20, anchor="w")
        self.search_label_keys.pack(side="left")

        # buttons frame
        button_frame = tk.Frame(self.command_frame, bd=2, relief="groove")
        button_frame.pack(expand=True, fill="both")

        self.save_button = tk.Button(button_frame, text="Guardar")
        self.save_button.pack(expand=True)
        self.save_button.config(state="disabled")

        self.delete_button = tk.Button(button_frame, text="Eliminar")
        self.delete_button.pack(expand=True)
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
                                        activestyle=tk.NONE,
                                        font= FONT)
        scrollbar.config(command=self.unit_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.unit_listbox.bind("<ButtonRelease-1>", self.on_select_unit)
        self.unit_listbox.bind("<Return>", self.on_select_unit)
        self.unit_listbox.bind("<ButtonRelease-1>", self.load_unit_list, add='+')
        listbox_search = Seeker(self.unit_listbox, self.search_label_keys)
        self.unit_listbox.bind("<Key>", listbox_search.search)
        self.unit_listbox.pack(expand=True, fill=tk.BOTH)

        self.load_unit_list()
        self.unit_listbox.focus_set()
        
    def load_unit_list(self, event=None):
        try:
            units = self.unit_service.get_all()
        except Exception as e:
            messagebox.showerror("Error", str(e))
        sorted_units = sorted(units, key=lambda unit: unit.name)
        list = [unit.name for unit in sorted_units]
        self.unit_list_var.set(list)
        self.unit_list_id = [unit.id for unit in sorted_units]
        
    def on_select_unit(self, event):
        if self.discard_changes():
            try:
                index = self.unit_listbox.curselection()[0]
                id = self.unit_list_id[index]
                try:
                    self.selected_unit = self.unit_service.get_by_id(id)
                except Exception as e:
                    messagebox.showerror("Error", str(e))
            except IndexError:
                pass
            finally:
                self.save_button.config(state="disabled")
                self.delete_button.config(state="disabled")
                self.unit_converter_frame = UnitConverterFrame(self, bd=4, relief="groove")
                self.unit_converter_frame.grid(row=2, column=0, columnspan=2, sticky="nsew")
                self.after(10, lambda: self.select_first_unit_converter())

    def select_first_unit_converter(self):
        listbox = self.unit_converter_frame.unit_converter_listbox # type: ignore
        if listbox.size() > 0:
            listbox.select_set(0)
            listbox.activate(0)
            listbox.event_generate("<ButtonRelease-1>")
        
    def close(self):
        if self.discard_changes():
            self.destroy()

    def discard_changes(self):
        if self.unit_converter_frame:
            self.unit_converter_frame.check_command_buttons(None)
        if self.save_button.cget("state") == "normal" and not messagebox.askokcancel("Unidad de conversion modificada", "¿Estas seguro de descartar los cambios?"):
            return False
        return True
class UnitConverterFrame(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.unit_converter_list_var = tk.Variable(value=[])    
        self.unit_converter_service = UnitConverterService()
        self.unit_service = UnitService()
        self.selected_unit_converter = UnitConverterDTO()
        self.previous_unit_converter = 0
        self.selected_source_unit = parent.selected_unit
        self.save_button = parent.save_button
        self.delete_button = parent.delete_button
        self.search_label_keys = parent.search_label_keys
        self.discard_changes = parent.discard_changes
        
        self.save_button.config(command=self.save)
        self.delete_button.config(command=self.delete)

        listbox_frame = tk.Frame(self)
        listbox_frame.pack(expand=True, fill=tk.BOTH)

        scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL)
        self.unit_converter_listbox = SmartListbox(
                                                    listbox_frame,
                                                    exportselection = False, 
                                                    listvariable=self.unit_converter_list_var,
                                                    yscrollcommand=scrollbar.set,
                                                    activestyle=tk.NONE,
                                                    font = ("CourierNew", 10))
        scrollbar.config(command=self.unit_converter_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.unit_converter_listbox.bind("<ButtonRelease-1>", self.on_select_unit_converter)
        self.unit_converter_listbox.bind("<Return>", self.on_select_unit_converter)
        # self.unit_converter_listbox.bind("<Enter>", self.load_unit_converter_list)
        listbox_search = Seeker(self.unit_converter_listbox, self.search_label_keys)
        self.unit_converter_listbox.bind("<Key>", listbox_search.search)
        self.unit_converter_listbox.pack(expand=True, fill=tk.BOTH)

        FONT = ("CourierNew", 15)
        entries_frame = tk.Frame(self, bd=4, relief="groove")
        entries_frame.pack(expand=True, fill=tk.BOTH)

        one_label = tk.Label(entries_frame, text= "1", font=FONT)
        one_label.pack(side="left", pady=100, padx=(60,10))

        self.source_unit_var = tk.StringVar()
        self.source_unit_var.set(self.selected_source_unit.name)

        source_unit_label = tk.Label(entries_frame, textvariable=self.source_unit_var, font=FONT)
        source_unit_label.pack(side="left", pady=100, padx=10)

        eq_label = tk.Label(entries_frame, text= "=", font=FONT)
        eq_label.pack(side="left", pady=100, padx=10)

        vcmd = (self.register(only_float), "%P")
        self.quantity_var = tk.StringVar()
        quantity_entry = tk.Entry(entries_frame,
                                validate="key",
                                validatecommand=vcmd,
                                textvariable=self.quantity_var,
                                justify="right",
                                width=8,
                                font=FONT)
        quantity_entry.bind("<Leave>", self.check_command_buttons)
        quantity_entry.pack(side="left", pady=100, padx=10)

        self.target_unit_var = tk.Variable()
        self.target_unit_combobox = ttk.Combobox(entries_frame, textvariable=self.target_unit_var,values=self.load_target_unit_values(), font=FONT, state="readonly")
        self.target_unit_combobox.bind("<<ComboboxSelected>>", self.check_command_buttons)
        self.target_unit_combobox.pack(side="left", pady=100, padx=10)
        target_unit_search = Seeker(self.target_unit_combobox, self.search_label_keys)
        self.target_unit_combobox.bind("<Key>", target_unit_search.search)
        
        self.load_unit_converter_list()
        self.unit_converter_listbox.select_set(0)

    def load_unit_converter_list(self, event=None):
        try:
            units_converter = self.unit_converter_service.get_all(self.selected_source_unit.id)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        sorted_units_converter = sorted(units_converter, key=lambda unit_converter: unit_converter.target_unit.name)
        list = [f"{unit_converter.source_unit.name.ljust(25)} --> {unit_converter.quantity:8,.2f} {unit_converter.target_unit.name}" for unit_converter in sorted_units_converter]
        list.append("+ Nuevo...")
        self.unit_converter_list_var.set(list)
        self.unit_converter_list_id = [unit_converted.id for unit_converted in sorted_units_converter]

    def load_target_unit_values(self):
        try:
            units = [u for u in self.unit_service.get_all() if u.id != self.selected_source_unit.id]
            sorted_units = sorted(units, key=lambda unit: unit.name)
            self.target_unit_ids = [unit.id for unit in sorted_units]
            return [unit.name for unit in sorted_units]
        except Exception as e:
            messagebox.showerror("Error", str(e))
            self.target_unit_ids = []
            return []

    def on_select_unit_converter(self, event):
        if self.discard_changes():
            try:
                index = self.unit_converter_listbox.curselection()[0]
                self.previous_unit_converter = index
                data = self.unit_converter_listbox.get(index)
                if data == "+ Nuevo...":
                    self.selected_unit_converter = UnitConverterDTO()
                else:
                    id = self.unit_converter_list_id[index]
                    try:
                        self.selected_unit_converter = self.unit_converter_service.get_by_id(id)
                    except Exception as e:
                        messagebox.showerror("Error", str(e))
            except IndexError:
                pass
            finally:
                self.set_unit_converter()
                self.save_button.config(state="normal")
                self.delete_button.config(state="normal")
                self.check_command_buttons(event)
        else:
            self.unit_converter_listbox.selection_clear(0, tk.END)
            self.unit_converter_listbox.select_set(self.previous_unit_converter)
            self.unit_converter_listbox.activate(self.previous_unit_converter)

    def save(self):
        try:
            self.flush_values()
            self.selected_unit_converter = self.unit_converter_service.save(self.selected_unit_converter)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        self.load_unit_converter_list()
        self.save_button.config(state="disabled")
        self.delete_button.config(state="disabled")

    def delete(self):
        try:
            self.unit_converter_service.delete(self.selected_unit_converter.id)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        self.selected_unit_converter = UnitConverterDTO()
        self.set_unit_converter()
        self.load_unit_converter_list()
        self.save_button.config(state="disabled")
        self.delete_button.config(state="disabled")

    def flush_values(self):
        self.selected_unit_converter.source_unit = self.selected_source_unit
        quantity = self.quantity_var.get().replace(",", "")
        self.selected_unit_converter.quantity = float(quantity) if quantity else 0.0
        index = self.target_unit_combobox.current()
        target_unit_id = self.target_unit_ids[index]
        self.selected_unit_converter.target_unit = self.unit_service.get_by_id(target_unit_id)

    def set_unit_converter(self):
        self.quantity_var.set(f"{self.selected_unit_converter.quantity:,.2f}")
        unit = self.selected_unit_converter.target_unit
        self.target_unit_var.set(unit.name if unit.id else "")

    def check_command_buttons(self, event):
        self.flush_values()
        if self.selected_unit_converter.id:
            self.delete_button.config(state="normal")
            if self.selected_unit_converter == self.unit_converter_service.get_by_id(self.selected_unit_converter.id):
                self.save_button.config(state="disabled")
            else:
                self.save_button.config(state="normal")
        else:
            self.delete_button.config(state="disabled")
            if self.selected_unit_converter.quantity and self.selected_unit_converter.target_unit:
                self.save_button.config(state="normal")
            else:
                self.save_button.config(state="disabled")

