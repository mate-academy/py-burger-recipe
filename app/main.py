from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner, name) -> None:
        self.protected_name = f"_{name}"

    def __get__(self, obj, objtype=None) -> int | str:
        return getattr(obj, self.protected_name)

    def __set__(self, obj, value) -> None:
        self.validate(value)
        setattr(obj, self.protected_name, value)

    @abstractmethod
    def validate(self, value):
        pass
class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        object.__setattr__(self, '_min_value', min_value)
        object.__setattr__(self, '_max_value', max_value)
    
    @property
    def min_value(self):
        return self._min_value
    
    @property
    def max_value(self):
        return self._max_value
    
    def validate(self, value) -> int:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        
        if value < self.min_value or value > self.max_value:
            raise ValueError(f"Quantity should not be less than {self.min_value} and greater than {self.max_value}.")

class OneOf(Validator):
    def __init__(self, options: tuple) -> None:
        object.__setattr__(self, '_options', options)
    
    @property
    def options(self):
        return self._options
    
    def validate(self, value: str) -> str:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")



class BurgerRecipe:
    eggs = Number(0, 2)
    cutlets = Number(1, 3)
    tomatoes = Number(0, 3)
    cheese = Number(0, 2)
    buns = Number(2, 3)
    sauce = OneOf(('ketchup', 'mayo', 'burger'))


    def __init__(self, 
                cheese: int,
                tomatoes: int,
                cutlets: int,
                eggs: int,
                buns: int,
                sauce: str) -> None:
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.buns = buns
        self.sauce = sauce
