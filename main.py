# main.py
from models.db_initializer import createDatabase
from ui.main_window import KitchenApp

def main():
    # Creates the database if it does not exist
    createDatabase()

    # Create UI
    ui = KitchenApp()

    elements_frame = ui.add_frame(
            bd=3,
            relief="groove",
            padx=10,
            pady=10
            )
    
    ui.add_button(elements_frame, text='Unidades', command=ui.unit_crud)
    ui.add_button(elements_frame, text='Acciones', command=ui.action_crud)
    ui.add_button(elements_frame, text='Ingredientes', command=ui.ingredient_crud)
    ui.add_button(elements_frame, text='Recetas', command=ui.recipe_crud)
    
    ui.root.mainloop()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print('Error:', e)

