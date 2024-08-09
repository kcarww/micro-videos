from abc import ABC, abstractmethod
import contextlib
from dataclasses import dataclass
from typing import Any, Dict, Generic, List, TypeVar
from rest_framework.serializers import Serializer
from rest_framework.fields import CharField, BooleanField
from django.conf import settings
from __seedwork.domain.exceptions import ValidationException

if not settings.configured:
    settings.configure(USE_I18N=False)


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


# pylint: disable=too-few-public-methods
class DRFValidator(ValidatorFieldsInterface[PropsValidated], ABC):
    def validate(self, data: Serializer) -> bool:
        serializer = data
        is_valid = serializer.is_valid()
        if not is_valid:
            self.errors = {
                field: [str(_error) for _error in _errors]
                for field, _errors in serializer.errors.items()
            }
            return False

        self.validated_data = dict(serializer.validated_data)
        return True


class StrictCharField(CharField):
    def to_internal_value(self, data):
        if not isinstance(data, str):
            self.fail('invalid')
        return super().to_internal_value(data)


class StrictBooleanField(BooleanField):
    def to_internal_value(self, data):
        with contextlib.suppress(TypeError):
            if data is True or data is False:
                return data
            if data is None and self.allow_null:
                return None

        self.fail('invalid', input=data)
