class InvalidUuidException(Exception):
    def __init__(self, error: str = "Invalid UUID"):
        super().__init__(error)


class ValidationException(Exception):
    pass
