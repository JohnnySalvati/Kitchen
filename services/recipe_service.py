from models.recipe_model import Recipe
from dto.recipe_dto import RecipeDTO
from collections import defaultdict
from services.step_service import StepService
step_service = StepService()

class RecipeService:

    def save(self, recipeDTO):
        if not recipeDTO.name or not recipeDTO.name.strip():
            raise ValueError("El nombre no puede estar vacio")
        if recipeDTO.price is None or recipeDTO.price < 0:
            raise ValueError("El precio no puede ser menor que 0")
        try:
            recipe = RecipeDTO.to_model(recipeDTO)
            recipe.save()
            step_service.update_steps(recipe.id, recipeDTO.steps)
            return 
        except Exception as e:
            raise RuntimeError(f"No se pudo crear la receta: {e}")

    def get_by_id(self, id):
        recipe = Recipe.get_one("id", id)
        steps = step_service.get_all(id)
        recipeDTO = RecipeDTO.from_model(recipe, steps)
        return recipeDTO
    
    def get_all(self):
        recipesDTO = []
        recipes = Recipe.get_all()
        for recipe in recipes:
            steps = step_service.get_all(recipe.id)
            recipesDTO.append(RecipeDTO.from_model(recipe, steps))
        return recipesDTO
    
    def get_ingredient(self, id):
        recipe = Recipe.get_one("id", id)
        if not recipe.id:
            raise ValueError(f"No exite receta con ID {id}")
        recipeDTO = RecipeDTO.from_model(recipe)
        return recipeDTO

    def get_ingredient_all(self):
        recipes = Recipe.get_all()
        return [RecipeDTO.from_model(recipe) for recipe in recipes]
    
    def is_complete(self, recipe_object):
        """Determines if Recipe or RecipeDTO is complete, to be used like ingredient"""
        recipeDTO = self.get_by_id(recipe_object.id)
        if not recipeDTO.steps:
            return False
        if recipeDTO.steps[-1].resultIngredient.id == recipeDTO.id:
            return True
        return False
    
    def has_ingredients(self, recipe_object):
        """Determines if at least one step has ingredients"""
        recipeDTO = self.get_by_id(recipe_object.id)
        for step in recipeDTO.steps:
            if step.sources:
                return True
        return False
    
    def delete(self, id):
        recipe = Recipe.get_one("id", id)
        if recipe.id:
            recipe.delete()
        else:
            raise ValueError(f"No existe receta con ID {id}")
    
    def get_all_completed(self):
        """Return all completed ingredients to be used for calculating their basic ingredients. * * * Without STEP depth  * * * """
        return [recipe for recipe in self.get_ingredient_all() if self.is_complete(recipe) and not self.is_basic(recipe)]
    
    def is_basic(self, recipe_object):
        """Determines if the ingredient is basic."""
        return not self.has_ingredients(recipe_object) and self.is_complete(recipe_object)
    
    def basic_ingredients(self, recipe_object):
        """Returns the quantities of all basic ingredients that make up a recipe"""
        basic_ingredients = defaultdict(lambda: defaultdict(float))
        for step in recipe_object.steps:
            for source in step.sources:
                if self.is_basic(source.ingredient):
                    basic_ingredients[source.ingredient.id][source.unit.id] += source.quantity
                else:
                    basic_dictionary = self.basic_ingredients(source.ingredient)
                    for ingredient_id, unit_quantity in basic_dictionary.items():
                        for unit_id, quantity in unit_quantity.items():
                            basic_ingredients[ingredient_id][unit_id] += quantity
        return {ing: dict(units) for ing, units in basic_ingredients.items()}
    
    