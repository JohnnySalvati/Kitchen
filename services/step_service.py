from models.step_model import Step
from dto.step_dto import StepDTO

class StepService:
    def get_by_id(self, id):
        step = Step.get_one("id", id)
        return StepDTO.from_model(step)
    
    def get_all(self, recipe_id):
        steps = Step.get_all("recipe_id", recipe_id) 
        return [StepDTO.from_model(step) for step in steps]
        
    def delete(self, id):
        step = Step.get_one("id", id)
        if step.id:
            step.delete()

    def save(self, stepDTO):
        step = StepDTO.to_model(stepDTO)
        return step.save()
