from src.infra.configs.connection import DBConnectionHandler
from src.infra.repository.products_repository import ProductsRepository

# Instancia o objeto DBConnectionHandler
db_hanlde = DBConnectionHandler()

# Conecta ao banco de dados
db_hanlde.connect_to_db()

# Obtém a conexão com o banco de dados
db_connection = db_hanlde.get_db_connection()

# Verificando se a conexão foi estabelecida
if db_connection is not None:
    print("Conexão com o banco de dados estabelecida com sucesso!")
else:
    print("Falha ao estabelecer conexão com o banco de dados.")

# Instancia a classe ProductsRepository com a conexão db_connection
products_repository = ProductsRepository(db_connection)

# Realiza a inserção de dados
name_product = "Torta de Limão"
type_product = "Doce"
quantify_product = 2

response = products_repository.insert_product(name_product, type_product, quantify_product)
print(response)


# Realiza uma consulta com filtro
filter = {"type_product": "Doce"}
response = products_repository.select_many(filter)
print(response)

# Realiza uma consulta retornando apenas um documento
filter = {"name_product": "Torta de Morango"}
response = products_repository.select_one(filter)
print(response)

# Realiza uma consulta com ordenação 
products_repository.select_many_order()

# Realiza uma consulta buscando por um documento específico pelo ID
products_repository.select_by_object_id()

# Realiza uma busca de produto por nome
name_product = "Torta de Frango"
response = products_repository.search_product(name_product)
print(response)

# Deleta um produto por nome
name_product = "Torta de Limão"
result = products_repository.delete_product(name_product)
print(result)
