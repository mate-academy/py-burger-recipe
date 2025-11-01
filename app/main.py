from __future__ import annotations
from abc import ABC, abstractmethod


class Validator(ABC):
    """Abstract base class for creating validators."""

    @abstractmethod
    def validate(self, value: int | str) -> None:
        """
        An abstract method that validates the value of an ingredient.

        :param value: The value to validate.
        :raises TypeError: If the value is not of the correct type.
        :raises ValueError: If the value is not within
            the allowed range or options.
        """
        raise NotImplementedError

    def __set_name__(
            self,
            owner: type[BurgerRecipe],
            name: str
    ) -> None:
        """
        Set the name of the protected attribute.

        :param owner: The owner class.
        :param name: The name of the attribute.
        """
        self.protected_name = "_" + name

    def __get__(
            self,
            instance: BurgerRecipe,
            owner: type[BurgerRecipe]
    ) -> int | str:
        """
        Get the value of the protected attribute.

        :param instance: The instance of the class.
        :param owner: The owner class.
        :return: The value of the protected attribute.
        """
        return getattr(instance, self.protected_name)

    def __set__(
            self,
            instance: BurgerRecipe,
            value: int | str
    ) -> None:
        """
        Set the value of the protected attribute after validation.

        :param instance: The instance of the class.
        :param value: The value to set.
        """
        self.validate(value)
        setattr(instance, self.protected_name, value)


class Number(Validator):
    """A validator for numeric ingredients."""

    def __init__(self, min_value: int, max_value: int) -> None:
        """
        Initialize the validator.

        :param min_value: The minimum allowed value.
        :param max_value: The maximum allowed value.
        """
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: int) -> None:
        """
        Validate the value of a numeric ingredient.

        :param value: The value to validate.
        :raises TypeError: If the value is not an integer.
        :raises ValueError: If the value is not within the allowed range.
        """
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not self.min_value <= value <= self.max_value:
            raise ValueError(
                f"Quantity should not be less than {self.min_value} "
                f"and greater than {self.max_value}."
            )


class OneOf(Validator):
    """A validator for ingredients with a limited set of options."""

    def __init__(self, *options: str) -> None:
        """
        Initialize the validator.

        :param options: The allowed options.
        """
        self.options = options

    def validate(self, value: str) -> None:
        """
        Validate the value of a string ingredient.

        :param value: The value to validate.
        :raises ValueError: If the value is not one of the allowed options.
        """
        if value not in self.options:
            raise ValueError(
                f"Expected {value} to be one of {self.options}."
            )


class BurgerRecipe:
    """A burger recipe."""

    buns: Number = Number(2, 3)
    cheese: Number = Number(0, 2)
    tomatoes: Number = Number(0, 3)
    cutlets: Number = Number(1, 3)
    eggs: Number = Number(0, 2)
    sauce: OneOf = OneOf("ketchup", "mayo", "burger")

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
        Initialize the burger recipe.

        :param buns: The number of buns.
        :param cheese: The number of cheese slices.
        :param tomatoes: The number of tomato slices.
        :param cutlets: The number of cutlets.
        :param eggs: The number of eggs.
        :param sauce: The type of sauce.
        """
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce
