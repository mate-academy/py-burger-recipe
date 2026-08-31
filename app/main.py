from abc import ABC, abstractmethod
from typing import Any


class Validator(ABC):
    def __set_name__(self, owner: Any, name: str) -> Any:
        self.protected_name = "_" + name

    def __get__(self, instance: Any, owner: Any) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: int) -> Any:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: Any) -> Any:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> Any:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> Any:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(f"Quantity should not be less than"
                             f" {self.min_value} and greater"
                             f" than {self.max_value}.")


class OneOf(Validator):
    def __init__(self, *options: Any) -> Any:
        self.options = options

    def validate(self, value: int) -> Any:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf("ketchup", "mayo", "burger")

    def __init__(self, buns: Any, cheese: Any,
                 tomatoes: Any, cutlets: Any,
                 eggs: Any, sauce: Any
                 ) -> Any:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
