from abc import ABC, abstractmethod
from typing import Generic, List, TypeVar

from __seedwork.domain.value_objects import UniqueEntityId

ET = TypeVar('ET')

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