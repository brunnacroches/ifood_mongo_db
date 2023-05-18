from src.validators.validate_register_products import validate_register_products_request_body
from src.error_handling.validation_error_view import ViewError
from src.views.interface.view import ViewInterface
from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse

class RegisterProductsViews(ViewInterface):
    def __init__(self, controller, input:HttpResponse) -> HttpRequest:
        self.__controller = controller
    
    def register_order_view(self, input):
        try:
            validate_register_products_request_body(input.json)
            
            body = input.json
            name_product = body["name_product"]
            type_product = body["type_product"]
            quantity_product = body["quantity_product"]

            # chama o controller para criar o registro
            self.__controller.register_product_controller(name_product, type_product, quantity_product)
            
            return {
                "status_code": 200,
                "data": {
                    "name_product": name_product,
                    "type_product": type_product,
                    "quantity_product": quantity_product
                },
                "success": True
            }

        except Exception as exception:
            # Envia a exceção para a função de tratamento de erros
            response = ViewError.handler_error(exception, error_type="register")
            return response
    