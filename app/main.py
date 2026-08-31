from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner: object, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: object) -> int | str:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: str | int) -> None:
        if self.validate(value):
            setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int | str) -> bool:
        pass


class Number(Validator):
    def __init__(self, minvalue: int = 2, maxvalue: int = 12) -> None:
        self.min_value = minvalue
        self.max_value = maxvalue

    def validate(self, value: int) -> bool:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        elif self.min_value > value or self.max_value < value:
            raise ValueError(f"Quantity should not be less "
                             f"than {self.min_value} and greater "
                             f"than {self.max_value}.")
        return True


class OneOf(Validator):
    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value: str) -> bool:
        if value in self.options:
            return True
        else:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(("ketchup", "mayo", "burger"))

    def __init__(self,
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
        print("burger will be created")
