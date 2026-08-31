from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner: str, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: "Validator", owner: str) -> None:
        if hasattr(instance, self.protected_name):
            return getattr(instance, self.protected_name)

    def __set__(self, instance: "Validator", value: int) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int | tuple) -> None:
        pass


class Number(Validator):
    def __init__(self , min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        elif value not in range(self.min_value, self.max_value + 1):
            raise ValueError(f"Quantity should not be less than "
                             f"{self.min_value} and greater than "
                             f"{self.max_value}.")


class OneOf(Validator):
    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value: str) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")
