from models.recipe_model import Recipe
from models.step_model import Step
from dto.recipe_dto import RecipeDTO
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
        steps = Step.get_all("recipe_id", id)
        recipeDTO = RecipeDTO.from_model(recipe, steps)
        return recipeDTO
    
    def get_all(self):
        recipesDTO = []
        recipes = Recipe.get_all()
        for recipe in recipes:
            steps = Step.get_all("recipe_id", recipe.id)
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
        if isinstance(recipe_object,RecipeDTO):
            recipeDTO = recipe_object
        elif isinstance(recipe_object, Recipe):
            recipeDTO = RecipeDTO.from_model(recipe_object)
        if not recipeDTO.name or not recipeDTO.steps:
            return False
        if recipeDTO.steps[-1].resultIngredient.id == recipeDTO.id:
            return True
        return False
    
    def has_ingredients(self, recipe_object):
        """Determines if at least one step has ingredients"""
        if isinstance(recipe_object,RecipeDTO):
            recipeDTO = recipe_object
        elif isinstance(recipe_object, Recipe):
            recipeDTO = RecipeDTO.from_model(recipe_object)
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
    