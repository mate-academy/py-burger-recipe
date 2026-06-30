from app.Validator.validator import Validator


class OneOf(Validator):
    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value: int) -> None:
        for _ in range(len(self.options)):
            if value not in self.options:
                raise ValueError(f"Expected {value} "
                                 f"to be one of {self.options}.")
