class Validator:
    pass


class Number:
    pass


class OneOf:
    pass


class BurgerRecipe:
    # buns = Number(2, 3)
    # cheese = Number(0, 2)
    # tomatoes = Number(0, 3)
    # cutlets = Number(1, 3)
    # eggs = Number(0, 2)
    # sauce = Validator("ketchup", "mayo", "burger")

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
