from typing import Dict

class HttpRequest:
    
    def __init__(
        self,
        header: Dict = None, #  contém as informações de cabeçalho da solicitação HTTP.
        body: Dict = None, # contém o corpo da solicitação HTTP. 
        query_params: Dict = None, # contém os parâmetros de consulta da solicitação HTTP. 
        path_params: Dict = None, # contém os parâmetros de caminho da solicitação HTTP. 
        url: str = None, # contém a URL para a qual a solicitação HTTP está sendo enviada.
        ipv4: str = None, #  contém o endereço IP do cliente que está fazendo a solicitação.
        token_information: Dict = None #  contém informações sobre um token de autenticação usado na solicitação.
    ):
        self.header = header
        self.body = body
        self.query_params = query_params
        self.path_params = path_params
        self.url = url
        self.ipv4 = ipv4
        self.toke_information = token_information