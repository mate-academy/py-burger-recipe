from __future__ import annotations
from abc import abstractmethod, ABC


class Validator(ABC):
    def __set_name__(self, owner: Validator, name: str) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, instance: Validator, owner: Validator) -> int | str:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Validator, value: int | str) -> None:
        if self.validate(value):
            setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int | str) -> bool | TypeError:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        super().__init__()
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> bool | TypeError:
        if isinstance(value, int):
            if (self.min_value <= value <= self.max_value):
                return True
            less_than_str = (
                f"Quantity should not be less than {self.min_value}"
            )
            greater_than_str = f"and greater than {self.max_value}."
            raise ValueError(f"{less_than_str} {greater_than_str}")
        raise TypeError("Quantity should be integer.")


class OneOf(Validator):
    def __init__(self, options: tuple) -> None:
        super().__init__()
        self.options = options

    def validate(self, value: str) -> bool | TypeError:
        if value in self.options:
            return True
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
