from typing import Type
from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self: Type, owner: Type, name: str) -> None:
        self.protected_name = '_' + name

    def __get__(self: Type, instance: Type, owner:Type) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance, value):
        self.validate(value)
        return setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError('Quantity should be integer.')
        if self.min_value is not None and value < self.min_value:
            raise ValueError(f'Value {value} is below minimum {self.min_value}')
        if self.max_value is not None and value > self.max_value:
            raise ValueError(f'Value {value} exceeds maximum {self.max_value}')


class OneOf(Validator):
    def __init__(self, options):
        self.options = options

    def validate(self, value):
        if value not in self.options:
            raise ValueError(f'Expected {value} to be one of {self.options}.')


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(('ketchup', 'mayo', 'burger'))

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
