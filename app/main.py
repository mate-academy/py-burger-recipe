from abc import ABC, abstractmethod
from typing import Tuple


class Validator(ABC):
    def __set_name__(self, owner: str, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: int, owner: str) -> str:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: int, value: str) -> str:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: str) -> str:
        raise NotImplementedError("Subclasses must"
                                  " implement the validate method")


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> str:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if value < self.min_value or value > self.max_value:
            raise ValueError(f"Quantity should not be less than "
                             f"{self.min_value}"
                             f" and greater than {self.max_value}.")


class OneOf(Validator):
    def __init__(self, options: Tuple[str]) -> None:
        self.options = options

    def validate(self, value: str) -> str:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns: int = Number(min_value=2, max_value=3)
    cheese: int = Number(min_value=0, max_value=2)
    tomatoes: int = Number(min_value=0, max_value=3)
    cutlets: int = Number(min_value=1, max_value=3)
    eggs: int = Number(min_value=0, max_value=2)
    sauce: str = OneOf(options=("ketchup", "mayo", "burger"))

    def __init__(
            self,
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

    def __repr__(self) -> str:
        return f"Burger(buns={self.buns}, cheese={self.cheese}" \
               f", tomatoes={self.tomatoes}, cutlets={self.cutlets}" \
               f", eggs={self.eggs}, sauce='{self.sauce}')"
