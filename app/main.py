from __future__ import annotations

from abc import abstractmethod, ABC
from typing import Any, Type


class Validator(ABC):
    def __set_name__(self, cls: Type[Any], name: str) -> None:
        self.protected_name = f"_{name}"
        self.public_name = name

    def __get__(self, obj: Type[Any] | None, cls: Type[Any]) -> int | str:
        if obj is None:
            return self

        if self.protected_name not in obj.__dict__:
            raise AttributeError(f"Attribute {self.public_name} isn't set.")

        return obj.__dict__[self.protected_name]

    def __set__(self, obj: Any, value: Any) -> None:
        self.validate(value)
        obj.__dict__[self.protected_name] = value

    @abstractmethod
    def validate(self, value: str | int) -> bool | None:
        pass


class Number(Validator):
    def __init__(self, minvalue: int, maxvalue: int) -> None:
        self.min_value = minvalue
        self.max_value = maxvalue

    def validate(self, value: str | int) -> bool | None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            minvalue = self.min_value
            maxvalue = self.max_value
            raise ValueError(f"Quantity should not be less than {minvalue} "
                             f"and greater than {maxvalue}.")


class OneOf(Validator):
    def __init__(self, *options: tuple) -> None:
        self.options = options

    def validate(self, value: str | int) -> bool | None:
        if not (isinstance(value, str) and value in self.options):
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
            sauce: str,
    ) -> None:

        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
