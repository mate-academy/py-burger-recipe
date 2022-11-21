class Validator:
    
    def __setname__(self, name_of_the_attribute: str) -> str:
        return "_" + name_of_the_attribute

    def __set__(self, name_of_the_attribute: str, value: int) -> None:
       name_of_the_attribute = value 
    
    def __get__(name_of_the_attribute):
        return name_of_the_attribute
    



class Number:
    pass


class OneOf:
    pass


class BurgerRecipe:
    def __init__(self,
                 buns: int,
                 cheese: int,
                 tomatoes: int,
                 cutlets: int,
                 eggs: int,
                 sauce: int)
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce

