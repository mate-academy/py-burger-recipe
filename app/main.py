from abc import abstractmethod, ABC


class Validator(ABC):
    def __set_name__(self, owner, name: str) -> None:
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.protected_name)

    def __set__(self, instance, value):
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self,instance, value):
        pass


class Number(Validator):
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, instance, value):
        if not (type(value) == int):
            raise TypeError("Quantity should be integer")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(f"Quantity should not be less than {self.min_value} and greater than {self.max_value}")
        setattr(instance, self.protected_name, value)



class OneOf(Validator):
    def __init__(self, option) -> None:
        self.option = option

    def validate(self,instance, value):
        if  value is not self.option:
            raise ValueError (f"Expected {value} to be on of {self.option}")


class BurgerRecipe:
    def __init__(self, buns: int, cheese: int, tomatoes: int, cutlets: int, eggs: int, sauce: int) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
