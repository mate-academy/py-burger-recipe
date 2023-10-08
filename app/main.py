from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List, Union


class Validator(ABC):
    def __set_name__(self, owner: BurgerRecipe, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(
            self,
            instance: BurgerRecipe,
            owner: BurgerRecipe
    ) -> Union[int, str]:
        return getattr(instance, self.protected_name)

    def __set__(
            self,
            instance: BurgerRecipe,
            value: Union[int, str]
    ) -> None:
        setattr(instance, self.protected_name, self.validate(value))

    @abstractmethod
    def validate(self, value: Union[int, str]) -> Union[int, str]:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> int:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")

        if not (self.min_value <= value <= self.max_value):
            raise (
                ValueError(
                    f"Quantity should be not less than "
                    f"{self.min_value} and more than "
                    f"{self.max_value}."
                )
            )

        return value


class OneOf(Validator):
    def __init__(self, options: List[str]) -> None:
        self.options = options

    def validate(self, value: str) -> str:
        if value not in self.options:
            raise (
                ValueError(
                    f"Expected {value} to be one of "
                    f"{tuple(self.options)}."
                )
            )
        return value


class BurgerRecipe:
    buns: int = Number(2, 3)
    cheese: int = Number(0, 2)
    tomatoes: int = Number(0, 3)
    cutlets: int = Number(1, 3)
    eggs: int = Number(0, 2)
    sauce: str = OneOf(["ketchup", "mayo", "burger"])

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
