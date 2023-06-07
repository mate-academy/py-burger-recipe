from abc import abstractmethod, ABC
from typing import Any, Type


class Validator(ABC):

    def __set_name__(self, owner: Type, name: str) -> None:
        self.name = name
        self.protected_name = "_" + name

    def __get__(self, attribute: "BurgerRecipe", owner: Type) -> Any:
        return getattr(attribute, self.protected_name)

    def __set__(self, attribute: "BurgerRecipe", value: Any) -> Any:
        setattr(attribute, self.protected_name, value)

    @abstractmethod
    def validate(self, value: Any) -> Any:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def __set__(self, instance: "BurgerRecipe", value: int) -> None:
        if self.validate(value):
            super().__set__(instance, value)

    def validate(self, value: int) -> bool:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(f"Quantity should not be less than "
                             f"{self.min_value} and greater than "
                             f"{self.max_value}.")
        return True


class OneOf(Validator):
    def __init__(self, options: tuple) -> None :
        self.options = options

    def __set__(self, instance: "BurgerRecipe", value: str) -> None:
        if self.validate(value):
            super().__set__(instance, value)

    def validate(self, value: str) -> bool:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")
        return True


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
                 cutlets: int, eggs: int,
                 sauce: str) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
