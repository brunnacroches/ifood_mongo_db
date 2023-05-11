from typing import Optional
import re
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
    def validate_values_are_not_null(*values):
        return all(value is not None for value in values)
    
    @staticmethod
    def validate_names_not_found(*names):
        return all(name is not None for name in names)
    
    @staticmethod
    def validate_product_name(name_product: str):
        if not ValidationErrorController.validate_input_is_not_empty(name_product):
            raise ControllerError("Error: Invalid input. Name cannot be empty.")
        # if not ValidationErrorController.validate_no_spaces_in_inputs(name_product):
        #     raise ControllerError("Error: Invalid input. Name cannot contain spaces.")

    @staticmethod
    def validate_products_fields(name_product: str, type_product: str, quantity_product: int):
        ValidationErrorController.validate_product_name(name_product)
        if not ValidationErrorController.validate_input_is_not_empty(type_product):
            raise ControllerError("Error: Invalid input(s). Type cannot be empty.")
        if not ValidationErrorController.validate_values_are_not_null(quantity_product):
            raise ControllerError("Error: Invalid input(s). Quantity cannot be null.")
        try:
            int(quantity_product)
        except ValueError:
            raise ControllerError("Error: Invalid input(s). Quantity must be a valid integer.")

    @staticmethod
    def validate_input_is_alphanumeric(*inputs):
        pattern = re.compile('^[a-zA-Z0-9]+$')
        return all(bool(pattern.match(input)) for input in inputs)