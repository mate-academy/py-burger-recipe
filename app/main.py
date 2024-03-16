from abc import ABC, abstractmethod


class Validator(ABC):

    def __set_name__(self, owner, name):
        self.protected_name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.protected_name)

    def __set__(self, instance, value):
        return setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value:int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError(f"Quantity should be integer.")

        if not (self.min_value <= value <= self.max_value):
            raise ValueError(f"Quantity should not be less than {self.min_value} and greater than {self.max_value}.")




class OneOf:
    pass


class BurgerRecipe:
    def __init__(self,
                 buns: int,
                 cheese: int,
                 tomatoes:int,
                 cutlets: int,
                 eggs: int,
                 sauce: str) -> None:

        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
