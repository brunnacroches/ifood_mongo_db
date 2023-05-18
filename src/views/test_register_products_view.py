import pytest
from unittest.mock import MagicMock
from .register_product_view import RegisterProductsViews
from ..error_handling.validation_error import ValidationError


class MockController:
    def __init__(self, error=False) -> None:
        self.register_product_controller_attributes = []
        self.error = error

    def register_product_controller(self, name_product, type_product, quantity_product):
        if self.error:
            raise Exception("Erro na camada do controlador")
        else:
            print("register_product_controller foi chamado")
            self.register_product_controller_attributes.append((name_product, type_product, quantity_product))

# testar se o produto registrado é valido
def test_register_product_view_valid():
    controller = MockController()
    test_register_product_view = RegisterProductsViews(controller)
    request = MagicMock()
    request.json = {
        "name_product": "Product 1",
        "type_product": "Type 1",
        "quantity_product": 10
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
        "quantity_product": 10
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
        "quantity_product": ""
    }
    try:
        response = register_product_view.register_products_view(request)
    except ValidationError as e:
        assert str(e) == "{'message': 'Invalid request body', 'errors': {'quantity_product': ['must be of integer type']}}"

# Teste para verificar se os campos têm o tipo errado
def test_register_product_view_invalid_type():
    controller = MockController()
    register_product_view = RegisterProductsViews(controller)
    request = MagicMock()
    request.json = {
        "name_product": 123,  # valor inválido para name_product
        "type_product": "Type 1",
        "quantity_product": 10
    }
    try:
        response = register_product_view.register_products_view(request)
    except ValidationError as e:
        assert str(e) == "{'message': 'Invalid request body', 'errors': {'name_product': ['must be of string type']}}"

# testar quando o valor dos campos nao e valido
def test_register_product_view_invalid_value():
    controller = MockController()
    register_product_view = RegisterProductsViews(controller)
    request = MagicMock()
    request.json = {
        "name_product": "Product 1",
        "type_product": "Type 1",
        "quantity_product": -10  # valor inválido para quantity_product
    }
    try:
        response = register_product_view.register_products_view(request)
    except ValidationError as e:
        assert str(e) == "{'message': 'Invalid request body', 'errors': {'quantity_product': ['must be greater than or equal to 0']}}"

# testar quando ocorre um erro na camada do controlador
def test_register_product_view_controller_error():
    controller = MockController(error=True)
    register_product_view = RegisterProductsViews(controller)
    request = MagicMock()
    request.json = {
        "name_product": "Product 1",
        "type_product": "Type 1",
        "quantity_product": 10
    }
    response = register_product_view.register_products_view(request)

    assert response["status_code"] == 500
    assert response["error_message"] == "Erro na camada do controlador"