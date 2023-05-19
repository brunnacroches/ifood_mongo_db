from abc import ABC, abstractmethod
from ...main.http_types.http_request import HttpRequest
from ...main.http_types.http_response import HttpResponse

class ViewInterface(ABC):

    @abstractmethod
    def execute(self, input: HttpRequest) -> HttpResponse: pass
