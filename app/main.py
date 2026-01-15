from abc import ABC, abstractmethod

class Validator(ABC):
    def __set_name__(self, owner, name):
        # Armazena o nome com um sublinhado (ex: buns -> _buns)
        self.protected_name = f"_{name}"

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self, instance, value):
        # Chama a validação específica da subclasse antes de atribuir
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value):
        pass

class Number(Validator):
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"Quantity should not be less than {self.min_value} and greater than {self.max_value}."
            )

class OneOf(Validator):
    def __init__(self, *options):
        # Armazena as opções permitidas
        self.options = options

    def validate(self, value):
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")

class BurgerRecipe:
    # Definindo os descritores como atributos de classe
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf("ketchup", "mayo", "burger")

    def __init__(self, buns, cheese, tomatoes, cutlets, eggs, sauce):
        # As atribuições abaixo disparam o método __set__ de cada descritor
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
