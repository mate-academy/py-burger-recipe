from app.Validator.validator import Validator


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        elif value < self.min_value or value > self.max_value:
            raise ValueError(f"Quantity should not be less than "
                             f"{self.min_value} and greater than "
                             f"{self.max_value}.")
