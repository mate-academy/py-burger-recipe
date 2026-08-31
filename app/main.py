from abc import abstractmethod, ABC
from typing import Tuple


class Validator(ABC):
    def __set_name__(self, owner: type, name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, instance: object | None, owner: type) -> object | None:
        return getattr(instance,
                       self.protected_name)

    def __set__(self, instance: object | None, value: Tuple) -> None:
        self.validate(value)
        setattr(instance,
                self.protected_name,
                value)

    @abstractmethod
    def validate(self, value: Tuple) -> None:
        pass


class Number(Validator):
    def __init__(self,
                 min_value: int,
                 max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: tuple) -> None:
        if isinstance(value, int):
            if not self.min_value <= value <= self.max_value:
                raise ValueError(f"Quantity should not be less "
                                 f"than {self.min_value} and "
                                 f"greater "
                                 f"than {self.max_value}.")
        else:
            raise TypeError("Quantity should be integer.")


class OneOf(Validator):
    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value: Tuple) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} "
                             f"to be one of {self.options}.")


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(("ketchup", "mayo", "burger"))

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
