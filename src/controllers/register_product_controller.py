from ..error_handling.validation_error_controller import ValidationErrorController
from .interface.register_product_interface import RegisterProductControllerInterface

class RegisterProductController(RegisterProductControllerInterface):
    def __init__(self, model) -> None:
        self.db_repository = model
        
    
    def register_product_controller(self, name_product: str, type_product: str, quantity_product: int):
        ValidationErrorController.validate_products_fields(name_product, type_product, quantity_product)
    
        product = {
            'name_product': name_product,
            'type_product': type_product,
            'quantity_product': quantity_product
        }

        return self.db_repository.insert_product(product['name_product'], product['type_product'], product['quantity_product'])
