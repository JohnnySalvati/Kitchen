from models.persistent_model import PersistentModel
from models.step_model import Step

class Recipe(PersistentModel):
    table_name = "recipe"
    table_fields = ["name", "price", "unit_id", "quantity"]

    def __init__(self, name: str="", price: float=0, unit_id: int = 0, quantity: float=0, id=None):
        super().__init__(id)
        self.name = name
        self.price = price
        self.unit_id = unit_id
        self.quantity = quantity
