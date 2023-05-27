from abc import ABC, abstractmethod

class SearchProductControllerInterface(ABC):
    @abstractmethod
    def search_product(self, name_product: str):
        pass