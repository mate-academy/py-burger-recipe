from abc import ABC, abstractmethod
from typing import Union, List


class Validator(ABC):

    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: type) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: Union[List, int]) -> None:
        validated_value = self.validate(instance, value)
        setattr(instance, self.protected_name, validated_value)

    @abstractmethod
    def validate(self, instance: object, value: Union[List, int]) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, instance: object, value: int) -> int:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        elif not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"Quantity should not be less than {self.min_value} "
                f"and greater than {self.max_value}"
            )
        return value


class OneOf(Validator):
    def __init__(self, options: list) -> None:
        self.options = options

    def validate(self, instance: object, value: str) -> str:
        if value not in self.options:
            raise ValueError(
                f"Expected {value} to be one of "
                f"{tuple(self.options)}."
            )
        return value


class BurgerRecipe:
    buns = Number(min_value=2, max_value=3)
    cheese = Number(min_value=0, max_value=2)
    tomatoes = Number(min_value=0, max_value=3)
    cutlets = Number(min_value=1, max_value=3)
    eggs = Number(min_value=0, max_value=2)
    sauce = OneOf(options=["ketchup", "mayo", "burger"])

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
