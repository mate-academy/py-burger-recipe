from __future__ import annotations
from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner: BurgerRecipe, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, obj: BurgerRecipe, objtype: BurgerRecipe = None) -> str:
        return getattr(obj, self.protected_name)

    def __set__(self, obj: BurgerRecipe, value: int | str) -> None:
        setattr(obj, self.protected_name, self.validate(value))

    @abstractmethod
    def validate(self, value: int | str) -> None:
        pass


class Number(Validator):

    def __init__(self, min_value: int, max_value: int) -> None:
        self.max_value = max_value
        self.min_value = min_value

    def validate(self, value: int) -> int:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        elif value < self.min_value or value > self.max_value:
            raise ValueError(
                f"Quantity should not be "
                f"less than {self.min_value} "
                f"and greater than {self.max_value}."
            )
        else:
            return value


class OneOf(Validator):

    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value: str) -> str:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")
        return value


class BurgerRecipe:

    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(("ketchup", "mayo", "burger"))

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
