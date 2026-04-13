from abc import abstractmethod

class Validator():

    def __set_name__(self, instance, method_name: str):
        self.protected_name = '_' + method_name

    def __get__(self, instance, objtype=None) -> int | str:
        value = getattr(instance, self.protected_name)
        return value

    def __set__(self, instance, value) -> None:
        setattr(instance, self.protected_name, value)

    @abstractmethod
    def validate(self):
        pass

class Number(Validator):
    def __init__(self, max_value: int, min_value: int) -> None:
        self.max_value = max_value
        self.min_value = min_value





class OneOf(Validator):


    def __init__(self,option: str) -> None:
        self.option = option



class BurgerRecipe:
    def __init__(
            self,
            buns: int,
            cheese: int,
            tomatoes: int,
            cutlets: int,
            eggs: int,
            sauce: str
    ) -> None:
        pass
