class Validator:

    def __set_name__(self, owner, name):
        self.protected_name = "_" + name

    def __get__(self, instance, owner):
        return getattr(instance, self.protected_name)






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
