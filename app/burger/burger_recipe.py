from app.burger.validators.validator import Validator
from app.burger.validators.number import Number
from app.burger.validators.one_of import OneOf


class BurgerRecipe:
    burger = Validator()

    def __init__(
            self,
            buns: int = Number(2,3),
            cheese: int = Number(0, 2),
            tomatoes: int = Number(0, 3),
            cutlets: int = Number(1, 3),
            eggs: int = Number(0, 2),
            sauce: str = OneOf(("ketchup", "mayo", "burger"))) -> None:
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
