from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, obj: object, objtype: type = None) -> any:
        return getattr(obj, self.protected_name)

    def __set__(self, obj: object, value: any) -> None:
        self.validate(value)
        setattr(obj, self.protected_name, value)

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
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"Quantity should not be less than {self.min_value} "
                f"and greater than {self.max_value}.")


class OneOf(Validator):
    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value: any) -> None:
        if value not in self.options:
            raise ValueError(
                f"Expected {value} to be one of {self.options}."
            )


class BurgerRecipe:
    buns: Validator = Number(min_value=2, max_value=3)
    cheese: Validator = Number(min_value=0, max_value=2)
    tomatoes: Validator = Number(min_value=0, max_value=3)
    cutlets: Validator = Number(min_value=1, max_value=3)
    eggs: Validator = Number(min_value=0, max_value=2)
    sauce: Validator = OneOf(options=("ketchup", "mayo", "burger"))

    def __init__(self, buns: int,
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
