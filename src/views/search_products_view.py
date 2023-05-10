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
            
            # Retorna a resposta bem-sucecida da pesquisa
            return {
                "status_code": 200,
                "data": search_product,
                "success": True
            }
        except Exception as exception:
            response = ViewError.handler_error(exception, error_type="search")
            return response