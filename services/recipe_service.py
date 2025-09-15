from models.recipe_model import Recipe
from dto.recipe_dto import RecipeDTO
from collections import defaultdict
from services.source_service import SourceService
source_service = SourceService()
import sqlite3
class DatabaseError(Exception):
    pass
class RecipeService:

    def save(self, recipeDTO: RecipeDTO):
        if not recipeDTO.name or not recipeDTO.name.strip():
            raise ValueError("El nombre no puede estar vacio")
        if recipeDTO.price is None or recipeDTO.price < 0:
            raise ValueError("El precio no puede ser menor que 0")
        if recipeDTO.result_quantity <= 0:
            raise ValueError("La cantidad tiene que ser mayor que 0")
        if recipeDTO.result_unit.id == None:
            raise ValueError("Hay que especificar una unidad")
        recursion = self.has_recursion(recipeDTO)
        if recursion:
            raise DatabaseError(f"Recursión detectada: la receta {recipeDTO.name} se referencia a sí misma indirectamente en {recursion.name}")
        try:
            recipe = RecipeDTO.to_model(recipeDTO)
            recipe = recipe.save()
            recipeDTO.id = recipe.id
            for source in recipeDTO.sources: # if it's a new recipe, need to assign a recipe ID to sources
                source.recipe_id = recipe.id
            source_service.update_sources(recipe.id, recipeDTO.sources)
            sources = source_service.get_all(recipe.id)
            return RecipeDTO.from_model(recipe, sources)
        except sqlite3.IntegrityError:
            raise ValueError("Ya existe una receta con el mismo nombre")
        except Exception as e:
            raise RuntimeError(f"No se pudo crear la receta: {e}")

    def has_recursion(self, recipeDTO: RecipeDTO, primal: int | None = None) -> RecipeDTO | None:
        if not recipeDTO.id:
            return None
        if not primal:
            primal = recipeDTO.id
        for sourceDTO in recipeDTO.sources:
            source_ingredient = self.get_by_id(sourceDTO.ingredient.id)
            if primal == source_ingredient.id:
                return source_ingredient
            recursion = self.has_recursion(source_ingredient, primal)
            if recursion:
                return source_ingredient
        return None

    def get_by_id(self, id: int):
        try:
            recipe = Recipe.get_one("id", id)
            sources = source_service.get_all(id)
        except RecursionError as e:
            raise RecursionError(f"Se produjo una recursion infinita: {e}")
        recipeDTO = RecipeDTO.from_model(recipe, sources)
        return recipeDTO
    
    def get_all(self):
        recipesDTO = []
        recipes = Recipe.get_all()
        for recipe in recipes:
            sources = source_service.get_all(recipe.id)
            recipesDTO.append(RecipeDTO.from_model(recipe, sources))
        return recipesDTO
    
    def get_ingredient(self, id:int | None):
        recipe = Recipe.get_one("id", id)
        if not recipe.id:
            raise ValueError(f"No exite receta con ID {id}")
        recipeDTO = RecipeDTO.from_model(recipe, [])
        return recipeDTO

    def get_ingredient_all(self):
        recipes = Recipe.get_all()
        return [RecipeDTO.from_model(recipe, []) for recipe in recipes]
    
    def has_ingredients(self, recipe_object):
        """Determines if a recipe or recipeDTO has ingredients"""
        recipeDTO = self.get_by_id(recipe_object.id)
        if recipeDTO.sources:
            return True
        return False
    
    def delete(self, id:int):
        recipe = Recipe.get_one("id", id)
        sources = source_service.get_by_ingredient_id(id)
        if sources:
            raise DatabaseError(f"Este ingrediente esta siendo usado en {len(sources)} recetas")
        if recipe.id:
            recipe.delete()
        else:
            raise ValueError(f"No existe receta con ID {id}")
    
    def get_all_completed(self):
        """Return all completed ingredients to be used for calculating their basic ingredients. * * * Without STEP depth  * * * """
        return [recipe for recipe in self.get_ingredient_all() if self.has_ingredients(recipe)]
    
    def basic_ingredients(self, recipeDTO: RecipeDTO):
        """Returns the quantities of all basic ingredients that make up a recipe"""
        basic_ingredients = defaultdict(lambda: defaultdict(float))
        for source in recipeDTO.sources:
            if not self.has_ingredients(source.ingredient):
                basic_ingredients[source.ingredient.id][source.unit.id] += source.quantity
            else:
                basic_dictionary = self.basic_ingredients(source.ingredient)
                for ingredient_id, unit_quantity in basic_dictionary.items():
                    for unit_id, quantity in unit_quantity.items():
                        basic_ingredients[ingredient_id][unit_id] += quantity
        return {ing: dict(units) for ing, units in basic_ingredients.items()}
    
    def get_price(self, ingredient_id: int |None, unit_id: int |None, quantity:float):
        """Returns a price given ingredient id or obj, unit id or obj and quantity"""
        from services.unit_converter_service import UnitConverterService

        unit_converter_service = UnitConverterService()
        ingredient = self.get_ingredient(ingredient_id)
        if ingredient.result_unit.id == unit_id:
            final_quantity = quantity
        else:
            final_quantity = unit_converter_service.convert(quantity, unit_id, ingredient.result_unit.id)
        return ingredient.price / ingredient.result_quantity * final_quantity

        
    