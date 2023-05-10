from src.infra.repository.products_repository import ProductsRepository
from src.controllers.search_product_controller import SearchProductController
from src.views.search_products_view import SearchProductViews
from src.infra.configs.connection import DBConnectionHandler

def search_composer():
    model = ProductsRepository(DBConnectionHandler)
    controller = SearchProductController(model)
    view = SearchProductViews(controller)
    
    return view