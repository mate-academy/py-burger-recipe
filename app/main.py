from abc import ABC, abstractmethod
from typing import Iterable


class Validator(ABC):
    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name: str = "_" + name

    def __get__(self, instance: object | None, owner: type):
        if instance is None:
            return self
        return instance.__dict__.get(self.protected_name)

    def __set__(self, instance: object, value) -> None:
        self.validate(value)
        instance.__dict__[self.protected_name] = value

    @abstractmethod
    def validate(self, value) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value: int = min_value
        self.max_value: int = max_value

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"Quantity should not be less "
                f"than {self.min_value} and "
                f"greater than {self.max_value}"
            )


class OneOf(Validator):
    def __init__(self, options: Iterable[str]) -> None:
        self.options: Iterable[str] = options

    def validate(self, value: str) -> None:
        if value not in self.options:
            raise ValueError(
                f"Expected {value} to be one of {self.options}."
            )


class BurgerRecipe:
    buns: int = Number(2, 3)
    cheese: int = Number(0, 2)
    tomatoes: int = Number(0, 3)
    cutlets: int = Number(1, 3)
    eggs: int = Number(0, 2)
    sauce: str = OneOf(["ketchup", "mayo", "burger"])

    def __init__(
        self,
        buns: int,
        cheese: int,
        tomatoes: int,
        cutlets: int,
        eggs: int,
        sauce: str
    ) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
