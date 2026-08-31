from abc import ABC, abstractmethod
from typing import Any


class Validator(ABC):
    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, obj: object, objtype: type = None) -> object:
        return getattr(obj, self.protected_name)

    def __set__(self, obj: object, value: Any) -> None:
        setattr(obj, self.protected_name, value)
        self.validate(value)

    @abstractmethod
    def validate(self, value: Any) -> str:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> str:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if value not in range(self.min_value, self.max_value + 1):
            raise ValueError(
                f"Quantity should not be less than {self.min_value}"
                f"and greater than {self.max_value}."
            )


class OneOf(Validator):
    def __init__(self, options: tuple[str]) -> None:
        self.options = options

    def validate(self, value: str) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns: int = Number(min_value=2, max_value=3)
    cheese: int = Number(min_value=0, max_value=2)
    tomatoes: int = Number(min_value=0, max_value=3)
    cutlets: int = Number(min_value=1, max_value=3)
    eggs: int = Number(min_value=0, max_value=2)
    sauce: int = OneOf(options=("ketchup", "mayo", "burger"))

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
