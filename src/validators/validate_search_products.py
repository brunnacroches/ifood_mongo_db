from cerberus import Validator
from src.error_handling.validation_error import ValidationError

def validate_search_query_params(query_params):
    schema = {
        "name_product": {"type": "string", "required": True}
    }
    validator = Validator(schema)
    is_valid = validator.validate(query_params)
    
    if not is_valid:
        raise ValidationError({"message": "Invalid request body", "erros": validator.errors})
    
    return {
        "is_valid": is_valid,
        "error": validator.errors
    }