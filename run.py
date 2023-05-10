from src.infra.configs.connection import DBConnectionHandler
from src.infra.repository.products_repository import ProductsRepository

# instancia o objeto
db_hanlde = DBConnectionHandler()
# conecta
db_hanlde.connect_to_db()
# pega a conexao 
db_connection = db_hanlde.get_db_connection()

# instacia da classe ProductsRepository com a instancia db_connection dentro dela
products_repository = ProductsRepository(db_connection)

response = products_repository.select_many({"name": "Brunna", "request.pizza": 10})
# print(response)
print()

response2 = products_repository.select_many({"name": "Brunna"})

products_repository.select_by_object_id()


