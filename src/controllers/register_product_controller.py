from src.error_handling.validation_error_controller import ValidationErrorController

class RegisterProductController:
    def __init__(self, model) -> None:
        self.db_repository = model
    
    def register_product_controller(self, name_product: str, type_product: str, quantify_product: int):
        ValidationErrorController.validate_products_fileds(name_product, type_product, quantify_product)
        
        product = {
            'name_product': name_product,
            'type_product': type_product,
            'quantity_product': quantify_product
        }
        
        
        return self.db_repository.insert_product(product)
    