from pymongo import MongoClient
from .mongo_db_configs import mongo_db_infos

# aqui vai ser o gerente de conexão ao nosso banco de dados
# classe que gerencia todas as conexoes 
class DBConnectionHandler:
    def __init__(self) -> None:
        self.__connection_string = 'mongodb://{}:{}@{}:{}/?authSource=admin'.format(
            mongo_db_infos["USERNAME"],
            mongo_db_infos["PASSWORD"],
            mongo_db_infos["HOST"],
            mongo_db_infos["PORT"],
        )
        # vou indicar que o nome do meu banco de dados vai estar
        # como um atributo na minha classe
        self.__datababase_name = mongo_db_infos["DB_NAME"]
        self.__client = None
        self.__db_connection = None
    # Ao iniciar o objeto da minha classe ele ja vai criar essa conexão
    def connect_to_db(self):
        # fazer metedo para conectar o banco de dados
        self.__client = MongoClient(self.__connection_string)
        self.__db_connection = self.__client[self.__datababase_name]
    
    def get_db_connection(self):
        return self.__db_connection
    
    def get_db_client(self):
        return
