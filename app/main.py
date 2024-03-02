from abc import ABC, abstractmethod
from typing import Type, Any


class Validator(ABC):
    def __set_name__(self, owner: Type, name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, instance: Any, owner: Type) -> int | str:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: Any) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: Any) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.max_value = max_value
        self.min_value = min_value

    def validate(self, value: Any) -> Any:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")

        if not (self.min_value <= value <= self.max_value):
            raise ValueError(f"Quantity should not be less than"
                             f" {self.min_value} and greater than"
                             f" {self.max_value}.")


class OneOf(Validator):
    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value: Any) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:

    sauce = OneOf(("ketchup", "mayo", "burger"))
    eggs = Number(0, 2)
    cutlets = Number(1, 3)
    tomatoes = Number(0, 3)
    cheese = Number(0, 2)
    buns = Number(2, 3)

    def __init__(
            self, buns: int, cheese: int, tomatoes: int,
            cutlets: int, eggs: int, sauce: str) -> None:
        self.sauce = sauce
        self.eggs = eggs
        self.cutlets = cutlets
        self.tomatoes = tomatoes
        self.cheese = cheese
        self.buns = buns
