from abc import ABC, abstractmethod
from typing import Any


class Validator(ABC):

    def __set_name__(
            self,
            owner,
            name
    ) -> None:
        self.protected_name = "_" + name

    def __get__(
            self,
            instance,
            owner
    ) -> Any:
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(
            self,
            instance,
            value
    ) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value) -> None:
        raise NotImplementedError

class Number(Validator):
    def __init__(
            self,
            min_value: int,
            max_value: int
    ) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value) -> None:
        if not isinstance(value, int):
                raise TypeError(
                    "Quantity should be integer."
                )
        if value not in range(self.min_value, self.max_value + 1):
            raise ValueError(
                f"Quantity should not be less than "
                f"{self.min_value} and greater than "
                f"{self.max_value}.")


class OneOf(Validator):
    def __init__(
            self,
            options: Any
    ) -> None:
        self.options = options

    def validate(self, value) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    cheese = Number(2, 3)
    tomatoes = Number(0,2)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    buns = Number(2, 3)
    sauce = OneOf(("ketchup", "mayo", "burger"))

    def __init__(
            self,
            cheese: int,
            tomatoes: int,
            cutlets: int,
            eggs: int,
            buns: int,
            sauce: str
    ) -> None:
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.buns = buns
        self.sauce = sauce
