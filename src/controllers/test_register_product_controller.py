import pytest
from src.controllers.register_product_controller import RegisterProductController
from src.error_handling.validation_error_controller import ValidationErrorController


class MockModel:
    def __init__(self) -> None:
        self.insert_product_calls = []

    def insert_product(self, product):
        self.insert_product_calls.append(product)
        return True


def test_register_product_controller_valid_input():
    model = MockModel()
    register_product_controller = RegisterProductController(model)

    name_product = "Torta de Maçã"
    type_product = "Doce"
    quantity_product = 5

    result = register_product_controller.register_product_controller(
        name_product, type_product, quantity_product
    )

    assert len(model.insert_product_calls) == 1
    assert model.insert_product_calls[0] == {
        'name_product': name_product,
        'type_product': type_product,
        'quantity_product': quantity_product
    }
    assert result is True


# def test_register_product_controller_invalid_input():
#     model = MockModel()
#     register_product_controller = RegisterProductController(model)

#     name_product = ""
#     type_product = "Doce"
#     quantity_product = 5

#     with pytest.raises(Exception):
#         register_product_controller.register_product_controller(
#             name_product, type_product, quantity_product
#         )

#     assert len(model.insert_product_calls) == 0
