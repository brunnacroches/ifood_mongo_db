from ..error_handling.validation_error_controller import ValidationErrorController
from .interface.controller_interface import ControllerInterface

class SearchProductController(ControllerInterface):
    def __init__(self, model) -> None:
        self.db_repository = model

    def controllerinterface(self, *args, **kwargs):
        pass
    
    def search_product(self, name_product: str):
        ValidationErrorController.validate_product_name(name_product)
        
        return self.db_repository.search_product(name_product)
