from dataclasses import dataclass, field
from __seedwork.domain.exceptions import InvalidUuidException
import uuid
@dataclass(frozen=True)
class UniqueEntityId:
    id: str = field(default_factory=uuid.uuid4)
    
    def __post_init__(self):
        id_value = str(self.id) if isinstance(self.id, uuid.UUID) else self.id
        object.__setattr__(self, 'id', id_value)
        self.__validate()
        
    def __validate(self):
        try:
            uuid.UUID(self.id)
        except ValueError as ex:
            raise InvalidUuidException() from ex 
        
    def __str__(self):
        return f"{self.id}"