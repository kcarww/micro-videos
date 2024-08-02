from dataclasses import dataclass, field
from __seedwork.domain.exceptions import InvalidUuidException
import uuid
@dataclass()
class UniqueEntityId:
    id: str = field(default_factory=uuid.uuid4)
    
    def __post_init__(self):
        self.id = str(self.id) if isinstance(self.id, uuid.UUID) else self.id
        self.__validate()
    def __validate(self):
        try:
            uuid.UUID(self.id)
        except ValueError as ex:
            raise InvalidUuidException() from ex 