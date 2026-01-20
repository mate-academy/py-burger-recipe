from abc import abstractmethod


class Validator:

    def __set_name__(self, owner: object, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: object, owner: object) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: any) -> None:
        if self.validate(value):
            setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: any) -> bool:
        pass


class Number(Validator):

    def __init__(self, minvalue: int, maxvalue: int) -> None:
        self.minvalue = minvalue
        self.maxvalue = maxvalue

    def validate(self, value: int) -> bool:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if value not in range(self.minvalue, self.maxvalue + 1):
            value_error = f"Quantity should not be less than {self.min_value} "
            value_error += f"and greater than {self.max_value}."
            raise ValueError(value_error)
        return True


class OneOf(Validator):
    def __init__(self, options: list[str]) -> None:
        self.options = options

    def validate(self, value: str) -> bool:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")
        return True


class BurgerRecipe:

    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    egs = Number(0, 2)
    sauce = OneOf(["ketchup", "mayo", "burguer"])

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
