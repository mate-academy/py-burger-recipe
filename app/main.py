from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner: int, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: int | str, owner: int) -> int:
        self.validate(getattr(instance, self.protected_name))
        return getattr(instance, self.protected_name)

    def __set__(self, instance: int | str, value: int | str) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int | str) -> None:
        pass


class Number(Validator, ABC):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int | str) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")

        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"Quantity should not be less than {self.min_value}"
                f"and greater than {self.max_value}."
            )


class OneOf(Validator, ABC):
    def __init__(self, options: None) -> None:
        self.options = options or set()

    def validate(self, value: int | str) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns = Number(min_value=2, max_value=3)
    cheese = Number(min_value=0, max_value=2)
    tomatoes = Number(min_value=0, max_value=3)
    cutlets = Number(min_value=1, max_value=3)
    eggs = Number(min_value=0, max_value=2)
    sauce = OneOf(options=("ketchup", "mayo", "burger"))

    def __init__(
        self,
        buns: int = 0,
        cheese: int = 0,
        tomatoes: int = 0,
        cutlets: int = 0,
        eggs: int = 0,
        sauce: int = 0,
    ) -> None:
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.buns = buns
        self.sauce = sauce
