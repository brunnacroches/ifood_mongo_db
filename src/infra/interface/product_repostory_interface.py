from abc import ABC, abstractmethod
from typing import Dict, List

# tratamento dos dados
class ProductsRepository():

    @abstractmethod
    # funcionalidade de inserção 
    def insert_product(self, name_product: str, type_product: str, quantity_product: int) -> Dict:
        pass
    
    @abstractmethod
    def insert_list_of_product(self, list_of_product: List[Dict]) -> List[Dict]: pass
    
    @abstractmethod
    def select_many(self, filter) -> List[Dict]: pass
    
    @abstractmethod
    def select_one(self, filter) -> Dict: pass
    
    @abstractmethod
    def select_if_property_exists(self) -> None: pass
    
    @abstractmethod
    def select_many_order(self): pass
    
    @abstractmethod
    def select_or(self) -> None: pass
    
    @abstractmethod
    # filtro de busca usando o ID do pedido
    def select_by_object_id(self) -> None: pass
    
    @abstractmethod
    def search_product(self, name_product: str) -> Dict: pass
    
    @abstractmethod
    def delete_product(self, name_product: str) -> bool: pass
