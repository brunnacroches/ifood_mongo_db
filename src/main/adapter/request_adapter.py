from flask import request as FlaskRequest
from src.main.http_types.http_request import HttpRequest
from src.main.http_types.http_response import HttpResponse
from src.views.interface.view import ViewInterface

def request_adapter(request: FlaskRequest, view: ViewInterface) -> HttpResponse:
    http_request = HttpRequest(
        header=request.headers,
        body=request.json,
        query_params=dict(request.args),
        path_params=request.view_args,
        url=request.full_path,
        ipv4=request.remote_addr,
    )
    
    http_response = view.execute(http_request)
    return http_response
