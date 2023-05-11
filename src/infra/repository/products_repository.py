from bson.objectid import ObjectId
from typing import Dict, List

# tratamento dos dados
class ProductsRepository:
    def __init__(self, db_connection) -> None:
        self.__collection_name = 'productsRepository'
        self.__db_connection = db_connection

    # funcionalidade de inserção 
    def insert_product(self, name_product: str, type_product: str, quantify_product: int) -> Dict:
        product = {
            'name_product': name_product,
            'type_product': type_product,
            'quantify_product': quantify_product
        }
        collection = self.__db_connection.get_collection(self.__collection_name)
        collection.insert_one(product)
        return product

    def insert_list_of_product(self, list_of_product: List[Dict]) -> List[Dict]:
        # Obter a conexão com a coleção
        collection = self.__db_connection.get_collection(self.__collection_name)
        # Inserir vários produtos na coleção
        result = collection.insert_many(list_of_product)
        # Verificar se a inserção foi bem-sucedida
        if result.acknowledged:
            return list_of_product
        else:
            return []

    def select_many(self, filter) -> List[Dict]:
        # Obter a conexão com a coleção
        collection = self.__db_connection.get_collection(self.__collection_name)
        # Realizar a consulta na coleção
        data = collection.find(
            filter, # filtro
            {"_id": 0}  # Opções de retorno
        )

        # Retornar os resultados da consulta
        return list(data)

    def select_one(self, filter) -> Dict:
        collection = self.__db_connection.get_collection(self.__collection_name)
        response = collection.find_one(filter, {"_id": 0})
        return response
    
    def select_if_property_exists(self) -> None:
        collection = self.__db_connection.get_collection(self.__collection_name)
        data = collection.find({"name_product": {"$exists": True }})
        for elem in data: print(elem)
   
    def select_many_order(self):
        collection = self.__db_connection.get_collection(self.__collection_name)
        data = collection.find(
            {"name_product": "Torta Salgada"}, # filtro
            {"_id": 0} # Opções de retorno
        ).sort([("quantity_product", 1)])

        for elem in data: print(elem)

    def select_or(self) -> None:
        collection = self.__db_connection.get_collection(self.__collection_name)
        data = collection.find({"$or": [{"name_product": "Torta Doce"}, {"type_product": {"$exists": True} }] })
        for elem in data:
            print(elem)
    
    # filtro de busca usando o ID do pedido
    def select_by_object_id(self) -> None:
        collection = self.__db_connection.get_collection(self.__collection_name)
        data = collection.find({"_id": ObjectId("645d110500a56265a0c18fe8")})
        for elem in data: 
            print(elem)

    def search_product(self, name_product: str) -> Dict:
        # Acessa a coleção
        collection = self.__db_connection.get_collection(self.__collection_name)
        
        # Busca o produto com base no nome
        product = collection.find_one({"name_product": name_product})
        
        # Retorna o produto encontrado
        return product
    
    def delete_product(self, name_product: str) -> bool:
        collection = self.__db_connection.get_collection(self.__collection_name)
        result = collection.delete_one({"name_product": name_product})
        return result.deleted_count > 0
