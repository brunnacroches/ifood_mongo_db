class HttpResponse:
    
    def __init__(self, status_code: int, body: any):
        self.status_code = status_code
        self.body = body
        
    def __repr__(self) -> str:
        return f"HttpResponse (status_code={self.status_code}, body={self.body})"