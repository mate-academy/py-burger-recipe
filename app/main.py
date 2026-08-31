from abc import ABC, abstractmethod
from typing import Any, Type, Optional


class Validator(ABC):
    """
    Abstract base class for attribute validators (descriptors).

    This class implements Python's descriptor protocol to manage the storage of
    protected attributes and delegates the validation logic to its subclasses.
    """

    def __set_name__(
        self,
        owner: Type[Any],
        name: str
    ) -> None:
        """
        Assigns the attribute name with an underscore prefix.

        Args:
            owner: The owning class where the descriptor is defined.
            name: The name of the assigned attribute in the class.
        """
        self.protected_name = "_" + name

    def __get__(
        self,
        obj: Optional[Any],
        objtype: Optional[Type[Any]] = None
    ) -> Any:
        """
        Returns the attribute value from the instance of the  object.

        Args:
            obj: The object instance through which the attribute is accessed.
            objtype: The object type (optional).

        Returns:
            Any: The value stored in the protected attribute or the instance
                of the descriptor if accessed from the class.
        """
        if obj is None:
            return self
        return getattr(obj, self.protected_name)

    def __set__(
        self,
        obj: Any,
        value: Any
    ) -> None:
        """
        Validates and sets the value in the object's protected attribute.

        Args:
            obj: The object instance where the value will be set.
            value: The value to be assigned.
        """
        self.validate(value)
        setattr(obj, self.protected_name, value)

    @abstractmethod
    def validate(
        self,
        value: Any
    ) -> None:
        """
        Abstract method to implement specific validation logic.

         Args:
            value: The value to validate.

        Raises:
            NotImplementedError:
                If the subclass does not implement this method.
        """
        pass


class Number(Validator):
    """
    Descriptor to validate that a value is an integer within a range.

    Attributes:
        min_value (int): The minimum allowed value.
        max_value (int): The maximum allowed value.
    """

    def __init__(
        self,
        min_value: int,
        max_value: int
    ) -> None:
        """
        Initializes the number validator.

        Args:
            min_value (int): Lower limit.
            max_value (int): Upper limit.
        """
        self.min_value = min_value
        self.max_value = max_value

    def validate(
        self,
        value: int
    ) -> None:
        """
        Checks if the value is an integer and within the range.

        Args:
            value (int): The value to validate.

        Raises:
            TypeError: If the value is not an integer.
            ValueError: If the value is outside [min_value,  max_value].
        """
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        elif value < self.min_value or value > self.max_value:
            raise ValueError(
                f"Quantity should not be less than {self.min_value} and greater than {self.max_value}"
            )


class OneOf(Validator):
    """
    Descriptor that validates whether a value belongs to a set
    of allowed options.

    Attributes:
        options (tuple): Collection of valid values for the attribute.
    """

    def __init__(
        self,
        *options: str
    ) -> None:
        """
        Initializes the validator with the allowed options.

        Args:
            *options: A variable number of strings representing the
                valid options (e.g., 'ketchup', 'mayo').
        """
        self.options = options

    def validate(
        self,
        value: str
    ) -> None:
        """
        Checks if the provided value is within the options.

        Args:
            value: The string to validate.

        Raises:
            ValueError: If the value is not found in the allowed options,
            including the tuple format and a period at the end of the message.
        """
        if value not in self.options:
            raise ValueError(
                f"Expected {value} to be one of {self.options}."
            )


class BurgerRecipe:
    """
    Class representing a validated burger recipe.

    Attributes:
        buns (int): Number of buns (2-3).
        cheese (int): Amount of cheese (0-2).
        tomatoes (int): Number of tomatoes (0-3).
        cutlets (int): Number of patties (1-3).
        eggs (int): Number of eggs (0-2).
        sauce (str): Sauce type ('ketchup', 'mayo', 'burger').
    """
    buns = Number(2, 3)
    cheese = Number(0, 2)
    tomatoes = Number(0, 3)
    cutlets = Number(1, 3)
    eggs = Number(0, 2)
    sauce = OneOf("ketchup", "mayo", "burger")

    def __init__(
        self,
        buns: int,
        cheese: int,
        tomatoes: int,
        cutlets: int,
        eggs: int,
        sauce: str
    ) -> None:
        """
        Creates a new instance of BurgerRecipe.

        Args:
            buns: Number of  buns.
            cheese: Number of cheese slices.
            tomatoes: Number of tomato slices.
            cutlets: Number of meat medallions.
            eggs: Number of eggs.
            sauce: Name of the sauce.
        """
        self.buns = buns
        self. cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
