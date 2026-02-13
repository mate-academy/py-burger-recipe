from abc import ABC, abstractmethod
from typing import Tuple, Type, Optional


class Validator(ABC):
    def __set_name__(self, owner: Type, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Optional[object], owner: Type) -> object:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: object) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: object) -> None:
        raise NotImplementedError("Subclasses must implement validate()")


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")

        if value < self.min_value or value > self.max_value:
            raise ValueError(
                f"Quantity should not be less than "
                f"{self.min_value} and greater than {self.max_value}."
            )


class OneOf:
    def __init__(self, options: Tuple) -> None:
        self.options = options

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Optional[object], owner: Type) -> object:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: str) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    def validate(self, value: str) -> None:
        if value not in self.options:
            raise ValueError(
                "Expected mustard to be one of ('ketchup', 'mayo', 'burger')."
            )


class BurgerRecipe:
    buns = Number(min_value=2, max_value=3)
    cheese = Number(min_value=0, max_value=2)
    tomatoes = Number(min_value=0, max_value=3)
    cutlets = Number(min_value=1, max_value=3)
    eggs = Number(min_value=0, max_value=2)
    sauce = OneOf(options=("ketchup", "mayo", "burger"))

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
