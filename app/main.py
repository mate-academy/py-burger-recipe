from __future__ import annotations
from typing import Any, Union
from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner: Any, name: Any) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Any, owner: Any) -> Union[int, str]:
        value = getattr(instance, self.protected_name)
        return value

    def __set__(self, instance: Any, value: Any) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: Union[int, str]) -> None:
        pass


class Number(Validator):

    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if value < self.min_value or value > self.max_value:
            raise ValueError(
                f"Quantity should not be less than {self.min_value} "
                f"and greater than {self.max_value}."
            )


class OneOf(Validator):

    def __init__(self, *options: str) -> None:
        self.options = tuple(options)

    def validate(self, value: str) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns = Number(min_value=2, max_value=3)
    cheese = Number(min_value=0, max_value=2)
    tomatoes = Number(min_value=0, max_value=3)
    cutlets = Number(min_value=1, max_value=3)
    eggs = Number(min_value=0, max_value=2)
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
