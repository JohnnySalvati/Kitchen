
class StepDTO:
    def __init__(self,
                    recipe_id=None,
                    sources= None,
                    action=None,
                    resultIngredient=None,
                    resultUnit=None,
                    resultQuantity=None,
                    id=None):
        self.id = id
        self.recipe_id = recipe_id
        self.sources = sources if sources else []
        self.action = action
        self.resultIngredient = resultIngredient
        self.resultUnit = resultUnit
        self.resultQuantity = resultQuantity

    @classmethod
    def from_model(cls, step_model):
        """Converts a Step model to a DTO"""
        return StepDTO(step_model.recipe_id,
                        step_model.sources,
                        step_model.action,
                        step_model.resultIngredient,
                        step_model.resultUnit,
                        step_model.resultQuantity,
                        step_model.id)

    def to_model(self, RecipeModelClass):
        """Converts this DTO to a Step Model ready to persist"""
        return RecipeModelClass(recipe_id = self.recipe_id,
                                sources = self.sources,
                                action = self.action,
                                resultIngredient = self.resultIngredient,
                                resultUnit = self.resultUnit,
                                resultQuantity = self.resultQuantity,
                                id = self.id)