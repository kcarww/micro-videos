from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from core.__seedwork.domain.validators import ErrorsFields


class InvalidUuidException(Exception):
    def __init__(self, error: str = "Invalid UUID"):
        super().__init__(error)


class ValidationException(Exception):
    pass


class EntityValidationException(Exception):
    error: 'ErrorsFields'

    def __init__(self, error: 'ErrorsFields') -> None:
        self.error = error
        super().__init__('Entity validation error')


class LoadEntityException(Exception):
    error: 'ErrorsFields'

    def __init__(self, error: 'ErrorsFields') -> None:
        self.error = error
        super().__init__('Load entity error')

class NotFoundException(Exception):
    pass
