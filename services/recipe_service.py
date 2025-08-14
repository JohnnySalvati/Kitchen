from models.recipe_model import Recipe
from models.step_model import Step

class RecipeService:
    def create(self, name: str="", price: float=0, steps: list[Step]=[]):
        try:
            Recipe(name=name, price=price, steps=steps)
        except Exception as e:
            raise RuntimeError(f"No se pudo crear la receta: {e}")

    def get_by_id(self, id):
        return Recipe.get_one("id", id) or self.create()
    
    @classmethod
    def get_all(cls):
        return Recipe.get_all()
    
    def add_recipe(self, name: str, price: float, steps: list[Step]):
        if not name or not name.strip():
            raise ValueError("El nombre no puede estar vacio")
        if price is None or price < 0:
            raise ValueError("El precio no puede ser menor que 0")
        try:
            recipe = Recipe(name=name, price=price, steps=steps)
            recipe.save()
        except Exception as e:
            raise RuntimeError(f"No se pudo crear la receta: {e}")
        
    @classmethod
    def get_ingredients(cls):
        try:
            return Recipe.get_ingredients()
        except Exception as e:
            raise RuntimeError(f"No se pudo obtener ingredientes: {e}")

    @classmethod
    def get_ingredient(cls, id):
        try:
            return Recipe.get_ingredient(id)
        except Exception as e:
            raise RuntimeError(f"No se pudo obtener el ingrediente {id}: {e}")
