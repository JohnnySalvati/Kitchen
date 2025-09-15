from models.persistent_model import PersistentModel
class Recipe(PersistentModel):
    table_name = "recipe"
    table_fields = ["name", "price", "resultUnit_id", "resultQuantity"]

    def __init__(self, name: str="", price: float=0, resultUnit_id: int = 0, resultQuantity: float=0, id=None):
        super().__init__(id)
        self.name = name
        self.price = price
        self.resultUnit_id = resultUnit_id
        self.resultQuantity = resultQuantity
