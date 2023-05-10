from src.infra.repository.products_repository import ProductsRepository
from src.controllers.register_product_controller import  RegisterProductController
from src.views.register_product_view import RegisterProductsViews
from src.infra.configs.connection import DBConnectionHandler

def register_product_composer():
    model = ProductsRepository(DBConnectionHandler)
    controller = RegisterProductController(model)
    view = RegisterProductsViews(controller)
    
    return view