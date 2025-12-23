from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner: type, name: str) -> None:
        print(owner, name)
        self.protected_name = f"_{name}"

    def __get__(self, instance: object, owner: type) -> int | str:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: int | str) -> None:
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int | str) -> None:
        pass


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def __set__(self, instance: object, value: int) -> None:
        self.validate(value)
        super().__set__(instance, value)

    def validate(self, value: int | str) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")

        if value < self.min_value or value > self.max_value:
            raise ValueError(
                f"Quantity should not be less than {self.min_value} "
                f"and greater than {self.max_value}."
            )


class OneOf(Validator):
    def __init__(self, options: list[str]) -> None:
        self.options = options

    def __set__(self, instance: object, value: str) -> None:
        self.validate(value)
        super().__set__(instance, value)

    def validate(self, value: str) -> None:
        if value not in self.options:
            raise ValueError(
                f"Expected {value} to be one of "
                f"('{"', '".join(self.options)}')."
            )


class BurgerRecipe:
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(["ketchup", "mayo", "burger"])

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
