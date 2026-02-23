class Validator:
    pass


class Number:
    pass


class OneOf:
    pass

# End validator classes
class BurgerRecipe:

    buns = Number()
    cheese = Number()
    tomatoes = Number()
    cutlets = Number()
    eggs = Number()
    sauces = OneOf('ketchup', 'mustard', 'mayo')
    
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
