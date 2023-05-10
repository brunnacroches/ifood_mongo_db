import pytest
from unittest.mock import MagicMock
from src.views.register_product_view import RegisterProductsViews
from src.error_handling.validation_error import ValidationError


class MockController:
    def __init__(self) -> None:
        self.register_product_controller_attributes = []

    def register_product_controller(self, name_product, type_product, quantify_product):
        print("register_product_controller foi chamado")
        self.register_product_controller_attributes.append((name_product, type_product, quantify_product))

# testar se o produto registrado é valido
def test_register_product_view_valid():
    controller = MockController()
    test_register_product_view = RegisterProductsViews(controller)
    request = MagicMock()
    request.json = {
        "name_product": "Product 1",
        "type_product": "Type 1",
        "quantify_product": 10
    }
    try:
        response = test_register_product_view.register_products_view(request)
    except Exception as e:
        print("Uma exceção foi lançada: ", e)

    print("Controller attributes: ", controller.register_product_controller_attributes)

    assert controller.register_product_controller_attributes[0] == ('Product 1', 'Type 1', 10)
    assert response["status_code"] == 200
    assert response["data"] == {
        "name_product": "Product 1",
        "type_product": "Type 1",
        "quantify_product": 10
    }
    assert response["success"] == True
    
# testar se os campos obrigatórios não são fornecidos
def test_register_product_view_missing_fields():
    controller = MockController()
    register_product_view = RegisterProductsViews(controller)
    request = MagicMock()
    request.json = {
        "name_product": "Product 1",
        "type_product": "Type 1",
        "quantify_product": ""
    }
    try:
        response = register_product_view.register_products_view(request)
    except ValidationError as e:
        assert str(e) == "{'message': 'Invalid request body', 'errors': {'quantify_product': ['must be of integer type']}}"

# testar quando os campos tem o tipo errado 

# testar quando o valor dos campos nao e valido
    
# testar quando ocorre um erro na camada do controlador
