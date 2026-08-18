from abc import ABC, abstractmethod
from typing import Any


class Validator(ABC):
    """Base descriptor for validating attribute values."""

    protected_name: str

    def __set_name__(self, owner: type, name: str) -> None:
        """Create the protected name used to store the attribute value."""
        self.protected_name = "_" + name

    def __get__(self, instance: object | None, owner: type) -> Any:
        """Return the descriptor or the stored attribute value."""
        if instance is None:
            return self
        return getattr(instance, self.protected_name)

    def __set__(self, instance: object, value: Any) -> None:
        """Validate and store an attribute value."""
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: Any) -> None:
        """Validate a value before it is assigned."""
        pass


class Number(Validator):
    """Validate an integer within a specified range."""

    def __init__(self, min_value: int, max_value: int) -> None:
        """Initialize the allowed numeric range."""
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any) -> None:
        """Check the value type and range."""
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(f"Quantity should not be less than "
                             f"{self.min_value} and greater than "
                             f"{self.max_value}.")


class OneOf(Validator):
    """Validate that a value is one of the allowed options."""

    def __init__(self, options: tuple[str, ...]) -> None:
        """Initialize the allowed options."""
        self.options = options

    def validate(self, value: Any) -> None:
        """Check that the value is an allowed option."""
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    """Represent a validated burger recipe."""

    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf(("ketchup", "mayo", "burger"))

    def __init__(
        self,
        buns: int,
        cheese: int,
        tomatoes: int,
        cutlets: int,
        eggs: int,
        sauce: str
    ) -> None:
        """Initialize a burger recipe with the provided ingredients."""
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
