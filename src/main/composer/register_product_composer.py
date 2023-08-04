from src.infra.repository.products_repository import ProductsRepository
from src.controllers.register_product_controller import  RegisterProductController
from src.views.register_product_view import RegisterProductsViews
from src.infra.configs.connection import DBConnectionHandler



def register_product_composer():
    db_connection = DBConnectionHandler()
    db_connection.connect_to_db()       
    model = ProductsRepository(db_connection.get_db_connection())
    controller = RegisterProductController(model)
    view = RegisterProductsViews(controller)
    
    return view

# O problema:
#    na linha onde estava criando a instância da classe ProductsRepository 
# no arquivo register_product_composer.py. 
#   O erro indicava que estava passando DBConnectionHandler como argumento para 
#   o construtor ProductsRepository, mas está faltando o argumento obrigatório
#   db_connection.

# Corrigi a instância de DBConnectionHandler e passandei para ProductsRepository. 
# Certificando de chamar o método get_db_connection() em DBConnectionHandler 
# para obter a conexão com o banco de dados antes de passá-la como argumento 
# para ProductsRepository.

# ! def register_product_composer():
# !     model = ProductsRepository(DBConnectionHandler)
# !     controller = RegisterProductController(model)
# !     view = RegisterProductsViews(controller)
#  !   
# !     return view
