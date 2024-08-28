from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, List, TypeVar

from __seedwork.domain.entities import Entity
from __seedwork.domain.exceptions import NotFoundException
from __seedwork.domain.value_objects import UniqueEntityId

ET = TypeVar('ET', bound=Entity)


@dataclass(slots=True)
class RepositoryInterface(Generic[ET], ABC):

    @abstractmethod
    def insert(self, entity: ET) -> None:
        raise NotImplementedError()

    @abstractmethod
    def find_by_id(self, entity_id: str | UniqueEntityId) -> ET:
        raise NotImplementedError()
        
    @abstractmethod
    def find_all(self) -> List[ET]:
        raise NotImplementedError()

    @abstractmethod
    def update(self, entity: ET) -> None:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, entity_id: str | UniqueEntityId) -> None:
        raise NotImplementedError()


class InMemoryRepository(ABC, RepositoryInterface[ET]):
    items: List[ET] = []
    
    def insert(self, entity: ET) -> None:
        self.items.append(entity)

    def find_by_id(self, entity_id: str | UniqueEntityId) -> ET:
        id_str = str(entity_id)
        return self._get(id_str)
    
    def find_all(self) -> List[ET]:
        return self.items

    def update(self, entity: ET) -> None:
        entity_found = self._get(entity.id)
        index = self.items.index(entity_found)
        self.items[index] = entity

    def delete(self, entity_id: str | UniqueEntityId) -> None:
        id_str = str(entity_id)
        entity_found = self._get(id_str)
        self.items.remove(entity_found)
    
    def _get(self, entity_id: str ):
        id_str = str(entity_id)
        entity = next(filter(lambda x: x.id == id_str, self.items), None)
        if not entity:
            raise NotFoundException(f"Entity not using ID '{entity_id}'")
        return entity
