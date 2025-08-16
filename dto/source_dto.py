class SourceDTO():
    def __init__(self,
                step_id=None,
                ingredient=None,
                unit=None,
                quantity=0,
                id=None):
        self.id = id
        self.step_id = step_id
        self.ingredient = ingredient
        self.unit = unit
        self.quantity = quantity

    @classmethod
    def from_model(cls, source_model):
        """Converts a Source model to a DTO"""
        return SourceDTO(source_model.step_id,
                        source_model.ingredient,
                        source_model.unit,
                        source_model.quantity, 
                        source_model.id)

    def to_model(self, SourceModelClass):
        """Converts this DTO to a Source Model ready to persist"""
        return SourceModelClass(step_id = self.step_id,
                                ingredient = self.ingredient,
                                unit = self.unit,
                                quantity = self.quantity,
                                id = self.id)