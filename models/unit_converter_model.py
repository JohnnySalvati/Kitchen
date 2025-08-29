from models.persistent_model import PersistentModel

class UnitConverter(PersistentModel):
    table_name = "unit_converter"
    table_fields = [
        "source_unit_id",
        "quantity",
        "target_unit_id"]

    def __init__(self, source_unit_id, quantity, target_unit_id, id=None):
        super().__init__(id)
        self.source_unit_id = source_unit_id
        self.quantity = quantity
        self. target_unit_id = target_unit_id
