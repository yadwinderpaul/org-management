class OrganizationsException(Exception):
    def __init__(self, message=None, original=None):
        if message is None:
            if original:
                message = f'OrganizationsException: {str(original)}'
            else:
                message = 'OrganizationsException'
        super().__init__(message)


class InvalidInputException(OrganizationsException):
    pass


class AbsentResourceException(OrganizationsException):
    pass


class UnavailableException(OrganizationsException):
    pass
