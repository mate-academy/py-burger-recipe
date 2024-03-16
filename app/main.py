class Validator:


class Number:
    pass


class OneOf:
    pass


class BurgerRecipe:
    def __init__(self,
                 buns: int,
                 cheese: int,
                 tomatoes:int,
                 cutlets: int,
                 eggs: int,
                 sauce: str) -> None:

        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
