from bson.objectid import ObjectId
from typing import Dict, List

# tratamento dos dados
class ProductsRepository:
    def __init__(self, db_connection) -> None:
        self.__collection_name = 'productsRepository'
        self.__db_connection = db_connection

    # funcionalidade de inserção 
    def insert_product(self, product: Dict) -> Dict:
        collection = self.__db_connection.get_collection(self.__collection_name)
        collection.insert_one(product)
        return product

    def insert_list_of_product(self, list_of_product: List[Dict]) -> List[Dict]:
        # pegar a conexao com a collection
        collection = self.__db_connection.get_collection(self.__collection_name)
        # coloque varios
        collection.insert_many(list_of_product)
        return list_of_product

    def select_many(self, filter) -> List[Dict]:
        # pegar a conexao com a collection
        collection = self.__db_connection.get_collection(self.__collection_name)
        data = collection.find(
            filter, # filtro
            {"address": 0, "_id": 0 } # Opções de retorno
            )

        response = []
        for elem in data: response.append(elem)

        return response

    def select_one(self, filter) -> Dict:
        collection = self.__db_connection.get_collection(self.__collection_name)
        response = collection.find_one(filter, {"_id": 0})
        return response
    
    def select_if_property_exists(self) -> None:
        collection = self.__db_connection.get_collection(self.__collection_name)
        data = collection.find({"cpf": {"$exists": True }})
        for elem in data: print(elem)
    
    # fazer a ordenacao
    def select_many_order(self):
        collection = self.__db_connection.get_collection(self.__collection_name)
        data = collection.find(
            {"name": "Brunna"}, # filtro
            {"address": 0, "_id": 0 } # Opções de retorno
        ).sort([("request.pizza", 1)])

        for elem in data: print(elem)

    def select_or(self) -> None:
        collection = self.__db_connection.get_collection(self.__collection_name)
        data = collection.find({"$or": [{"name": "Brunna"}, {"ola": {"$exists": True} }] })
        for elem in data: print(elem)
        print(elem)
        print()
    
    # filtro de busca usando o ID do pedido
    def select_by_object_id(self) -> None:
        collection = self.__db_connection.get_collection(self.__collection_name)
        data = collection.find({"_id": ObjectId("645539491c730625e1d8949c")})
        for elem in data: print(elem)

    def search_product(self, name_product: str) -> Dict:
        # Acessa a coleção
        collection = self.__db_connection.get_collection(self.__collection_name)
        
        # Busca o produto com base no nome
        product = collection.find_one({"name_product": name_product})
        
        # Retorna o produto encontrado
        return product