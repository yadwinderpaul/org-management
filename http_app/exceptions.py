class HttpException(Exception):
    pass


class BadRequestException(HttpException):
    def __init__(self, ex):
        super().__init__()
        self.http_code = 400
        self.message = f'Bad request: {str(ex)}'


class NotFoundException(HttpException):
    def __init__(self):
        super().__init__()
        self.http_code = 404
        self.message = 'Resource not found'


class TooManyRequestsException(HttpException):
    def __init__(self):
        super().__init__()
        self.http_code = 429
        self.message = 'Too many requests'


class ServiceUnavailableException(HttpException):
    def __init__(self):
        super().__init__()
        self.http_code = 503
        self.message = 'Service temporarily unavailable'
