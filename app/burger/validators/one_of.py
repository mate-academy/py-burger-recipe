from app.burger.validators.validator import Validator


class OneOf(Validator):
    def __init__(self, options: tuple[str]) -> None:
        self.options = options

    def validate(self, value) -> None:
        if not isinstance(value, str):
            raise TypeError('sauce should be string')
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")