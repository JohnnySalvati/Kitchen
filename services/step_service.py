from models.step_model import Step

class StepService:
    def get_by_id(self, id):
        return Step.get_one("id", id)
    
    def get_all(self):
        return Step.get_all()