from abc import ABC, abstractmethod
from typing import Any, Type


class Validator(ABC):
    def __set_name__(self, owner: Type[Any], name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, instance: Any, owner: Type[Any]) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: Any) -> None:
        self.validate(instance, value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, instance: Any, value: Any) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, instance: Any, value: Any) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                "Quantity should not be less than {} and greater than {}.".
                format(self.min_value, self.max_value)
            )


class OneOf(Validator):
    def __init__(self, options: list[str]) -> None:
        self.options = options

    def validate(self, instance: Any, value: Any) -> None:
        if value not in self.options:
            raise ValueError(
                f"Expected {value} to be one of {tuple(self.options)}.")


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(["ketchup", "mayo", "burger"])

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
