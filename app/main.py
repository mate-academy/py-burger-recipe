from __future__ import annotations

from abc import abstractmethod
from typing import Any, Type


class Validator:
    def __set_name__(self, cls: Type[Any], name: str) -> None:
        self._protected_name = f"_{name}"
        self._public_name = name

    def __get__(self, obj: Type[Any] | None, cls: Type[Any]) -> int | str:
        if obj is None:
            return self

        if self._protected_name not in obj.__dict__:
            raise AttributeError(f"Attribute {self._public_name} isn't set.")

        return obj.__dict__[self._protected_name]

    def __set__(self, obj: Any, value: Any) -> None:
        self.validate(value)
        obj.__dict__[self._protected_name] = value

    @abstractmethod
    def validate(self, value: str | int) -> bool | None:
        pass


class Number(Validator):
    def __init__(self, minvalue: int, maxvalue: int) -> None:
        self._min_value = minvalue
        self._max_value = maxvalue

    def validate(self, value: str | int) -> bool | None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self._min_value <= value <= self._max_value):
            minvalue = self._min_value
            maxvalue = self._max_value
            raise ValueError(f"Quantity should not be less than {minvalue} "
                             f"and greater than {maxvalue}.")


class OneOf(Validator):
    def __init__(self, *options: tuple) -> None:
        self._options = options

    def validate(self, value: str | int) -> bool | None:
        if not (isinstance(value, str) and value in self._options):
            raise ValueError(f"Expected {value} to be one of {self._options}.")


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
