from models.source_model import Source
from dto.source_dto import SourceDTO

class SourceService:
    def get_by_id(self, id):
        source = Source.get_one("id", id)
        if not source.id:
            raise ValueError(f"No exite ingrediente original con ID {id}")
        return SourceDTO.from_model(source)
    
    def get_all(self, recipe_id):
        sources = Source.get_all("recipe_id", recipe_id)
        try:
            sourcesDTO = [SourceDTO.from_model(source) for source in sources]
        except RecursionError as e:
            raise RecursionError(f"Se produjo una recursionita {e}")
        return sourcesDTO
    
    def get_by_ingredient_id(self, id: int) -> list[SourceDTO]:
        sources = Source.get_all("ingredient_id", id)
        return sources
    
    def delete(self, id):
        source = Source.get_one("id", id)
        if source.id:
            source.delete()
        else:
            raise ValueError(f"No exite ingrediente original con ID {id}")

    def save(self, sourceDTO: SourceDTO):
        if not sourceDTO.ingredient.id:
            raise ValueError(sourceDTO)
        elif sourceDTO.quantity == 0:
            raise ValueError(sourceDTO)
        elif not sourceDTO.unit:
            raise ValueError(SourceDTO)
        else:
            source = SourceDTO.to_model(sourceDTO)
        return source.save()

    def update_sources(self, recipe_id, sourcesDTO: list[SourceDTO]):
        """Checks if source need to be deleted, updated, or left as is"""
        sources = Source.get_all("recipe_id", recipe_id)
        for source in sources:
            index = self.find_source_index(sourcesDTO, source.id)
            if index >= 0:
                if SourceDTO.to_model(sourcesDTO[index]) != source:
                    self.save(sourcesDTO[index])
            else:
                source.delete()
        for sourceDTO in sourcesDTO:
            index = self.find_source_index(sources, sourceDTO.id)
            if index < 0:
                self.save(sourceDTO)
        
    def find_source_index(self, sources: list[SourceDTO], source_id):
        for index, source in enumerate(sources):
            if source.id == source_id:
                return index
        return -1        
    
    def are_equals(self, sourcesDTO_a: list[SourceDTO], sourcesDTO_b: list[SourceDTO]) -> bool:
        return list(sourcesDTO_a) == list(sourcesDTO_b)