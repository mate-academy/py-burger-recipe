from __future__ import annotations
from typing import Any
from abc import ABC, abstractmethod


class Validator(ABC):
    @abstractmethod
    def validate(self, value: Any) -> bool:
        return True

    def __set_name__(self, owner: str, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Validator, owner: str) -> Any:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Validator, value: Any) -> None:
        if self.validate(value):
            setattr(instance, self.protected_name, value)


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any) -> bool:
        if isinstance(value, int):
            if value in range(self.min_value, self.max_value + 1):
                return True
            error_text1 = f"Quantity should not be less than {self.min_value} "
            error_text2 = f"and greater than {self.max_value}."
            raise ValueError(error_text1 + error_text2)

        raise TypeError("Quantity should be integer.")


class OneOf(Validator):
    def __init__(
        self,
        options: tuple = ("ketchup", "mayo", "burger")
    ) -> None:
        self.options = tuple(options)

    def validate(self, value: Any) -> bool:
        if value in self.options:
            return True

        raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf()

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
