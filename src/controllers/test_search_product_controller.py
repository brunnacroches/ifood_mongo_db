import pytest
from ..controllers.search_product_controller import SearchProductController
from ..error_handling.validation_error import ControllerError

class MockModel:
    def __init__(self) -> None:
        self.search_product_attributes = []

    def search_product(self, name_product):
        self.search_product_attributes.append(name_product)
        if name_product == "ProdutoExistente":
            return {"name_product": "ProdutoExistente", "type_product": "Tipo1", "quantity_product": 10}
        return None

class InvalidModel:
    pass

def test_search_product_controller_existing_product():
    model = MockModel()
    search_product_controller = SearchProductController(model)
    response = search_product_controller.search_product("ProdutoExistente")
    
    assert model.search_product_attributes[0] == "ProdutoExistente"
    assert response == {"name_product": "ProdutoExistente", "type_product": "Tipo1", "quantity_product": 10}

def test_search_product_controller_non_existing_product():
    model = MockModel()
    search_product_controller = SearchProductController(model)
    response = search_product_controller.search_product("ProdutoInexistente")
    
    assert model.search_product_attributes[0] == "ProdutoInexistente"
    assert response == None

def test_search_product_controller_empty_input():
    model = MockModel()
    search_product_controller = SearchProductController(model)
    with pytest.raises(ControllerError) as exc_info:
        search_product_controller.search_product('')
    assert str(exc_info.value) == "Error: Invalid input. Name cannot be empty."

def test_search_product_controller_invalid_model():
    model = InvalidModel()
    search_product_controller = SearchProductController(model)
    
    with pytest.raises(AttributeError):
        response = search_product_controller.search_product("Produto1")
        print()
        print(response)
        assert response == 'Error: Not found'
