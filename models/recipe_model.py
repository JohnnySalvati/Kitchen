from models.persistent_model import PersistentModel
from models.step_model import Step

class Recipe(PersistentModel):
    def __init__(self, name: str="", price: float=0, steps: list[Step]=[], id=None):
        super().__init__(id)
        self.name = name
        self.price = price
        self.steps = [] if steps is None else steps

    table_name = "recipe"
    table_fields = ["name", "price"]

    @classmethod
    def get_one(cls, field=None, value=None):  
        """
        Returns a recipe that match the condition or None
        """
        recipe = super().get_one(field, value)
        if recipe:
            recipe.steps = Step.get_all("recipe_id", recipe.id)
        return recipe

    @classmethod
    def get_all(cls, field=None, value=None):
        """
        Returns a list of Recipes that match the condition 
        """
        recipes = super().get_all(field, value)
        for recipe in recipes:
            recipe.steps = Step.get_all("recipe_id", recipe.id)
        return recipes

    @classmethod
    def get_ingredient(cls, id): 
        """
        Return a recipe to be used by other classes that don't need steps to avoid recursivity
        """
        return super().get_one("id", id)

    @classmethod
    def get_ingredients(cls):
        """
        Return a list of recipes to be used by other classes that don't need steps to avoid recursivity
        """
        return super().get_all()

    def save(self):
        super().save() # stores Recipe
        # stores Steps
        for step in self.steps:
            step.save()
        return self

    def delete(self):
        # delete Steps
        for step in self.steps:
            self.delete_step(step)
        super().delete() # delete Recipe

    def add_step(self, step):
        self.steps.append(step)
        step.save()
    
    def delete_step(self, step):
        self.steps = [s for s in self.steps if s.id != step.id]
        step.delete()

    def is_complete(self):
        """Determines if Recipe is complete, to be used like ingredient"""
        if not self.name or not self.steps:
            return False
        if self.steps[-1].resultIngredient_id == self.id:
            return True
        return False

    def has_ingredients(self): 
        """Determines if at least one step has ingredients"""
        for step in self.steps:
            if step.sources:
                return True
        return False