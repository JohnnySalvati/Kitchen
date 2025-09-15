from models.persistent_model import PersistentModel

class Unit(PersistentModel):
    table_name = "unit"
    table_fields = ["name", "short_name"]

    def __init__(self, name="", short_name="", id=None):
        super().__init__(id)
        self.name = name
        self.short_name = short_name
