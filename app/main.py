from __future__ import annotations
from typing import Union
from abc import ABC, abstractmethod


class Validator(ABC):
    def __init__(self) -> None:
        self.protected_name = None

    def __set_name__(self, owner: BurgerRecipe, name: str) -> None:
        self.protected = "_" + name

    def __get__(self,
                instance: BurgerRecipe,
                owner: BurgerRecipe
                ) -> Union[str, int]:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: BurgerRecipe, value: Union[str, int]) -> None:
        if self.protected_name == "_sauce":
            self.validate(value)
        else:
            self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: Union[int, str]) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value

    def __set_name__(self, owner: Number, name: str) -> None:
        self.protected_name = "_" + name

    def validate(self, value: Union[int, str]) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not self.min_value <= value < self.max_value:
            raise ValueError(
                f"Quantity should not be less than {self.min_value}"
                f" and greater than {self.max_value}."
            )


class OneOf(Validator):
    def __init__(self, options: tuple) -> None:
        super().__init__()
        self.options = options

    def __set_name__(self, owner: OneOf, name: str) -> None:
        self.protected_name = "_" + name

    def validate(self, value: str) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    cheese = Number(0, 3)
    tomatoes = Number(0, 4)
    cutlets = Number(1, 4)
    eggs = Number(0, 3)
    buns = Number(2, 4)
    sauce = OneOf(("ketchup", "mayo", "burger"))

    def __init__(self,
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
