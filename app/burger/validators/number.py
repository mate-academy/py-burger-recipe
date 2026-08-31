from app.burger.validators.validator import Validator


class Number(Validator):
    def __init__(self, min_value: int, max_value: int):
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError('Quantity should be integer.')
        if value < self.min_value or value > self.max_value:
            raise ValueError(f"Quantity should not be less than {self.min_value} and greater than {self.max_value}.")
