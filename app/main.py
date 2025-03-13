from abc import ABC, abstractmethod
from typing import Any, Tuple


class Validator(ABC):
    """Базовый класс для всех дескрипторов."""

    def __set_name__(self, owner: Any, name: str) -> None:
        """Метод для установки имени атрибута."""
        self.protected_name = f"_{name}"

    def __get__(self, instance: Any, owner: Any) -> Any:
        """Метод для получения значения атрибута."""
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Any, value: Any) -> None:
        """Метод для установки значения атрибута."""
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: Any) -> None:
        """Абстрактный метод для валидации значения."""
        pass


class Number(Validator):
    """Дескриптор для проверки целых чисел в заданном диапазоне."""

    def __init__(self, min_value: int, max_value: int) -> None:
        self.min_value = min_value
        self.max_value = max_value

    def validate(self, value: Any) -> None:
        """Метод для валидации значения."""
        if not isinstance(value, int):
            raise TypeError("Quantity should be integer.")
        if not (self.min_value <= value <= self.max_value):
            raise ValueError(
                f"Quantity should not be less than {self.min_value} "
                f"and greater than {self.max_value}."
            )


class OneOf(Validator):

    def __init__(self, options: Tuple[Any, ...]) -> None:
        """Инициализация дескриптора с допустимыми вариантами."""
        self.options = options

    def validate(self, value: Any) -> None:
        """Метод для валидации значения."""
        if value not in self.options:
            raise ValueError(f"Expected {value} to be one of {self.options}.")


class BurgerRecipe:
    """Класс для создания рецепта бургера."""

    buns = Number(min_value=2, max_value=3)
    cheese = Number(min_value=0, max_value=2)
    tomatoes = Number(min_value=0, max_value=3)
    cutlets = Number(min_value=1, max_value=3)
    eggs = Number(min_value=0, max_value=2)
    sauce = OneOf(options=("ketchup", "mayo", "burger"))

    def __init__(
        self,
        buns: int,
        cheese: int,
        tomatoes: int,
        cutlets: int,
        eggs: int,
        sauce: str,
    ) -> None:
        """Инициализация рецепта бургера."""
        self.buns = buns
        self.cheese = cheese
        self.tomatoes = tomatoes
        self.cutlets = cutlets
        self.eggs = eggs
        self.sauce = sauce

    def __repr__(self) -> str:
        """Метод для представления объекта в виде строки."""
        return (
            f"BurgerRecipe(buns={self.buns}, cheese={self.cheese}, "
            f"tomatoes={self.tomatoes}, cutlets={self.cutlets}, "
            f"eggs={self.eggs}, sauce='{self.sauce}')"
        )
