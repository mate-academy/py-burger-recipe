from abc import abstractmethod, ABC


class Validator(ABC):
    def __set_name__(self, owner: str, name: str) -> None:
        self.protected_name = name
        self.protected_name = "_" + name

    def __get__(self, instance: str, owner: str) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, key: str, value: str) -> None:
        return setattr(key, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int or str) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if value < self.min_value or value > self.max_value:
            raise ValueError(
                f"Quantity should not be less than {self.min_value} "
                f"and greater than {self.max_value}."
            )


class OneOf(Validator):
    def __init__(self, options: tuple) -> None:
        self.options = options

    def validate(self, value: str) -> None:
        if value not in self.options:
            raise ValueError(
                f"Expected {value} to be one of {self.options}."
            )


class BurgerRecipe:
    sauce_list = ("ketchup", "mayo", "burger")

    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(sauce_list)

    def __init__(
            self,
            buns: int,
            cheese: int,
            tomatoes: int,
            cutlets: int,
            eggs: int,
            sauce: str,
    ) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce

        sauce_list = ("ketchup", "mayo", "burger")

        Number(2, 3).validate(self.buns)
        Number(0, 2).validate(self.cheese)
        Number(0, 3).validate(self.tomatoes)
        Number(1, 3).validate(self.cutlets)
        Number(0, 2).validate(self.eggs)
        OneOf(sauce_list).validate(self.sauce)
