class ValidationError(Exception):
    def __init__(self, message, errors=None) -> None:
        super().__init__(message)
        self.message = message
        self.errors = errors
        self.error_type = 'This is my mistake'

    class ControllerError(Exception):
        def __init__(self, message, errors=None) -> None:
            super().__init__(message)
            self.message = message
            self.errors = errors
            self.error_tpye = 'Controller Error'
