import pytest
from ..controllers.register_product_controller import RegisterProductController
from ..error_handling.validation_error import ControllerError

class MockModel:
    def __init__(self) -> None:
        self.insert_product_attributes = []
        self.insert_products = []

    def insert_product(self, product):
        self.insert_product_attributes.append(product)
        self.insert_products.append(product)
        return True

class InvalidModel:
    pass

def test_register_product_controller_varying_values():
    model = MockModel()
    register_product_controller = RegisterProductController(model)
    response = register_product_controller.register_product_controller("Produto1", "Tipo1", 10)
    
    assert model.insert_product_attributes[0] == {"name_product": "Produto1", "type_product": "Tipo1", "quantity_product": 10}
    assert response == True

def test_register_product_controller_empty_inputs():
    model = MockModel()
    register_product_controller = RegisterProductController(model)
    with pytest.raises(ControllerError) as exc_info:
        register_product_controller.register_product_controller('', '', '')
    assert str(exc_info.value) == "Error: Invalid input. Name cannot be empty."

def test_register_product_controller_invalid_model():
    model = InvalidModel()
    register_product_controller = RegisterProductController(model)
    
    with pytest.raises(AttributeError):
        response = register_product_controller.register_product_controller("Produto1", "Tipo1", 10)
        print()
        print(response)
        assert response == 'Error: Not found'

def test_register_product_controller_invalid_inputs():
    model = MockModel()
    register_product_controller = RegisterProductController(model)
    with pytest.raises(ControllerError) as exc_info:
        register_product_controller.register_product_controller('!@#$', '!@#$', '!@#$')
    assert str(exc_info.value) == 'Error: Invalid input(s). Quantity must be a valid integer.'

def test_register_product_controller_case_insensitive_inputs():
    model = MockModel()
    register_product_controller = RegisterProductController(model)
    
    try:
        response_upper = register_product_controller.register_product_controller("PRODUTO1", "TIPO1", 10)
        response_lower = register_product_controller.register_product_controller("produto1", "tipo1", 10)
        response_mixed = register_product_controller.register_product_controller("PrOdUtO1", "TiPo1", 10)
    except ControllerError:
        pytest.fail("ControllerError raised unexpectedly")
    
    assert model.insert_product_attributes[0] == {"name_product": "PRODUTO1", "type_product": "TIPO1", "quantity_product": 10}
    assert response_upper == True
    
    assert model.insert_product_attributes[1] == {"name_product": "produto1", "type_product": "tipo1", "quantity_product": 10}
    assert response_lower == True
    
    assert model.insert_product_attributes[2] == {"name_product": "PrOdUtO1", "type_product": "TiPo1", "quantity_product": 10}
    assert response_mixed == True
