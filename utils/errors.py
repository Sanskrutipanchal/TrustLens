class TrustLensError(Exception):
    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class InvalidInputError(TrustLensError):
    def __init__(self, message: str) -> None:
        super().__init__(message, status_code=400)


class FileProcessingError(TrustLensError):
    def __init__(self, message: str = "Could not process the uploaded file.") -> None:
        super().__init__(message, status_code=422)
