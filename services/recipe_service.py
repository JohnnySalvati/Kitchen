from models.recipe_model import Recipe
from models.step_model import Step
from dto.recipe_dto import RecipeDTO

class RecipeService:
    def save(self, recipeDTO):
        if not recipeDTO.name or not recipeDTO.name.strip():
            raise ValueError("El nombre no puede estar vacio")
        if recipeDTO.price is None or recipeDTO.price < 0:
            raise ValueError("El precio no puede ser menor que 0")
        try:
            recipe = RecipeDTO.to_model(recipeDTO)
            return recipe.save()
        except Exception as e:
            raise RuntimeError(f"No se pudo crear la receta: {e}")

    def get_by_id(self, id):
        recipe = Recipe.get_one("id", id)
        if not recipe.id:
            raise ValueError(f"No exite accion con ID {id}")
        return RecipeDTO.from_model(recipe)
    
    def get_all(self):
        recipes = Recipe.get_all()
        return [RecipeDTO.from_model(recipe) for recipe in recipes]
    
    def get_ingredient_all(self):
        try:
            ingredients = Recipe.get_ingredients()
            return [RecipeDTO.from_model(ingredient) for ingredient in ingredients]
        except Exception as e:
            raise RuntimeError(f"No se pudieron obtener ingredientes: {e}")

    def get_ingredient(self, id):
        try:
            ingredient = Recipe.get_ingredient(id)
            return RecipeDTO.from_model(ingredient)
        except Exception as e:
            raise RuntimeError(f"No se pudo obtener el ingrediente {id}: {e}")
        
    def is_complete(self, id):
        try:
            recipe = Recipe.get_one("id", id)
        except Exception as e:
            raise RuntimeError(f"No se pudo obtener el ingrediente {id}: {e}")
        return recipe.is_complete()
    
    def has_ingredients(self, id):
        try:
            recipe = Recipe.get_one("id", id)
        except Exception as e:
            raise RuntimeError(f"No se pudo obtener el ingrediente {id}: {e}")
        return recipe.has_ingredients()

    def delete(self, id):
        recipe = Recipe.get_one("id", id)
        if recipe.id:
            recipe.delete()
        else:
            raise ValueError(f"No existe receta con ID {id}")