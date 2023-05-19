import pytest
from unittest.mock import MagicMock
from .search_products_view import SearchProductViews

# criar a classe Mock
class MockController:
    def __init__(self, error=False) -> None:
        self.search_product_controller_attributes = []
        self.error = error
    
    def search_product_controller(self, name_product):
        if self.error:
            raise Exception("Erro na camada do controlador")
        else:
            print("search_product_controller foi chamado")
            self.search_product_controller_attributes.append(name_product)
            return [{"id": 1, "name_product": name_product}]

# Testar se o produto procurado é valido
def test_search_product_view_valid():
    controller = MockController()
    search_product_view = SearchProductViews(controller)
    request = MagicMock()
    request.args = {"name_product": "Product 1"}
    
    response = search_product_view.search_product_view(request.args)
    
    print("Controller attributes:", controller.search_product_controller_attributes)
    assert controller.search_product_controller_attributes[0] == 'Product 1'
    assert response["status_code"] == 200
    assert response["data"] == [{"id": 1, "name_product": "Product 1"}]
    assert response["success"] == True

# Testar quando ocorre um erro na camada do controlador
def test_search_product_view_validation_error():
    controller = MockController()
    search_product_view = SearchProductViews(controller)
    request = MagicMock()
    request.args = {"name_product": ""}  # valor inválido para name_product

    response = search_product_view.search_product_view(request.args)

    assert response["status_code"] == 400
    assert "Invalid request body" in response["error_message"]

# Testar quando o produto não é encontrado
def test_search_product_view_product_not_found():
    controller = MockController()
    controller.search_product_controller = MagicMock(return_value=[])  # Retornar uma lista vazia
    search_product_view = SearchProductViews(controller)
    request = MagicMock()
    request.args = {"name_product": "Product 1"}
    
    response = search_product_view.search_product_view(request.args)
    
    assert response["status_code"] == 404
    assert response["error_message"] == "Product not found"

# Testar quando o parâmetro de consulta name_product está ausente
def test_search_product_missing_name_product():
    controller = MockController()
    search_product_view = SearchProductViews(controller)
    request = MagicMock()
    request.args = {}
    
    response = search_product_view.search_product_view(request.args)
    
    assert response["status_code"] == 400
    assert "name_product" in response["error_message"]

# Testar quando o parâmetro de consulta name_product é nulo
def test_search_product_view_null_name_product():
    controller = MockController()
    search_product_view = SearchProductViews(controller)
    request = MagicMock()
    request.args = {"name_product": None} # name_product é nulo

    response = search_product_view.search_product_view(request.args)

    assert response["status_code"] == 400
    assert "name_product" in response["error_message"]

# Testar quando a requisição inclui parâmetros de consulta adicionais: Você pode adicionar um teste onde a requisição inclui parâmetros de consulta além de name_product
def test_search_product_view_extra_query_params():
    controller = MockController()
    search_product_view = SearchProductViews(controller)
    request = MagicMock()
    request.args = {"name_product": "Product 1", "extra_param": "extra"}  # Parâmetro de consulta extra

    response = search_product_view.search_product_view(request.args)

    assert response["status_code"] == 400
    assert "extra_param" in response["error_message"]

# Testar quando o controlador retorna uma resposta inesperada
def test_search_product_view_unexpected_controller_response():
    controller = MockController()
    controller.search_product_controller = MagicMock(return_value="unexpected")  # Retornar uma resposta inesperada
    search_product_view = SearchProductViews(controller)
    request = MagicMock()
    request.args = {"name_product": "Product 1"}
    
    response = search_product_view.search_product_view(request.args)
    
    assert response["status_code"] == 500
    assert "Unexpected response from controller" in response["error_message"]
