from __future__ import annotations
from abc import abstractmethod, ABC


class Validator(ABC):
    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: type, owner: type) -> int | str:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: type, value: int | str) -> None:
        return setattr(instance, self.protected_name, self.validate(value))

    @abstractmethod
    def validate(self, value: any) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: any) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        elif value in range(self.min_value, self.max_value + 1):
            return value
        else:
            raise ValueError(
                f"Quantity should not be less than {self.min_value}"
                f" and greater than {self.max_value}."
            )


class OneOf(Validator):
    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value: any) -> None:
        if value in self.options:
            return value
        else:
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
