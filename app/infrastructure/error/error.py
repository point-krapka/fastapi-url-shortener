class AppError(Exception):
    def __init__(self, message: str, reason: str = None):
        self.message = message
        self.reason = reason
        super().__init__(message)

class NotFoundError(AppError):
    pass

class AlreadyExistsError(AppError):
    pass

class IncorrectPassword(AppError):
    pass

