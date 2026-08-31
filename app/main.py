from __future__ import annotations
from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, instance: BurgerRecipe, owner: type) -> Validator:
        if instance is None:
            return self

        return getattr(instance, self.protected_name)

    def __set__(self, instance: BurgerRecipe, value: int) -> None:
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int | str) -> int | str:
        pass


class Number(Validator):
    def __init__(
        self,
        min_value: int,
        max_value: int,
    ) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> int:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")

        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"Quantity should not be less than {self.min_value} "
                f"and greater than {self.max_value}."
            )

        return value


class OneOf(Validator):
    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value: str) -> str:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")
        return value


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
        self.buns = type(self).buns.validate(buns)
        self.cheese = type(self).cheese.validate(cheese)
        self.tomatoes = type(self).tomatoes.validate(tomatoes)
        self.cutlets = type(self).cutlets.validate(cutlets)
        self.eggs = type(self).eggs.validate(eggs)
        self.sauce = type(self).sauce.validate(sauce)
