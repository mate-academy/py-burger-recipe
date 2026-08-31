from abc import abstractmethod, ABC
from symtable import Class


class Validator(ABC):
    def __set_name__(self, owner: Class, name: str) -> None:
        self.protected_name = "_" + name

    def __get__(self, instance: int, owner: Class) -> None:
        return getattr(instance, self.protected_name)

    def __set__(self, instance: Class, value: int) -> None:
        self.validate(value)  # только вызов
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self, value: int) -> None:
        pass
