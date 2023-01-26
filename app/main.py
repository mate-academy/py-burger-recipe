from __future__ import annotations
from abc import ABC, abstractmethod


class Validator(ABC):

    def __set_name__(self, owner: BurgerRecipe, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(
            self,
            instance: BurgerRecipe,
            owner: BurgerRecipe
    ) -> int | str:
        return getattr(instance, self.protected_name)

    def __set__(
            self,
            instance:
            BurgerRecipe,
            value: int | str
    ) -> int | str | None:
        self.validate(value)
        return setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int | str) -> None:
        pass


class Number(Validator):

    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:

        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(f"Quantity should "
                             f"not be less than {self.min_value}"
                             f" and greater than {self.max_value}.")
        return


class OneOf(Validator):

    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value: str) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} "
                             f"to be one of {self.options}.")
        return


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
