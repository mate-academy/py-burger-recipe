from abc import abstractmethod, ABC
from collections.abc import Callable


class Validator(ABC):
    def __set_name__(self, owner: Callable, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: Callable, owner: Callable) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Callable, value: int) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:
        if isinstance(value, int):
            if not (self.min_value <= value <= self.max_value):
                raise ValueError(f"Quantity should not be less than "
                                 f"{self.min_value} and greater "
                                 f"than {self.max_value}")
            return
        raise TypeError("Quantity should be integer.")


class OneOf(Validator):
    def __init__(self) -> None:
        self.options = ("ketchup", "mayo", "burger")

    def validate(self, value: str) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} "
                             f"to be one of {self.options}.")
        print("burger will be created")


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf()

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
        self.eggs = eggs
        self.sauce = sauce
