from typing import Optional
from src.error_handling.validation_error import ControllerError

class ValidationErrorController(Exception):
    def __init__(self, message, errors=None) -> None:
        super().__init__(message)
        self.message = message
        self.errors = errors
        self.error_type = 'Controller Error'
    
    @staticmethod
    def validate_input_is_not_empty(*inputs):
        return all(len(input) > 0 for input in inputs)
    
    @staticmethod
    def validate_no_spaces_in_inputs(*inputs):
        return all(' ' not in input for input in inputs)
    
    @staticmethod
    def validate_values_are_not_null(*values):
        return all(value is not None for value in values)
    
    @staticmethod
    def validate_names_not_found(*names):
        return all(name is not None for name in names)
    
    @staticmethod
    def validate_products_fileds(name_product: str, type_product: str, quantify_product: int):
        if not ValidationErrorController.validate_input_is_not_empty(name_product, type_product) or not ValidationErrorController.validate_no_spaces_in_inputs(name_product, type_product, quantify_product):
            raise ControllerError("Error: Invalid inputs(s)")
        if not ValidationErrorController.validate_values_are_not_null(quantify_product):
            raise ControllerError("Error: Quantify product not found")
        try:
            int(quantify_product)
        except ValueError:
            raise ControllerError("Error: Not found")
