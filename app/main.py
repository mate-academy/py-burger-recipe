from __future__ import annotations
from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner: object, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: BurgerRecipe, owner: object) -> int | str:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: BurgerRecipe, value: int | str) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int | str) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.max_value = max_value
        self.min_value = min_value

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        elif not (self.min_value <= value <= self.max_value):
            raise ValueError("Quantity should not be "
                             f"less than {self.min_value} "
                             f"and greater than {self.max_value}.")


class OneOf(Validator):
    def __init__(self, *options) -> None:
        self.options = options

    def validate(self, value: str) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf("ketchup", "mayo", "burger")

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
