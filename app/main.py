from abc import ABC, abstractmethod
from typing import Any


class Validator(ABC):
    def __set_name__(
            self,
            owner: Any,
            name: str
    ) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(
            self,
            obj: Any,
            obj_type: Any = None
    ) -> Any:
        value = getattr(obj, self.protected_name)

        return value

    def __set__(
            self,
            obj: Any,
            value: Any
    ) -> None:
        setattr(obj, self.protected_name, self.validate(value))

    @abstractmethod
    def validate(self, value: Any) -> Any:
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
        if type(value) != int:
            raise TypeError(
                "Quantity should be integer."
            )

        if value < self.min_value or value > self.max_value:
            raise ValueError(
                f"Quantity should not be less than {self.min_value} "
                f"and greater than {self.max_value}"
            )

        return value


class OneOf(Validator):
    def __init__(
            self,
            options: tuple[str, str, str],
    ) -> None:
        self.options = options

    def validate(self, value: str) -> str:
        if value not in self.options:
            raise ValueError(
                f"Expected {value} to be one of {self.options}."
            )

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
            sauce: str,
    ) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
