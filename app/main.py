from app.validators import Validator, Number, OneOf
Validator = Validator

BUNS = Number(2, 3)
CHEESE = Number(0, 2)
TOMATOES = Number(0, 3)
CUTLETS = Number(1, 3)
EGGS = Number(0, 2)
SAUCE = OneOf(["ketchup", "mayo", "burger"])


class BurgerRecipe:
    buns = BUNS
    cheese = CHEESE
    tomatoes = TOMATOES
    cutlets = CUTLETS
    eggs = EGGS
    sauce = SAUCE

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
