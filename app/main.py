from abc import ABC, abstractmethod
from typing import Any, Tuple


class Validator(ABC):
    @abstractmethod
    def validate(self, value: Any) -> None:
        pass

    def __set_name__(self, owner: Any, name: str) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, instance: Any, owner: Any) -> str | int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: Any) -> None:
        if self.validate(value):
            setattr(instance, self.protected_name, value)


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any) -> bool:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        elif self.min_value > value or self.max_value < value:
            raise ValueError("Quantity should not be less than "
                             f"{self.min_value} and greater than "
                             f"{self.max_value}.")
        return True


class OneOf(Validator):
    def __init__(self, options: Tuple) -> None:
        self.options = options

    def validate(self, value: Any) -> bool:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")
        return True


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(("ketchup", "mayo", "burger"))

    def __init__(self,
                 buns: int,
                 cheese: int,
                 tomatoes: int,
                 cutlets: int,
                 eggs: int,
                 sauce: str) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
