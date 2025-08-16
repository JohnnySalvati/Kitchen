from models.persistent_model import PersistentModel

class Step(PersistentModel):
    def __init__(self, recipe_id, sources= None, action_id=None, action=None, resultIngredient_id=None, resultIngredient=None, resultUnit_id=None, resultUnit=None, resultQuantity=None, id=None):
        super().__init__(id)
        self.recipe_id = recipe_id
        self.sources = sources if sources else []
        self.action_id = action_id
        self._action = None
        self.action = action
        self.resultIngredient_id = resultIngredient_id
        self._resultIngredient = None
        self.resultIngredient = resultIngredient
        self.resultUnit_id = resultUnit_id
        self._resultUnit = None
        self.resultUnit = resultUnit
        self.resultQuantity = resultQuantity

    table_name = "step"
    table_fields = ["recipe_id",
                    "action_id",
                    "resultIngredient_id",
                    "resultUnit_id",
                    "resultQuantity"]
    
    @classmethod
    def get_one(cls, field=None, value=None):
        from models.source_model import Source

        step = super().get_one(field, value)
        if step:
            step.sources = Source.get_all("step_id", step.id)
        return step

    @classmethod
    def get_all(cls, field=None, value=None):
        from models.source_model import Source

        steps = super().get_all(field, value)
        for step in steps:
            step.sources = Source.get_all("step_id", step.id)
        return steps

    @property
    def action(self):
        return self._action

    @action.setter
    def action(self, value):
        from models.action_model import Action

        if value:
            self._action = value
            self.action_id = value.id
        else:
            if self.action_id:
                self._action = Action.get_one("id", self.action_id)
            else:
                self._action = None

    @property
    def resultIngredient(self):
        return self._resultIngredient
    
    @resultIngredient.setter
    def resultIngredient(self, value):
        from models.recipe_model import Recipe

        if value:
            self._resultIngredient = value
            self.resultIngredient_id = value.id if value else None
        else:
            if self.resultIngredient_id:
                self._resultIngredient =  Recipe.get_ingredient(self.resultIngredient_id)
            else:
                self._resultIngredient = None

    @property
    def resultUnit(self):
        return self._resultUnit
    
    @resultUnit.setter
    def resultUnit(self, value):
        from models.unit_model import Unit

        if value:
            self._resultUnit = value
            self.resultUnit_id = value.id if value else None
        else:
            if self.resultUnit_id:
                self._resultUnit = Unit.get_one("id", self.resultUnit_id)
            else:
                self._resultUnit = None

    def save(self):
        from models.source_model import Source
        super().save() # almacena el Step
        # almacena los Sources
        # borramos todos los sources anteriores por consistencia con eliminados en memoria, se grabaran nuevamente los que estan en memoria
        for source in Source.get_all("step_id", self.id):
            source.delete()
        for source in self.sources:
            if not source.step_id:
                source.step_id = self.id
            source.id = None # borramos el id para que lo vuelva a crear
            source.save()

    def delete(self):
        super().delete() #delete the step

    def delete_source(self, source):
        self.sources = [s for s in self.sources if s.id != source.id]

    def __str__(self):
        action = self.action.name if self.action else None
        ingredient = self.resultIngredient.name if self.resultIngredient else None
        unit = self.resultUnit.name if self.resultUnit else None
        return f"Id: {self.id or ''} Accion: {action} -> Ingredient: {ingredient} Unit: {unit} Cantidad: {self.resultQuantity or 0}"