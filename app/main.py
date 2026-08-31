from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner: None, name: None) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, instance: None, owner: None) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: None, value: None) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: None) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: None) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(f"Quantity should not be less than "
                             f"{self.min_value}"f" and greater than "
                             f"{self.max_value}.")


class OneOf(Validator):
    def __init__(self, options: None) -> None:
        self.options = options

    def validate(self, value: None) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns = Number(min_value=2, max_value=3)
    cheese = Number(min_value=0, max_value=2)
    tomatoes = Number(min_value=0, max_value=3)
    cutlets = Number(min_value=1, max_value=3)
    eggs = Number(min_value=0, max_value=2)
    sauce = OneOf(options=("ketchup", "mayo", "burger"))

    def __init__(self, buns: None, cheese: None, tomatoes: None,
                 cutlets: None, eggs: None, sauce: None) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
