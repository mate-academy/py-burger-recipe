from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(self, owner, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance) -> int:
        return getattr(instance, self.protected_name)

    def __set__(self, instance, value) -> None:
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self) -> None:
        pass


class Number(Validator, ABC):
    def __init__(self, min_value, max_value) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value) -> None:
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")

        if (
            self.min_value is not None
            and value < self.min_value
            or self.max_value is not None
            and value > self.max_value
        ):
            raise ValueError(
                f"Quantity should not "
                f"be less than {self.min_value} "
                f"and greater than {self.max_value}."
            )


class OneOf(Validator, ABC):
    def __init__(self, options) -> None:
        self.options = options or set()

    def validate(self, value) -> None:
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    buns = Number(min_value=2, max_value=3)
    cheese = Number(min_value=0, max_value=2)
    tomatoes = Number(min_value=0, max_value=3)
    cutlets = Number(min_value=1, max_value=3)
    eggs = Number(min_value=0, max_value=2)
    sauce = OneOf(options={"ketchup", "mayo", "burger"})

    def __init__(
        self,
        cheese: int = 0,
        tomatoes: int = 0,
        cutlets: int = 0,
        eggs: int = 0,
        buns: int = 0,
        sauce: int = 0,
    ) -> None:
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.buns = buns
        self.sauce = sauce


if __name__ == "__main__":
    burger = BurgerRecipe(
        buns="1", cheese="1", tomatoes="1", cutlets="1", eggs="1", sauce="mayo"
    )
    print(burger.buns)

    burger = BurgerRecipe(
        buns=1, cheese=10, tomatoes=1, cutlets=1, eggs=1, sauce="mayo"
    )
    print(burger.cheese)

    burger = BurgerRecipe(
        buns=2, cheese=1, tomatoes=1, cutlets=1, eggs=1, sauce="mustard"
    )
    print(burger.sauce)

    burger = BurgerRecipe(
        buns=2, cheese=1, tomatoes=1, cutlets=1, eggs=1, sauce="ketchup"
    )
