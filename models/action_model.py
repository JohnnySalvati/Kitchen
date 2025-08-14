from models.persistent_model import PersistentModel

class Action(PersistentModel):
    table_name = "action"
    table_fields = ["name"]

    def __init__(self, name, id=None):
        super().__init__(id)
        self.name = name
