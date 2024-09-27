from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from category.domain.entities import Category
from category.domain.repositories import CategoryRepository

@dataclass(slots=True, frozen=True)
class CreateCategoryUseCase:
    
    category_repo: CategoryRepository
    
    def execute(self, input_param: 'Input') -> 'Output':
        category = Category(name=input_param.name,
                            description=input_param.description,
                            is_active=input_param.is_active)
        self.category_repo.insert(category)
        return self.Output(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
            created_at=category.created_at
        )
    
    @dataclass(slots=True, frozen=True)
    class Input:
        name: str
        description: Optional[str] = None
        is_active: Optional[bool] = True
        
    @dataclass(slots=True, frozen=True)
    class Output:
        id: str
        name: str
        description: Optional[str]
        is_active: bool
        created_at: datetime