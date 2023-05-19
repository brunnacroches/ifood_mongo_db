from ..error_handling.validation_error_controller import ValidationErrorController

class SearchProductController:
    def __init__(self, model) -> None:
        self.db_repository = model
    
    def search_product(self, name_product: str):
        ValidationErrorController.validate_product_name(name_product)
        
        return self.db_repository.search_product(name_product)
