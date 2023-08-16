from abc import ABC, abstractmethod
from typing import Type, Any


class Validator(ABC):
    def __set_name__(self, owner: Type, name: str) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, instance: object, owner: Type) -> object:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: object) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: object) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> Any:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if value < self.min_value or value > self.max_value:
            raise ValueError(f"Quantity should not be less than "
                             f"{self.min_value} and greater "
                             f"than {self.max_value}.")


class OneOf(Validator):
    def __init__(self, options: int) -> None:
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
    sauce = OneOf(("ketchup", "mayo", "burger"))

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


try:
    burger = BurgerRecipe(buns="1",
                          cheese="1",
                          tomatoes="1",
                          cutlets="1",
                          eggs="1",
                          sauce="mayo")
except TypeError as e:
    print(e)

try:
    burger = BurgerRecipe(buns=1,
                          cheese=10,
                          tomatoes=1,
                          cutlets=1,
                          eggs=1,
                          sauce="mayo")
except ValueError as e:
    print(e)

try:
    burger = BurgerRecipe(buns=2,
                          cheese=1,
                          tomatoes=1,
                          cutlets=1,
                          eggs=1,
                          sauce="mustard")
except ValueError as e:
    print(e)

burger = BurgerRecipe(buns=2,
                      cheese=1,
                      tomatoes=1,
                      cutlets=1,
                      eggs=1,
                      sauce="ketchup")
print("Burger will be created")
