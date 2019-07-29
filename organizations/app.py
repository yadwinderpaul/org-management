from cerberus import Validator
from .exceptions import InvalidInputException


class Organizations():
    def __init__(self, app):
        self._logger = app['logger']
        self._adapter = app['organizations_adapter']

    def list(self, start=0):
        self._logger.info('Getting list of organizations')
        orgs = self._adapter.list_organizations(start)
        self._logger.info('Succesfully got organizations')
        return orgs

    def get(self, id):
        org = self._adapter.get_organization(id)
        return org

    def create(self, details):
        schema = {
            'name': {'type': 'string', 'required': True},
            'url': {'type': 'string', 'required': True},
            'address': {'type': 'string', 'required': True},
            'lat': {'type': 'float', 'required': True},
            'lng': {'type': 'float', 'required': True},
        }
        self._validate(schema, details)
        self._logger.info(f'Creating a new organization: {details}')
        org = self._adapter.create_organizations(details)
        self._logger.info(f'Succesfully created organization: {org["id"]}')
        return org

    def update(self, id, details):
        schema = {
            'name': {'type': 'string', 'required': True},
            'url': {'type': 'string'},
            'address': {'type': 'string'},
            'lat': {'type': 'float'},
            'lng': {'type': 'float'},
        }
        self._validate(schema, details)
        self._logger.info(f'Updating organization: {details}')
        org = self._adapter.update_organizations(id, details)
        self._logger.info('Succesfully updated organization')
        return org

    def delete(self, id):
        self._logger.info(f'Deleting organization: {id}')
        self._adapter.delete_organizations(id)
        self._logger.info('Succesfully deleted organization')
        return True

    def search(self, query, user_lat=None, user_lng=None, start=0):
        if not query:
            raise InvalidInputException(message='"query": is required')
        if user_lat:
            user_lat = float(user_lat)
        if user_lng:
            user_lng = float(user_lng)
        self._logger.info(f'Searching organization: {query}')
        orgs = self._adapter.search_organizations(query,
                                                  user_lat=user_lat,
                                                  user_lng=user_lng,
                                                  start=start)
        self._logger.info('Succesfully searched organizations')
        return orgs

    def _validate(self, schema, details):
        validator = Validator(schema)
        validator.allow_unknown = True
        res = validator.validate(details)
        if not res:
            message = '; '.join([
                f'"{key}": {", ".join(validator.errors[key])}'
                for key in validator.errors
            ])
            raise InvalidInputException(message=message)
