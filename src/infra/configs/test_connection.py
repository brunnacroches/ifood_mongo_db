from pymongo import MongoClient

from pymongo.database import Database
from src.infra.configs.connection import DBConnectionHandler

def test_db_connection():
    # Cria uma instância do DBConnectionHandler
    db_handler = DBConnectionHandler()

    # Conecta ao banco de dados
    db_handler.connect_to_db()

    # Obtém a conexão com o banco de dados
    db_connection = db_handler.get_db_connection()

    # Obtém o cliente do banco de dados
    db_client = db_handler.get_db_client()
    
    # Verifica se a conexão e o cliente são instancias válidas
    assert db_connection is not None
    assert isinstance(db_connection, Database)
    assert db_client is not None
    assert isinstance(db_client, MongoClient)

# Verifica se o nome do banco de dados está correto
    assert db_connection.name == "meuBanco"