from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Generator


class Validator(ABC):
    def __set_name__(self, obj: any, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, obj: any = None, obj_type: type = None) -> any:
        return getattr(obj, self.protected_name)

    def __set__(self, obj: any, value: int) -> None:
        self.validate(value)
        setattr(obj, self.protected_name, value)

    _value = property(__get__, __set__)

    @abstractmethod
    def validate(self, value: any) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        elif self.min_value > value or self.max_value < value:
            print(f"Validating {value}")
            raise ValueError("Quantity should not be less than attribute "
                             "minvalue and greater than attribute maxvalue.")


class OneOf(Validator):
    def __init__(self, options: list) -> None:
        self.options = options

    def validate(self, value: str) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be "
                             f"one of ({self.__repr__()}).")

    def get_options(self) -> Generator[int, None, None]:
        for option in self.options:
            yield option

    def __repr__(self) -> str:
        gen = self.get_options()
        result = f"'{next(gen)}'"
        for i in range(1, len(self.options)):
            result += f", '{next(gen)}'"
        return result


class BurgerRecipe:
    def __init__(self,
                 buns: int,
                 cheese: int,
                 tomatoes: int,
                 cutlet: int,
                 eggs: int,
                 sauce: str) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlet
        self.eggs = eggs
        self.sauce = sauce

    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(["ketchup", "mayo", "burger"])
