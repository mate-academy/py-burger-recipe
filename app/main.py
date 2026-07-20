from abc import ABC, abstractmethod
from typing import Any


class Validator(ABC):
    """
    Abstract base class for descriptor-based validators.

    Implements the descriptor protocol (__set_name__, __get__, __set__)
    so subclasses can be used as class-level attributes that validate
    values on assignment.

    Subclasses must implement:
        - validate: raises TypeError or ValueError on invalid input.
    """

    @abstractmethod
    def validate(self, value: Any) -> None:
        """
        Validate the given value.

        Raises TypeError or ValueError if the value does not meet
        the subclass-specific constraints.
        """

    def __set_name__(self, owner: type, name: str) -> None:
        """
        Store the attribute name with a leading underscore as the
        private storage name on the owner class.
        """
        self.protected_name = "_" + name

    def __get__(self, instance: Any, owner: type) -> Any:
        """
        Return the stored value from the instance, or the descriptor
        itself when accessed on the class.
        """
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: Any) -> None:
        """
        Validate and store value on the instance.
        """
        self.validate(value)
        setattr(instance, self.protected_name, value)


class Number(Validator):
    """
    Validator that enforces an integer value within a closed range.

    Raises:
        TypeError: if the value is not an int.
        ValueError: if the value is outside [min_value, max_value].
    """

    def __init__(self, min_value: int, max_value: int) -> None:
        """
        Initialize the validator with inclusive lower and upper bounds.
        """
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:
        """
        Validate that value is an integer within [min_value, max_value].
        """
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not self.min_value <= value <= self.max_value:
            raise ValueError(
                f"Quantity should not be less than {self.min_value} "
                f"and greater than {self.max_value}."
            )


class OneOf(Validator):
    """
    Validator that enforces a value to be one of the allowed options.

    Raises:
        ValueError: if the value is not present in options.
    """

    def __init__(self, options: tuple[str, ...]) -> None:
        """
        Initialize the validator with the tuple of allowed string values.
        """
        self.options = options

    def validate(self, value: str) -> None:
        """
        Validate that value is contained in the allowed options.
        """
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    """
    Descriptor-validated recipe for assembling a burger.

    Class-level descriptors enforce valid ranges for each ingredient
    and restrict the sauce to a predefined set of options.

    Attributes:
        buns: number of buns (2–3).
        cheese: number of cheese slices (0–2).
        tomatoes: number of tomato slices (0–3).
        cutlets: number of cutlets (1–3).
        eggs: number of eggs (0–2).
        sauce: sauce type, one of SAUCES.
    """

    SAUCES: tuple[str, ...] = ("ketchup", "mayo", "burger")
    buns = Number(min_value=2, max_value=3)
    cheese = Number(min_value=0, max_value=2)
    tomatoes = Number(min_value=0, max_value=3)
    cutlets = Number(min_value=1, max_value=3)
    eggs = Number(min_value=0, max_value=2)
    sauce = OneOf(SAUCES)

    def __init__(
        self,
        buns: int,
        cheese: int,
        tomatoes: int,
        cutlets: int,
        eggs: int,
        sauce: str,
    ) -> None:
        """
        Create a BurgerRecipe, validating every ingredient on assignment.
        """
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
