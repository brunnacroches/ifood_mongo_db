from cerberus import Validator
from ..error_handling.validation_error import ValidationError

def validate_register_products_request_body(request_body):
    schema = {
        "name_product": {"type": "string", "required": True},
        "type_product": {"type": "string", "required": True},
        "quantity_product": {"type": "integer", "required": True},
    }
    validator = Validator(schema)
    is_valid = validator.validate(request_body)
    
    if not is_valid:
        raise ValidationError({'message': "Invalid request body", "errors":validator.errors})

    return {
        "is_valid": is_valid,
        "error": validator.errors
    }