from cerberus import Validator
from ..error_handling.validation_error import ValidationError

def validate_search_query_params(query_params):
    schema = {
        "name_product": {"type": "string", "required": True, "empty": False}
    }
    validator = Validator(schema)
    is_valid = validator.validate(query_params)

    if not is_valid:
        raise ValidationError({"message": "Invalid request body", "errors": validator.errors})

    return is_valid, validator.errors
