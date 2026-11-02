from abc import ABC, abstractmethod


class Validator(ABC):
    def __set_name__(
        self,
        owner: type,
        name: str,
    ) -> None:
        self.protected_name = f"_{name}"

    def __get__(
        self,
        instance,
        owner: type,
    ):
        return getattr(instance, self.protected_name)

    def __set__(
        self,
        instance,
        value,
    ) -> None:
        self.validate(value)
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value) -> None:
        pass
