from abc import ABC, abstractmethod


class Validator(ABC):
    def __init__(self, protected_name: str = "empty") -> None:
        self.protected_name = protected_name

    def __set_name__(self, owner: object, name: str) -> None:
        self.protected_name = self.name = "_" + name

    def __get__(self, instance: object, owner: object) -> None:
        return getattr(instance, self.name)

    def __set__(self, instance: object, value: int | str) -> None:
        self.validate(instance, value)

    @abstractmethod
    def validate(self, instance: object, value: int | str) -> None:
        pass


class Number(Validator):
    def __init__(self,
                 min_value: int,
                 max_value: int,
                 protected_name: str = "") -> None:
        super().__init__(protected_name)
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, instance: object, value: int) -> None:
        if isinstance(value, int):
            if self.max_value >= value >= self.min_value:
                setattr(instance, self.name, value)
            else:
                raise ValueError(f"Quantity should not be less than "
                                 f"{self.min_value} and greater than "
                                 f"{self.max_value}")
        else:
            raise TypeError("Quantity should be integer.")


class OneOf(Validator):
    def __init__(self,
                 options: tuple,
                 protected_name: str = "") -> None:
        super().__init__(protected_name)
        self.options = options

    def validate(self, instance: object, value: str) -> None:
        if value in self.options:
            setattr(instance, self.name, value)
        else:
            raise ValueError(f"Expected {value} "
                             f"to be one of {self.options}.")


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
                 sauce: str) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
