# https://github.com/mate-academy/py-burger-recipe/pull/238
from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner, name):
        protected_name = "_" + name

    def __get__(self, instance, owner):
        return instance

    def __set__(self, instance, value):
        return value

    @abstractmethod
    def validate(self):
        pass


class Number(Validator):

    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value



    def validate(self, value):
        print(type(value))
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer")
        if not self.min_value < value < self.max_value:
            raise ValueError(f"Quantity should not be less than "
                             f"{self.min_value} and greater than "
                             f"{self.max_value}.")



class OneOf(Validator):
    def __init__(self, options):
        self.options = options

    def validate(self, value):
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    def __init__(self, cheese, tomatoes, cutlets, eggs, buns, sauce):
        self.buns = Number(2, 3)
        self.cheese = Number(0, 2)
        self.tomatoes = Number(0, 3)
        self.cutlets = Number(1, 3)
        self.eggs = Number(0, 2)
        self.sauce = OneOf(["ketchup", "mayo", "burger"])

        self.buns.validate(buns)
        self.cheese.validate(cheese)
        self.tomatoes.validate(tomatoes)
        self.cutlets.validate(cutlets)
        self.eggs.validate(eggs)
        self.sauce.validate(sauce)

