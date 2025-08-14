class UnitDTO:
    def __init__(self, name=None, short_name=None, id=None):
        self.id = id
        self.name = name
        self.short_name = short_name

    @classmethod
    def from_model(cls, unit_model):
        """Converts a Unit model to a DTO"""
        return UnitDTO( unit_model.name, unit_model.short_name, unit_model.id)

    def to_model(self, UnitModelClass):
        """Converts this DTO to a Unit Model ready to persist"""
        return UnitModelClass(self.name, self.short_name, self.id)