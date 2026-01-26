from abc import abstractmethod, ABC
from typing import Any


class Validator(ABC):
    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Any, owner: type) -> Any:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: Any) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int | str) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if self.min_value <= value <= self.max_value:
            setattr(self, self.protected_name, value)
        else:
            raise ValueError(
                "Quantity should not be less than "
                "attribute minvalue and greater than attribute maxvalue."
            )


class OneOf(Validator):
    def __init__(self, *options: str) -> None:
        self.options = options

    def validate(self, value: str) -> None:
        if value in self.options:
            setattr(self, self.protected_name, value)
        else:
            raise ValueError(f"Expected {value} "
                             f"to be one of {self.options}.")


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf("ketchup", "mayo", "burger")

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
        self.sauce = sauce
        self.eggs = eggs
