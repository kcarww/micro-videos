from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Generic, List, TypeVar
from rest_framework.serializers import Serializer
from __seedwork.domain.exceptions import ValidationException

@dataclass(frozen=True, slots=True)
class ValidatorRules:
    value: Any
    prop: str

    @staticmethod
    def values(value: Any, prop: str):
        return ValidatorRules(value, prop)

    def required(self) -> "ValidatorRules":
        if self.value is None or self.value == "":
            raise ValidationException(f'{self.prop} is required')
        return self

    def string(self) -> "ValidatorRules":
        if self.value is not None and not isinstance(self.value, str):
            raise ValidationException(f'{self.prop} must be a string')
        return self

    def max_length(self, length: int) -> "ValidatorRules":
        if self.value is not None and len(self.value) > length:
            raise ValidationException(
                f'{self.prop} must be at most {length} characters long')
        return self

    def boolean(self) -> "ValidatorRules":
        if self.value is not None and not isinstance(self.value, bool):
            raise ValidationException(f'{self.prop} must be a boolean')
        return self


ErrorsFields = Dict[str, List[str]]
PropsValidated = TypeVar('PropsValidated')


@dataclass(slots=True)
class ValidatorFieldsInterface(ABC, Generic[PropsValidated]):
    errors: ErrorsFields = None
    validated_data: Any = None

    @abstractmethod
    def validate(self, data: Any) -> bool:
        raise NotImplementedError()


class DRFValidator(ValidatorFieldsInterface[PropsValidated]):
    def validate(self, serializer: Serializer):
        serializer.is_valid()