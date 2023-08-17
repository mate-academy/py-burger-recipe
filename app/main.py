from abc import ABC, abstractmethod
from typing import Generic, Type, TypeVar

Instance = TypeVar("Instance")
Value = TypeVar("Value")


class Validator(ABC, Generic[Instance, Value]):
    def __set_name__(self, _: Instance, name: str) -> None:
        self.protected_name: str = "_" + name

    def __get__(self, instance: Instance, _: Type[Instance]) -> Value:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Instance, value: Value) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: Value) -> None:
        pass


class Number(Validator[Instance, Value]):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value: int = min_value
        self.max_value: int = max_value

    def validate(self, value: Value) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if value not in range(self.min_value, self.max_value + 1):
            raise ValueError(
                f"Quantity should not be less than {self.min_value} "
                f"and greater than {self.max_value}."
            )


class OneOf(Validator[Instance, Value]):
    def __init__(self, options: tuple[str, ...]) -> None:
        self.options: tuple[str, ...] = options

    def validate(self, value: Value) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    buns = Number(2, 3)
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
