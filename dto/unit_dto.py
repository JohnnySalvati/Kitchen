class UnitDTO:
    def __init__(self, name=None, short_name=None, id=None):
        self.id = id
        self.name = name
        self.short_name = short_name

    @classmethod
    def from_model(cls, unit_model):
        """Converts a Unit model to a DTO"""
        return UnitDTO(unit_model.name,
                        unit_model.short_name,
                        unit_model.id)

    def to_model(self):
        """Converts this DTO to a Unit Model ready to persist"""
        from models.unit_model import Unit

        return Unit(name = self.name,
                            short_name = self.short_name,
                            id = self.id)