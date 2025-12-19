class Validator:
    def __set_name__(self, owner: type, name: str) -> None:
        self.protected_name: str = "_" + name

    def __get__(self, instance: object, owner: type) -> object:
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: object) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    def validate(self, value: object) -> None:
        raise NotImplementedError("Subclasses must implement validate method")


class Number(Validator):
    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value: int = min_value
        self.max_value: int = max_value

    def validate(self, value: object) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"Quantity should not be less than {self.min_value} "
                f"and greater than {self.max_value}."
            )


class OneOf(Validator):
    def __init__(self, *options: str) -> None:
        self.options: tuple[str, ...] = options

    def validate(self, value: object) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns: Number = Number(2, 3)
    cheese: Number = Number(0, 2)
    tomatoes: Number = Number(0, 3)
    cutlets: Number = Number(1, 3)
    eggs: Number = Number(0, 2)
    sauce: OneOf = OneOf("ketchup", "mayo", "burger")

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
