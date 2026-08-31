from abc import ABC, abstractmethod


class Validator(ABC):
    """
    Base Descriptor Class.
    """

    def __set_name__(self, owner, name):
        # Adds _ to the beginning and stores it in protected_name
        self.protected_name = "_" + name

    def __get__(self, instance, owner):
        # Returns the attribute value
        return getattr(instance, self.protected_name)

    def __set__(self, instance, value):
        # Validates and sets the attribute value
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value):
        # Abstract method to be implemented by child classes
        pass


class Number(Validator):
    """
    Validates that a value is an integer and within a specific range.
    """

    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value):
        # Check type
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")

        # Check range
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"Quantity should not be less than {self.min_value} and greater than {self.max_value}."
            )


class OneOf(Validator):
    """
    Validates that a value is one of the allowed options.
    """

    def __init__(self, options):
        self.options = options

    def validate(self, value):
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    """
    The main class describing the burger recipe using descriptors.
    """

    # Descriptors created as class attributes with specified constraints
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(('ketchup', 'mayo', 'burger'))

    def __init__(self, buns, cheese, tomatoes, cutlets, eggs, sauce):
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
