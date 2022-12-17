from abc import abstractmethod, ABC


class Validator(ABC):
    def __set_name__(self, owner, name):
        self.public_name = name
        self.protected_name = "_" + name

    def __get__(self, value, owner):
        return getattr(value, self.protected_name)

    def __set__(self, value, new_value):
        pass

    @abstractmethod
    def validate(self, value) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value, max_value) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def __set__(self, value, new_value):
        return setattr(value, self.protected_name, self.validate(new_value))

    def validate(self, value) -> int:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if value < self.min_value or value > self.max_value:
            raise ValueError(f"Quantity should not be "
                             f"less than {self.min_value} "
                             f"and greater than {self.max_value}.")
        return value


class OneOf(Validator):
    def __init__(self, options: tuple) -> None:
        self.options = options

    def __set__(self, value, new_value):
        return setattr(value, self.protected_name, self.validate(new_value))

    def validate(self, value) -> str:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")
        return value


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(("ketchup", "mayo", "burger"))

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
