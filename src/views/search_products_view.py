from src.validators.validate_search_products import validate_search_query_params
from src.error_handling.validation_error_view import ViewError

class SearchProductViews:
    def __init__(self, controller) -> None:
        self.__controller = controller
    
# Metodo para tratar a aquisição da rota e retornar a resposta da pesquisa
    def search_product_view(self, request_args):
        try:
            # Converte os argumentos da requisição em um dicionário
            query_params = dict(request_args)
            
            # Valida os parâmetros de consulta recebidos
            validate_search_query_params(query_params)
            
            # Obtém os nomes a partir dos parâmetros de consulta
            search_product = request_args.get("name_product")
            
            # Retorna a lista de produtos encontrados
            filtered_products = self.__controller.search_product_controller(search_product)
            
            # Verifica se a lista de produtos está vazia
            if not filtered_products:
                return {
                    "status_code": 404,
                    "error_message": "Product not found",
                    "success": False
                }
            
            # Verifica se a resposta do controlador é uma lista (como esperado)
            if not isinstance(filtered_products, list):
                raise Exception("Unexpected response from controller")

            return {
                "status_code": 200,
                "data": filtered_products,
                "success": True
            }
        except Exception as exception:
            response = ViewError.handler_error(exception, error_type="search")
            return response
