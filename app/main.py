from __future__ import annotations
from typing import Any
from abc import ABC, abstractmethod


class Validator(ABC):
    @abstractmethod
    def validate(self, value: Any) -> bool:
        pass

    def __set_name__(self, owner: str, name: str) -> None:
        print(owner)
        self.protected_name = "_" + name

    def __get__(self, instance: Validator, owner: str) -> Any:
        print(owner)
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Validator, value: Any) -> None:
        setattr(instance, self.protected_name, value)


class Number(Validator):
    def __init__(self, minvalue: int, maxvalue: int) -> None:
        self.min_value = minvalue
        self.max_value = maxvalue

    def validate(self, value: Any) -> bool:
        if isinstance(value, int):
            if value in range(self.min_value, self.max_value + 1):
                return True
            error_text1 = f"Quantity should not be less than {self.max_value} "
            error_text2 = f"and greater than {self.min_value}."
            raise ValueError(error_text1 + error_text2)

        raise TypeError("Quantity should be integer.")

    def __set_name__(self, owner: str, name: str) -> None:
        return super().__set_name__(owner, name)

    def __get__(self, instance: Validator, owner: str) -> int:
        return super().__get__(instance, owner)

    def __set__(self, instance: Validator, value: Any) -> None:
        if self.validate(value):
            super().__set__(instance, value)


class OneOf(Validator):
    def __init__(
        self,
        valid_items: tuple = ("ketchup", "mayo", "burger")
    ) -> None:
        self.options = tuple(valid_items)

    def validate(self, value: Any) -> bool:
        if value in self.options:
            return True

        raise ValueError(f"Expected {value} to be one of {self.options}.")

    def __set_name__(self, owner: str, name: str) -> None:
        return super().__set_name__(owner, name)

    def __get__(self, instance: Validator, owner: str) -> int:
        return super().__get__(instance, owner)

    def __set__(self, instance: Validator, value: Any) -> None:
        if self.validate(value):
            super().__set__(instance, value)


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf()

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
