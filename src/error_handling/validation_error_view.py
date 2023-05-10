import traceback
from src.error_handling.validation_error import ValidationError

# Definindoo a classe de exeção personalizada ViewError
class ViewError(Exception):
    # Construtor da classe ViewError
    def __init__(self, message, errors=None) -> None:
        # Chamando o construtor da classe pai Exception com a mensagem
        super().__init__(message)
        self.message = message
        self.errors = errors
        self.error_type = 'View Error'
    
    # Método estático para lidar com diferentes tipos de erros
    @staticmethod
    def handler_error(error, error_type=None): # manipulador de erros
        # Obtendo a mensagem de erro e o rastreamento de pilha
        error_message = str(error)
        error_traceback = traceback.format_exc()
    
    # Verificiando se o erro é uma instancia de ValidationError e tratando
        if isinstance(error, ValidationError):
            print("Handler my custom error")
            return {
                "status_code": 400,
                "error_message": error_message,
                "traceback": error_traceback
            }
    # Verificando se o erro é uma instancia de ZeroDivisionError e tratando
        if isinstance(error, ZeroDivisionError):
            print("Treat division by zero")
            return {
                "status_code": 400,
                "data": "Division by zero is not allowed",
                "error_message": error_message,
                "traceback": error_traceback
            }
    # Tratando outros tipos de erros genéricos
        else:
            if error_type == "register":
                error_msg = "Ocorreu um erro ao registrar o produto."
            elif error_type == "attack":
                error_msg = "Ocorreu um erro ao registrar os produtos"
            else:
                error_msg = "An unknown error occurred"
        
        print(f"Error: {error_message}")
        return {
            "status_code": 500,
            "data": {"error": error_msg},
            "error_message": error_message,
            "traceback": error_traceback
        }