import functools
from organizations import\
    OrganizationsException,\
    InvalidInputException,\
    AbsentResourceException,\
    UnavailableException
from .exceptions import\
    BadRequestException,\
    NotFoundException,\
    TooManyRequestsException,\
    ServiceUnavailableException


def handle_organizations_exceptions(fun):
    @functools.wraps(fun)
    def func(*args, **kwargs):
        try:
            return fun(*args, **kwargs)
        except InvalidInputException as ex:
            raise BadRequestException(ex)
        except AbsentResourceException:
            raise NotFoundException()
        except UnavailableException:
            raise TooManyRequestsException()
        except OrganizationsException:
            raise ServiceUnavailableException()
    return func


class Controller():
    def __init__(self, app):
        self._service = app['organizations']

    @handle_organizations_exceptions
    def list_organizations(self, start):
        result = self._service.list(start)
        return result['data'], result['meta']

    @handle_organizations_exceptions
    def get_organizations(self, id):
        result = self._service.get(id)
        return result

    @handle_organizations_exceptions
    def create_organizations(self, details):
        result = self._service.create(details)
        return result

    @handle_organizations_exceptions
    def update_organizations(self, id, details):
        result = self._service.update(id, details)
        return result

    @handle_organizations_exceptions
    def delete_organizations(self, id):
        self._service.delete(id)

    @handle_organizations_exceptions
    def search_organizations(self, query, user_lat, user_lng, start):
        result = self._service.search(query, user_lat, user_lng, start)
        return result['data'], result['meta']
