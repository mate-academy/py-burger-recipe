from typing import Any
from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, instance: Any, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Any, owner: Any = None) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: Any) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: Any) -> None:
        pass


class Number(Validator):
    def __init__(self, min_num: int, max_num: int) -> None:
        self.min_value = min_num
        self.max_value = max_num

    def validate(self, ordered_quantity: Any) -> None:
        if not isinstance(ordered_quantity, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= ordered_quantity <= self.max_value):
            raise ValueError(f"Quantity should not be less than "
                             f"{self.min_value} and greater than "
                             f"{self.max_value}")


class OneOf(Validator):
    def __init__(self, sauce_list: tuple = None) -> None:
        self.options = sauce_list or ("ketchup", "mayo", "burger")

    def validate(self, ordered_sauce: str) -> None:
        if ordered_sauce not in self.options:
            raise ValueError(f"Expected {ordered_sauce} "
                             f"to be one of {self.options}.")


class BurgerRecipe:
    sauce = OneOf()
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)

    def __init__(self,
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
