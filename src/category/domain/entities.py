from datetime import datetime
from dataclasses import dataclass, field
from typing import Optional
from __seedwork.domain.entities import Entity
from category.domain.validators import CategoryValidatorFactory


@dataclass(kw_only=True, frozen=True, slots=True)
class Category(Entity):
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = True
    created_at: Optional[datetime] = field(default_factory=datetime.now)

    def __new__(cls, **kwargs):
        cls.validate(name=kwargs.get('name'),
                     description=kwargs.get('description'),
                     is_active=kwargs.get('is_active'),
                     created_at=kwargs.get('created_at'))
        return super(Category, cls).__new__(cls)

    def __post_init__(self):
        if not self.created_at:
            self._set('created_at', datetime.now())

    def update(self, name: str, description: str = None):
        self.validate(name, description)
        self._set('name', name)
        self._set('description', description)

    def activate(self):
        self._set('is_active', True)

    def deactivate(self):
        self._set('is_active', False)

    @classmethod
    def validate(cls, name: str, description: str,
                 is_active: bool = None, created_at: datetime = None):
        validator = CategoryValidatorFactory.create()
        validator.validate({
            'name': name,
            'description': description,
            'is_active': is_active,
            'created_at': created_at

        })
