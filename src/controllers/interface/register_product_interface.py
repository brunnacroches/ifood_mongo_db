
from abc import ABC, abstractmethod

class RegisterProductControllerInterface(ABC):
    @abstractmethod
    def register_product_controller(self, name_product: str, type_product: str, quantity_product: int):
        pass
